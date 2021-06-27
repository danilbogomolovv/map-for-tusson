from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class FilterForm(ModelForm):
	class Meta():
		model = Terminal
		fields = '__all__'