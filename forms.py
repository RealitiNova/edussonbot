from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Bid

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter username or email', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'})
    )

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

<!-- edusson_app/templates/edusson_app/signup.html -->
<h2>Sign Up</h2>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Render the form fields -->
    
    <!-- Display any form errors -->
    {% if form.errors %}
        <ul>
            {% for field in form %}
                {% for error in field.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            {% endfor %}
        </ul>
    {% endif %}
    
    <button type="submit">Sign Up</button>
</form>


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['order_id', 'title', 'subject', 'bid_amount']
        widgets = {
            'order_id': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'bid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }



