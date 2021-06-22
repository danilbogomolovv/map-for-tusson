from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import *
from ..models import *

class TerminalListAPIView(ListAPIView):
	serializer_class = TerminalSerializer
	queryset = Terminal.objects.all()
	filter_backends = [SearchFilter]
	search_fields = ['cgorod']

class ErrorTerminalListAPIView(ListAPIView):
	serializer_class = ErrorTerminalSerializer
	queryset = ErrorTerminal.objects.all()

class ExistTerminalListAPIView(ListAPIView):
	serializer_class = ExistTerminalSerializer
	queryset = ExistTerminal.objects.all()