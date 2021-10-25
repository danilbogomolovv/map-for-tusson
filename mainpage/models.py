from django.db import models
#from django.contrib.postgres.fields import JSONField
# Create your models here.

# class Right_components(models.Model):
# 	street_number = models.CharField(max_length = 400, null = True)
# 	route = models.CharField(max_length = 400, null = True)
# 	sublocality_level_1 = models.CharField(max_length = 400, null = True)
# 	locality = models.CharField(max_length = 400, null = True)
# 	administrative_area_level_2 = models.CharField(max_length = 400, null = True)
# 	administrative_area_level_1= models.CharField(max_length = 400, null = True)
# 	country = models.CharField(max_length = 400, null = True)

class Terminal(models.Model):
	cimei = models.CharField(max_length = 400, null = True)
	inr = models.CharField(max_length = 400, null = True)
	ctid = models.CharField(max_length = 400, null = True)
	cmid = models.CharField(max_length = 400, null = True)
	cpodr = models.CharField(max_length = 400, null = True)
	cadres = models.CharField(max_length = 400, null = True)
	cgorod = models.CharField(max_length = 400, null = True)
	cobl = models.CharField(max_length = 400, null = True)
	craion = models.CharField(max_length = 400, null = True)
	ddatan = models.DateField(max_length = 400, null = True)
	cname = models.CharField(max_length = 400, null = True)
	cparta = models.CharField(max_length = 400, null = True)
	cots = models.CharField(max_length = 400, null = True)
	czona = models.CharField(max_length = 400, null = True)
	zona_name = models.CharField(max_length = 400, null = True)
	cvsoba = models.CharField(max_length = 400, null = True)
	cunn = models.CharField(max_length = 400, null = True)
	cbank = models.CharField(max_length = 400, null = True)
	ctype = models.CharField(max_length = 400, null = True)
	right_adres = models.CharField(max_length = 400, null = True)
	right_components = models.CharField(max_length = 800, null = True)
	ss_nom = models.CharField(max_length = 400, null = True)
	ddatap = models.DateField(max_length = 400, null = True)
	cmemo = models.CharField(max_length = 700, null = True)
	cstatus = models.IntegerField( null = True)
	lat = models.CharField(max_length = 400, null = True)
	lng = models.CharField(max_length = 400, null = True)

class Office(models.Model):
	cpodr = models.CharField(max_length = 400, null = True)
	podr_name = models.CharField(max_length = 400, null = True)
	cadres = models.CharField(max_length = 400, null = True)
	cfio = models.CharField(max_length = 400, null = True)
	zona_name = models.CharField(max_length = 400, null = True)
	lat = models.CharField(max_length = 400, null = True)
	lng = models.CharField(max_length = 400, null = True)


class Marker(models.Model):
	cgorod = models.CharField(max_length = 400, null = True)
	cobl = models.CharField(max_length = 400, null = True)
	craion = models.CharField(max_length = 400, null = True)
	count = models.IntegerField( null = True)
	lat = models.CharField(max_length = 400, null = True)
	lng = models.CharField(max_length = 400, null = True)
	status = models.IntegerField( null = True)
	cadres = models.CharField(max_length = 400, null = True)
	zona_name = models.CharField(max_length = 400, null = True)
	terminals = models.ManyToManyField(Terminal)

class ErrorTerminal(models.Model):

	cadres = models.CharField(max_length = 400, null = True)
	ss_nom = models.CharField(max_length = 400, null = True)


class Zone(models.Model):
	zona = models.CharField(max_length = 400, null = True)
	name_zona = models.CharField(max_length = 400, null = True)
	cpodr = models.CharField(max_length = 400, null = True)

class Terminal_zona_name_and_count(models.Model):
	attr_name =  models.CharField(max_length = 400, null = True)
	attr_count =  models.IntegerField(null = True)

class Terminal_name_name_and_count(models.Model):
	attr_name =  models.CharField(max_length = 400, null = True)
	attr_count =  models.IntegerField(null = True)

class Terminal_part_name_and_count(models.Model):
	attr_name =  models.CharField(max_length = 400, null = True)
	attr_count =  models.IntegerField(null = True)

class Terminal_podr_name_and_count(models.Model):
	attr_name =  models.CharField(max_length = 400, null = True)
	attr_count =  models.IntegerField(null = True)

class Available(models.Model):
	attr_name = models.CharField(max_length = 400, null = True)
	value = models.CharField(max_length = 400, null = True)



