from hack.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	first_name = forms.CharField(max_length = 30)
	last_name = forms.CharField(max_length = 30)
	username = forms.EmailField(max_length=30)

	class Meta:
		model = User
		fields = ('username', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('phone',)