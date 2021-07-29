from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import *
from ..models import *
from rest_framework.response import Response
import googlemaps
import os

class TerminalView(ListCreateAPIView):
	queryset = Terminal.objects.all()
	serializer_class = TerminalSerializer
	filter_backends = [SearchFilter]
	search_fields = ['ctid']	

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		if request.data.get('lat') == '-' and request.data.get('lng') == '-':
			query = ''
			if request.data.get('cgorod') != '-':
				query = request.data.get('cgorod') + ' ,'
			query = query + request.data.get('cadres')
			gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
			print(query)
			geocode_result = gmaps.geocode(query, language = 'ru')
			request.data['lat'] = geocode_result[0]['geometry']['location']['lat']
			request.data['lng'] = geocode_result[0]['geometry']['location']['lng']
	
		return self.create(request, *args, **kwargs)

class UpdateTerminalView(RetrieveUpdateDestroyAPIView):
	queryset = Terminal.objects.all()
	serializer_class = TerminalSerializer
	lookup_field = 'ctid'
