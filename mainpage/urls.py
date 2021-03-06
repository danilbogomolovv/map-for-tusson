from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('search/', views.search),
	path('filter/', views.filter),
	path('terminals_for_repair/', views.terminals_for_repair),
	path('terminals_for_installation/', views.terminals_for_installation),
	path('save/', views.save),
	path('charts/', views.charts),
	path('charts/<str:chart_name>', views.charts),
	path('one_terminal/', views.one_terminal),
	path('one_terminal/<str:ctid>', views.one_terminal),
	path('search_terminals/', views.search_terminals),
	path('search_terminals/<str:ctid>', views.search_terminals),
	path('route/', views.route),
	path('route/<str:ctid>', views.route),
    path('search/<str:name>', views.search),
    path('search/<str:parta>', views.search),
    path('search/<str:zone>', views.search),
    path('add_new_marker/', views.add_new_marker),
    path('add_new_marker/<str:latlng>', views.add_new_marker),
    path('delete_marker/', views.delete_marker),
    path('delete_marker/<str:lat>', views.delete_marker),
    path('add_terminal_to_marker/', views.add_terminal_to_marker),
    path('add_terminal_to_marker/<str:lat>', views.add_terminal_to_marker),

]