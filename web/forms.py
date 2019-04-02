from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', 
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-4'}
        )
    )
    password = forms.CharField(
        label='Password', 
        max_length=20, 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-4'}
        )
    )

class NewBookingForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.defaultDate = kwargs.pop('defaultDate')
        super(NewBookingForm,self).__init__(*args,**kwargs)
        self.fields['date'].initial = self.defaultDate

    date = forms.CharField(
        label='Date', 
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-4 dateTimePicker'}
        )
    )
    persons = forms.CharField(
        label='Persons', 
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-4'}
        )
    )
    name = forms.CharField(
        label='Name', 
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-4'}
        )
    )