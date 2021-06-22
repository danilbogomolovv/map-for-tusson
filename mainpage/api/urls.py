from django.urls import path

from .api_views import *

urlpatterns = [
	path('terminals/', TerminalListAPIView.as_view(), name = 'terminals'),
	path('errorterminals/', ErrorTerminalListAPIView.as_view(), name = 'errorterminals'),
	path('existterminals/', ExistTerminalListAPIView.as_view(), name = 'existterminals')
]