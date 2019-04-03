from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from web.models import RestaurantApiClient, ApiRestaurantException, ApiRestaurantTokenInvalidException
from datetime import datetime, timedelta
from .forms import LoginForm, NewBookingForm
from collections import OrderedDict
from django.contrib import messages

apiClient = RestaurantApiClient()

def token_required(function):
    def wrap(request, *args, **kwargs):
        if request.session.has_key('token'):
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def index(request):
    return render(request, 'web/index.html')

def stats(request):
    return render(request, 'web/stats.html')

def logout(request):
    request.session.pop('user', None)
    request.session.pop('token', None)
    return redirect('login')

def login(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # login in api_restaurant
            try:
                username = form.cleaned_data['username']
                json_response = apiClient.sendRequest(settings.API_ENDPOINT + 'login',
                                                    http_method="post",
                                                    json={'username': username, 'password': form.cleaned_data['password']})
                token = json_response["token"]
                request.session["token"] = token
                request.session["user"] = username
                return redirect('index')
            except ApiRestaurantException as e:
                error = str(e)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        request.session.pop('user', None)
    return render(request, 'web/login.html', {'form': form, 'error': error})

@token_required
def contact(request):
    return render(request, 'web/contact.html')

@token_required
def new(request):
    date = request.GET.get('date', '')
    error = None
    
    if request.method == 'POST':
        form = NewBookingForm(request.POST, defaultDate=date)
        if form.is_valid():
            date = form.cleaned_data['date']
            persons = form.cleaned_data['persons']
            name = form.cleaned_data['name']

            try:
                apiClient.sendRequest(settings.API_ENDPOINT + 'bookings',
                                                        http_method="post",
                                                        json={'date': date, 'persons': persons, 'name' : name},
                                                        headers={'x-access-token': request.session["token"]})
                messages.success(request, 'New booking successfully added.')
                return redirect('index')
            except ApiRestaurantException as e:
                error = str(e)
                return render(request, 'web/bookings/new.html', {'form': form, 'date':date, 'error':error})
            except ApiRestaurantTokenInvalidException as e:
                request.session.pop('token', None)
                return redirect('login')
    else:
        form = NewBookingForm(defaultDate=date)

    return render(request, 'web/bookings/new.html', {'form': form, 'date':date, 'error':error})


@token_required
def bookings(request):
    error = None
    bookings = None
    tables = None
    
    if request.method == 'POST':
        # Get bookings for specific day
        dateString = request.POST['date']
        date = datetime.strptime(dateString, "%Y-%m-%d %H:%M")
    else:
        # Get today's bookings
        date = datetime.now()
        dateString = date.strftime("%Y-%m-%d")
    
    try:
        json_response = apiClient.sendRequest(settings.API_ENDPOINT + 'bookings',
                                                http_method="get",
                                                params={'date':dateString},
                                                headers={'x-access-token': request.session["token"]})
        bookings = json_response["bookings"]
    except ApiRestaurantException as e:
        error = str(e)
        return render(request, 'web/bookings/index.html', {'error': error, 'bookings': bookings, 'tables':tables, 'date':date})
    except ApiRestaurantTokenInvalidException as e:
        request.session.pop('token', None)
        return redirect('login')

    # Get all tables
    try:
        all_tables = apiClient.sendRequest(settings.API_ENDPOINT + 'tables',
                                                http_method="get",
                                                headers={'x-access-token': request.session["token"]})
    except ApiRestaurantException as e:
        error = str(e)
        return render(request, 'web/bookings/index.html', {'error': error, 'bookings': bookings, 'tables':tables, 'date':date})
    except ApiRestaurantTokenInvalidException as e:
        request.session.pop('token', None)
        return redirect('login')

    tables = OrderedDict()
    # inicilize array
    for hour in settings.BOOKING_HOURS:
        tables[hour] = {}
        for table in all_tables:
            tables[hour][table['id']] = {"available": True, "seats": table['seats'] }

    # Fill array with bookings
    for booking in bookings:
        date = datetime.strptime(booking["booked_at"], "%Y-%m-%dT%H:%M:%S+00:00")
        bookingTimeStart = date.strftime("%H:%M")
        bookingTimeEnd = date + timedelta(minutes = 30)
        bookingTimeEnd = bookingTimeEnd.strftime("%H:%M")
        for table_id in booking["tables"]:
            tables[bookingTimeStart][table_id]["available"] = False
            tables[bookingTimeStart][table_id]["booking_id"] = booking["id"]
            if bookingTimeEnd in tables:
                tables[bookingTimeEnd][table_id]["available"] = False
                tables[bookingTimeEnd][table_id]["booking_id"] = booking["id"]

    return render(request, 'web/bookings/index.html', {'error': error, 'bookings': bookings, 'tables':tables, 'date':date})
    
@token_required
def remove_booking(request, booking_id):
    try:
        apiClient.sendRequest(settings.API_ENDPOINT + 'bookings/' + str(booking_id),
                                                http_method="delete",
                                                headers={'x-access-token': request.session["token"]})
        messages.success(request, 'Booking successfully removed.')
    except ApiRestaurantException as e:
        messages.error(request, str(e))
    except ApiRestaurantTokenInvalidException as e:
        request.session.pop('token', None)
        return redirect('login')

    return redirect('index')
    