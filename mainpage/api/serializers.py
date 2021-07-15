from rest_framework import serializers

from ..models import *


class TerminalSerializer( serializers.ModelSerializer):
	class Meta:
		model = Terminal
		fields = '__all__'

	def create(self, validated_data):
		return Terminal.objects.create(**validated_data)


	def update(self, instance, validated_data):
		instance.cstatus = validated_data.get('cstatus', instance.cstatus)
		instance.cmemo = validated_data.get('cmemo', instance.cmemo)
		instance.save()
		return instance

class ErrorTerminalSerializer( serializers.ModelSerializer):

	class Meta:
		model = ErrorTerminal
		fields = '__all__'