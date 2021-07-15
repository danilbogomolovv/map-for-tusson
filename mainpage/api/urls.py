from django.urls import path

from .api_views import *

urlpatterns = [
	path('getterminals/', getTerminal.as_view(), name = 'getterminals'),
	path('postterminal/', postTerminal.as_view(), name = 'postterminals'),
	path('updateterminal/<str:ctid>', updateTerminal.as_view(), name = 'updateterminal'),
	path('deleteterminal/<str:ctid>', deleteTerminal.as_view(), name = 'deleteterminal'),
	#path('errorterminals/', ErrorTerminalListAPIView.as_view(), name = 'errorterminals')
]