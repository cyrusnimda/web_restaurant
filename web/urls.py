from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('bookings', views.bookings, name='bookings'),
    path('contact', views.contact, name='contact'),
    path('stats', views.stats, name='stats'),
    path('bookings/new', views.new, name='new'),
    path('bookings/<int:booking_id>/delete', views.remove_booking, name='delete_booking'),
    path('', views.index, name='index'),
]