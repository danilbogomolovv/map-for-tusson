from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from .serializers import *
from ..models import *
from rest_framework.response import Response

# class TerminalListAPIView(ListCreateAPIView):
# 	serializer_class = TerminalSerializer
# 	queryset = Terminal.objects.all()
# 	filter_backends = [SearchFilter]
# 	search_fields = ['cgorod']

class getTerminal(APIView):
	def get(self, request):
		terminals = Terminal.objects.all()
		serializer = TerminalSerializer(terminals, many=True)
		return Response({"terminals": serializer.data})

class postTerminal(APIView):
	def post(self, request):
		terminal = request.data.get('terminal')
        # Create an article from the above data
		serializer = TerminalSerializer(data=terminal)
		if serializer.is_valid(raise_exception=True):
			terminal_saved = serializer.save()
		return Response({"success": "terminal '{}' created successfully".format(terminal_saved.ctid)})

class updateTerminal(APIView):
	def put(self, request, ctid):
		saved_terminal = get_object_or_404(Terminal.objects.all(), ctid=ctid)
		data = request.data.get('terminal')
		serializer = TerminalSerializer(instance=saved_terminal, data=data, partial=True)
		if serializer.is_valid(raise_exception=True):
			terminal_saved = serializer.save()
		return Response({
			"success": "Terminal '{}' updated successfully".format(terminal_saved.title)
		})

class deleteTerminal(APIView):
	def delete(self, request, ctid):
		# Get object with this pk
		terminal = get_object_or_404(Terminal.objects.all(), ctid= ctid)
		terminal.delete()
		return Response({
			"message": "Terminal with ctid `{}` has been deleted.".format(ctid)
		}, status=204)