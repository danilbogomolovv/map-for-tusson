from rest_framework.generics import ListAPIView
from .serializers import *
from ..models import *

class TerminalListAPIView(ListAPIView):
	serializer_class = TerminalSerializer
	queryset = Terminal.objects.all()

class ErrorTerminalListAPIView(ListAPIView):
	serializer_class = ErrorTerminalSerializer
	queryset = ErrorTerminal.objects.all()

class ExistTerminalListAPIView(ListAPIView):
	serializer_class = ExistTerminalSerializer
	queryset = ExistTerminal.objects.all()