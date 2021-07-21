from django.urls import path

from .api_views import *

urlpatterns = [
	path('terminals/', TerminalView.as_view(), name = 'terminals'),
	path('update_terminal/<str:ctid>', UpdateTerminalView.as_view(), name = 'update_terminals'),
]