from django.shortcuts import render
from lxml import etree
import xml.etree.ElementTree as ET
from .models import Terminal, ErrorTerminal
import googlemaps


def index(request):
    context = {}

    if len(Terminal.objects.all()) == 0: 
        count = 0
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals.xml", parser=parser)
        root = tree.getroot()
        for child in root:
            try:
                gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
                geocode_result = gmaps.geocode(child[5].text)
                new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, lat = geocode_result[0]['geometry']['location']['lat'],
                                        lng = geocode_result[0]['geometry']['location']['lng'])
                new_terminal.save()
                print('OK ' + str(count))
                count = count + 1
            except Exception as e:
                new_error_terminal = ErrorTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text)  
                new_error_terminal.save() 
                print('ERROR ' + str(count))
                count = count + 1      


    context['terminals'] = Terminal.objects.all()
    return render(request, 'mainpage/mainpage.html', context)
