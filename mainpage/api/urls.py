from django.urls import path

from .api_views import *

urlpatterns = [
	path('terminals/', TerminalView.as_view(), name = 'gen_terminals'),
	path('update_terminal/<int:pk>', UpdateTerminalView.as_view(), name = 'update_terminals'),
]