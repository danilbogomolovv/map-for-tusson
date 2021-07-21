from rest_framework import serializers

from ..models import *


class TerminalSerializer( serializers.ModelSerializer):
	class Meta:
		model = Terminal
		fields = '__all__'
		

class ErrorTerminalSerializer( serializers.ModelSerializer):
	inr = serializers.CharField(default=None, source='checkouts.checked_out', read_only=True)
	class Meta:
		model = ErrorTerminal
		fields = '__all__'
