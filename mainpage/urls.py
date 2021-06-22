from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('search/', views.search),
	path('save/', views.save),
    path('search/<str:name>/', views.search),
    path('search/<str:parta>', views.search),
    path('search/<str:zone>', views.search),

]