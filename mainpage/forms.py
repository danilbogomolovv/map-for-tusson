from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class FilterForm(forms.Form):

	cadres = forms.CharField(max_length = 50, required = False, label='Адрес', widget = forms.TextInput(attrs={'id': 'cadres',
							 								 'placeholder':'Поиск по адресу',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cgorod = forms.CharField(max_length = 50, required = False, label='Город', widget = forms.TextInput(attrs={'id': 'cgorods',
							 								 'placeholder':'Поиск по городу',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cobl = forms.CharField(max_length = 50, required = False, label='Область', widget = forms.TextInput(attrs={'id': 'cobls',
							 								 'placeholder':'Поиск по области',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	craion = forms.CharField(max_length = 50, required = False, label='Район', widget = forms.TextInput(attrs={'id': 'craions',
							 								 'placeholder':'Поиск по району',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cname = forms.CharField(max_length = 70, required = False, label='Название', widget = forms.TextInput(attrs={'id': 'cnames',
							 								 'placeholder':'Поиск по навзванию',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cparta = forms.CharField(max_length = 50, required = False, label='Партнер', widget = forms.TextInput(attrs={'id': 'parts',
							 								 'placeholder':'Поиск по партнерам',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	zona_name = forms.CharField(max_length = 50, required = False, label='Зона', widget = forms.TextInput(attrs={'id': 'zones',
							 								 'placeholder':'Поиск по зонам',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
