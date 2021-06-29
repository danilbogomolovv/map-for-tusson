from django.db import models

# Create your models here.

class Terminal(models.Model):
	cimei = models.CharField(max_length = 150, null = True)
	inr = models.CharField(max_length = 150, null = True)
	ctid = models.CharField(max_length = 150, null = True)
	cmid = models.CharField(max_length = 150, null = True)
	cpodr = models.CharField(max_length = 150, null = True)
	cadres = models.CharField(max_length = 150, null = True)
	cgorod = models.CharField(max_length = 150, null = True)
	cobl = models.CharField(max_length = 150, null = True)
	craion = models.CharField(max_length = 150, null = True)
	ddatan = models.DateField(max_length = 150, null = True)
	cname = models.CharField(max_length = 150, null = True)
	cparta = models.CharField(max_length = 150, null = True)
	cots = models.CharField(max_length = 150, null = True)
	czona = models.CharField(max_length = 150, null = True)
	zona_name = models.CharField(max_length = 150, null = True)
	cvsoba = models.CharField(max_length = 150, null = True)
	cunn = models.CharField(max_length = 150, null = True)
	cbank = models.CharField(max_length = 150, null = True)
	ctype = models.CharField(max_length = 150, null = True)
	right_adres = models.CharField(max_length = 150, null = True)
	lat = models.CharField(max_length = 150, null = True)
	lng = models.CharField(max_length = 150, null = True)

class ErrorTerminal(models.Model):
	cimei = models.CharField(max_length = 150, null = True)
	inr = models.CharField(max_length = 150, null = True)
	ctid = models.CharField(max_length = 150, null = True)
	cmid = models.CharField(max_length = 150, null = True)
	cpodr = models.CharField(max_length = 150, null = True)
	cadres = models.CharField(max_length = 150, null = True)
	cgorod = models.CharField(max_length = 150, null = True)
	cobl = models.CharField(max_length = 150, null = True)
	craion = models.CharField(max_length = 150, null = True)
	ddatan = models.DateField(max_length = 150, null = True)
	cname = models.CharField(max_length = 150, null = True)
	cparta = models.CharField(max_length = 150, null = True)
	cots = models.CharField(max_length = 150, null = True)
	czona = models.CharField(max_length = 150, null = True)
	zona_name = models.CharField(max_length = 150, null = True)
	cvsoba = models.CharField(max_length = 150, null = True)
	cunn = models.CharField(max_length = 150, null = True)
	cbank = models.CharField(max_length = 150, null = True)
	ctype = models.CharField(max_length = 150, null = True)


class TerminalName(models.Model):
	terminal_name = models.CharField(max_length = 150, null = True)

class Zone(models.Model):
	zona = models.CharField(max_length = 150, null = True)
	name_zona = models.CharField(max_length = 150, null = True)



class Terminal_for_check(models.Model):
	ss_nom = models.CharField(max_length = 150, null = True)
	cadres = models.CharField(max_length = 150, null = True)
	right_adres = models.CharField(max_length = 150, null = True)
	right_city_distrcit = models.CharField(max_length = 150, null = True)
	right_district = models.CharField(max_length = 150, null = True)
	right_area = models.CharField(max_length = 150, null = True)
