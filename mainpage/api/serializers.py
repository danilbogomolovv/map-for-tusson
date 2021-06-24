from rest_framework import serializers

from ..models import *

class BaseTerminalSerializer:
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
	czona = serializers.CharField()

class TerminalSerializer(BaseTerminalSerializer, serializers.ModelSerializer):
	lat = serializers.CharField()
	lng = serializers.CharField() 

	class Meta:
		model = Terminal
		fields = '__all__'

class ErrorTerminalSerializer(BaseTerminalSerializer, serializers.ModelSerializer):

	class Meta:
		model = ErrorTerminal
		fields = '__all__'