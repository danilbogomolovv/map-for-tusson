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
	ss_nom = models.CharField(max_length = 150, null = True)
	ddatap = models.CharField(max_length = 150, null = True)
	cmemo = models.CharField(max_length = 250, null = True)
	cstatus = models.CharField(max_length = 3, null = True)
	lat = models.CharField(max_length = 150, null = True)
	lng = models.CharField(max_length = 150, null = True)


class ErrorTerminal(models.Model):

	cadres = models.CharField(max_length = 150, null = True)
	ss_nom = models.CharField(max_length = 150, null = True)


class Zone(models.Model):
	zona = models.CharField(max_length = 150, null = True)
	name_zona = models.CharField(max_length = 150, null = True)

class Terminal_attr_name_and_count(models.Model):
	attr_name =  models.CharField(max_length = 150, null = True)
	attr_count =  models.CharField(max_length = 150, null = True)



