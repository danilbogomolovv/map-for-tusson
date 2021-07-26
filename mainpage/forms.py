from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User


class FilterForm(forms.Form):

	cbank = forms.CharField(max_length = 100, required = False, label='Банк', widget = forms.TextInput(attrs={'id': 'cbanks',
							 								 'placeholder':'Поиск по банку',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	ctype = forms.CharField(max_length = 100, required = False, label='Тип оборудования', widget = forms.TextInput(attrs={'id': 'ctypes',
							 								 'placeholder':'Поиск по типу оборудования',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cname = forms.CharField(max_length = 100, required = False, label='Название', widget = forms.TextInput(attrs={'id': 'cnames',
							 								 'placeholder':'Поиск по названию',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	inr = forms.CharField(max_length = 100, required = False, label='Артикул', widget = forms.TextInput(attrs={'id': 'inrs',
							 								 'placeholder':'Поиск по аритиклю',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	zona_name = forms.CharField(max_length = 100, required = False, label='Зона', widget = forms.TextInput(attrs={'id': 'zones',
							 								 'placeholder':'Поиск по зоне',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	ctid = forms.CharField(max_length = 100, required = False, label='Идентификатор', widget = forms.TextInput(attrs={'id': 'ctids',
							 								 'placeholder':'Поиск по идентификаторам',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cparta = forms.CharField(max_length = 100, required = False, label='Партнер', widget = forms.TextInput(attrs={'id': 'parts',
							 								 'placeholder':'Поиск по партнерам',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cunn = forms.CharField(max_length = 100, required = False, label='УНП', widget = forms.TextInput(attrs={'id': 'cunns',
							 								 'placeholder':'Поиск по УНП',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cadres = forms.CharField(max_length = 100, required = False, label='Адрес', widget = forms.TextInput(attrs={'id': 'cadres',
							 								 'placeholder':'Поиск по адресу',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cgorod = forms.CharField(max_length = 100, required = False, label='Город', widget = forms.TextInput(attrs={'id': 'cgorods',
							 								 'placeholder':'Поиск по городу',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	cvsoba = forms.CharField(max_length = 100, required = False, label='Вид собственности', widget = forms.TextInput(attrs={'id': 'cvsobas',
							 								 'placeholder':'Поиск по Виду собственности',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))

	cpodr = forms.CharField(max_length = 100, required = False, label='Отдел', widget = forms.TextInput(attrs={'id': 'cpodrs',
							 								 'placeholder':'Поиск по отделу',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))

class TerminalForRepairForm(forms.Form):

	cmemo = forms.CharField(max_length = 100, required = False, label='Проблема', widget = forms.TextInput(attrs={'id': 'cmemos',
							 								 'placeholder':'Поиск по проблеме',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))
	ddatap = forms.DateField( required = False, label='Дата', widget = forms.TextInput(attrs={'id': 'ddataps',
							 								 'placeholder':'Поиск по дате',
							 								 'class':'ui-autocomplite-input',
							 								 'autocomplie':'off'}))