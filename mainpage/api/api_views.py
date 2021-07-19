from rest_framework.generics import ListAPIView, ListCreateAPIView, get_object_or_404, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
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

# class getTerminal(APIView):

# 	def get(self, request):
# 		terminals = Terminal.objects.all()
# 		serializer = TerminalSerializer(terminals, many=True)
# 		return Response({"terminals": serializer.data})

# 	def post(self, request):

# 		terminal = request.data.get('terminal')
		
# 		serializer = TerminalSerializer(data=terminal)
# 		if serializer.is_valid(raise_exception=True):
# 			terminal_saved = serializer.save()
# 		print(serializer.errors)
# 		return Response({"success": "terminal with ctid '{}' created successfully".format(terminal_saved.ctid)})

# 	def put(self, request, ctid):
# 		saved_terminal = get_object_or_404(Terminal.objects.all(), ctid=ctid)
# 		data = request.data.get('terminal')
# 		serializer = TerminalSerializer(instance=saved_terminal, data=request.data, partial=True)
# 		if serializer.is_valid(raise_exception=True):
# 			terminal_saved = serializer.save()
# 		return Response({
# 			"success": "Terminal with ctid '{}' updated successfully".format(terminal_saved.ctid)
# 		})

# 	def delete(self, request, ctid):
# 		terminal = get_object_or_404(Terminal.objects.all(), ctid= ctid)
# 		terminal.delete()
# 		return Response({
# 			"message": "Terminal with ctid `{}` has been deleted.".format(ctid)
# 		}, status=204)

