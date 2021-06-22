from rest_framework import serializers

from ..models import *

class TerminalSerializer(serializers.ModelSerializer):
	cimei = serializers.CharField()
	inr = serializers.CharField()
	ctid = serializers.CharField()
	cmid = serializers.CharField()
	cpodr = serializers.CharField()
	cadres = serializers.CharField()
	cgorod = serializers.CharField()
	cobl = serializers.CharField()
	craion = serializers.CharField()
	ddatan = serializers.DateField()
	cname = serializers.CharField()
	cparta = serializers.CharField()
	cots = serializers.CharField()
	lat = serializers.CharField()
	lng = serializers.CharField() 

	class Meta:
		model = Terminal
		fields = '__all__'

class ErrorTerminalSerializer(serializers.ModelSerializer):
	cimei = models.CharField()
	inr = models.CharField()
	ctid = models.CharField()
	cmid = models.CharField()
	cpodr = models.CharField()
	cadres = models.CharField()
	cgorod = models.CharField()
	cobl = models.CharField()
	craion = models.CharField()
	ddatan = models.DateField()
	cname = models.CharField()
	cparta = models.CharField()
	cots = models.CharField()

	class Meta:
		model = ErrorTerminal
		fields = '__all__'

class ExistTerminalSerializer(serializers.ModelSerializer):
	cimei = models.CharField()
	inr = models.CharField()
	ctid = models.CharField()
	cmid = models.CharField()
	cpodr = models.CharField()
	cadres = models.CharField()
	cgorod = models.CharField()
	cobl = models.CharField()
	craion = models.CharField()
	ddatan = models.DateField()
	cname = models.CharField()
	cparta = models.CharField()
	cots = models.CharField()

	class Meta:
		model = ExistTerminal
		fields = '__all__'