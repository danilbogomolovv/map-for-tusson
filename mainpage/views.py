from django.shortcuts import render
from lxml import etree

def index(request):
    context = {}


    return render(request, 'mainpage/mainpage.html', context)
