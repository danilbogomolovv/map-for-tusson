from django.db import models

# Create your models here.

class Terminal(models.Model):
	cimei = models.CharField(max_length = 50, null = True)
	inr = models.CharField(max_length = 50, null = True)
	ctid = models.CharField(max_length = 50, null = True)
	cmid = models.CharField(max_length = 50, null = True)
	cpodr = models.CharField(max_length = 50, null = True)
	cadres = models.CharField(max_length = 50, null = True)
	cgorod = models.CharField(max_length = 50, null = True)
	cobl = models.CharField(max_length = 50, null = True)
	craion = models.CharField(max_length = 50, null = True)
	ddatan = models.DateField(max_length = 50, null = True)
	cname = models.CharField(max_length = 70, null = True)
	cparta = models.CharField(max_length = 50, null = True)
	cots = models.CharField(max_length = 50, null = True)
	lat = models.CharField(max_length = 30, null = True)
	lng = models.CharField(max_length = 30, null = True)

class ErrorTerminal(models.Model):
	cimei = models.CharField(max_length = 50, null = True)
	inr = models.CharField(max_length = 50, null = True)
	ctid = models.CharField(max_length = 50, null = True)
	cmid = models.CharField(max_length = 50, null = True)
	cpodr = models.CharField(max_length = 50, null = True)
	cadres = models.CharField(max_length = 50, null = True)
	cgorod = models.CharField(max_length = 50, null = True)
	cobl = models.CharField(max_length = 50, null = True)
	craion = models.CharField(max_length = 50, null = True)
	ddatan = models.DateField(max_length = 50, null = True)
	cname = models.CharField(max_length = 70, null = True)
	cparta = models.CharField(max_length = 50, null = True)
	cots = models.CharField(max_length = 50, null = True)


class ExistTerminal(models.Model):
	cimei = models.CharField(max_length = 50, null = True)
	inr = models.CharField(max_length = 50, null = True)
	ctid = models.CharField(max_length = 50, null = True)
	cmid = models.CharField(max_length = 50, null = True)
	cpodr = models.CharField(max_length = 50, null = True)
	cadres = models.CharField(max_length = 50, null = True)
	cgorod = models.CharField(max_length = 50, null = True)
	cobl = models.CharField(max_length = 50, null = True)
	craion = models.CharField(max_length = 50, null = True)
	ddatan = models.DateField(max_length = 50, null = True)
	cname = models.CharField(max_length = 70, null = True)
	cparta = models.CharField(max_length = 50, null = True)
	cots = models.CharField(max_length = 50, null = True)

class TerminalName(models.Model):
	terminal_name = models.CharField(max_length = 70, null = True)




