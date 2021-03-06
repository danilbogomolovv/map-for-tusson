from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.filters import SearchFilter
from .serializers import *
from ..models import *
from rest_framework.response import Response
from django.db.models import F

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

		# if not serializer_class.is_valid():
		# 	return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
		lat = ''
		lng = ''

		if request.data.get('lat') == '-' and request.data.get('lng') == '-':
			query_str = ''
			if request.data.get('cobl') != '-':
				query_str = query_str + request.data.get('cobl') + ' область, '
			if request.data.get('craion') != '':
				query_str = query_str + request.data.get('craion') + ' район, '
			if request.data.get('cgorod') != '':
				query_str = query_str + request.data.get('cgorod') + ', '
			query_str = query_str + request.data.get('cadres')
			gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
			geocode_result = gmaps.geocode(query_str, language = 'ru')
			request.data['lat'] = geocode_result[0]['geometry']['location']['lat']
			request.data['lng'] = geocode_result[0]['geometry']['location']['lng']
			lat = geocode_result[0]['geometry']['location']['lat']
			lng = geocode_result[0]['geometry']['location']['lng']
			right_components = {}
			for i in geocode_result[0]['address_components']:
				right_components[str(i['types']).replace("['","").replace("']", "").replace("political',","").replace(", 'political","").replace(" 'sublocality', ","").replace("'","")] = str(i['long_name']) 
				print(right_components)
		# new_right_components = Right_components.objects.create(**right_components)
		# new_right_components.save()
		zona_name = Zone.objects.get(zona = request.data.get('zona'))			
		new_terminal = Terminal.objects.create(**request.data)
		new_terminal.right_components = str(right_components)
		new_terminal.zona_name = str(zona_name.name_zona)
		new_terminal.save()

		mark_check = True
	# for marker in Marker.objects.all():                  
	# 	if request.data.get('lat') == marker.lat and request.data.get('lng')== marker.lng:
	# 		marker.terminals.add(new_terminal)
	# 		marker.count = F('count') + 1
	# 		if request.data.get('cstatus') == 3:
	# 			marker.status = 3
	# 		if request.data.get('cstatus') == 2:
	# 			marker.status = 2
		# 		marker.save()
		# 		mark_check = False
		# 		break
		try:
			mark = Marker.objects.get(lat = lat, lng = lng)
			mark.terminals.add(new_terminal)

	 		
			mark.count = F('count') + 1
			if request.data.get('cstatus') == 3:
				mark.status = 3
			if request.data.get('cstatus') == 2:
				mark.status = 2
			mark.save()


		except:
			new_marker = Marker(count = 1, lat = request.data.get('lat'), lng = request.data.get('lng'), status = request.data.get('cstatus'), zona_name = request.data.get('zona_name'))
			new_marker.save()
			new_marker.terminals.add(new_terminal)


		return Response()

class UpdateTerminalView(RetrieveUpdateDestroyAPIView):
	queryset = Terminal.objects.all()
	serializer_class = TerminalSerializer
	lookup_field = 'ctid'
		
	def put(self, request, *args, **kwargs):
		print(request.data)
		for marker in Marker.objects.all():                  
			if request.data.get('lat') == marker.lat and request.data.get('lng')== marker.lng:
				if request.data.get('cstatus') == 3:
					marker.status = 3
				if request.data.get('cstatus') == 2:
					marker.status = 2
				marker.save() 
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)
