from django import forms
from django.contrib.auth import authenticate
from django.core.validators import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django_flatpickr.widgets import DateTimePickerInput
from .models import User, Complaint, Reservation, Invoice

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username / Email', max_length=50)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add css classes for input fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        username_or_email = self.data['username_or_email']
        password = self.data['password']

        user = authenticate(username=username_or_email, password=password)
        if not user:
            user = authenticate(email=username_or_email, password=password)
            if not user:
                raise forms.ValidationError('Credentials are incorrect.')

        if not user.is_active:
            raise forms.ValidationError('You must validate your email first.')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add css classes for input fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        if self.data['password1'] != self.data['password2']:
            raise ValidationError("Passwords do not match.")

        username = self.data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Username {username} is already in use.")

        email = self.data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Email {email} is already in use.")

    def clean_password2(self):
        pass


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'form-control'})


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['bike', 'requestDate', 'endDate']
        widgets = { 
            'requestDate': DateTimePickerInput(),
            'endDate': DateTimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class TopUpForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super(TopUpForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
