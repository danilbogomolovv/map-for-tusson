from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from ..models import *
from rest_framework.response import Response

class TerminalView(ListCreateAPIView):
	queryset = Terminal.objects.all()
	serializer_class = TerminalSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class UpdateTerminalView(RetrieveUpdateDestroyAPIView):
	queryset = Terminal.objects.all()
	serializer_class = TerminalSerializer
	lookup_field = 'ctid'
