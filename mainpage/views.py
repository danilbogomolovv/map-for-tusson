from django.shortcuts import render
from lxml import etree
import xml.etree.ElementTree as ET
from .models import Terminal
import googlemaps


def index(request):
    context = {}

    if len(Terminal.objects.all()) == 0: 
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals.xml", parser=parser)
        root = tree.getroot()
        for child in root:
            gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
            geocode_result = gmaps.geocode(child[5].text)
            new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                    cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                    ddatan = child[9].text, cname = child[10].text, lat = geocode_result[0]['geometry']['location']['lat'],
                                    lng = geocode_result[0]['geometry']['location']['lng'])
            new_terminal.save()
#    else:
#        print(len(Terminal.objects.all()))
#        gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
#        geocode_result = gmaps.geocode('г. Минск, ул. Левкова, 12, пом. 1')
 #       print(geocode_result[0]['geometry']['location']['lat'])
  #      print(geocode_result[0]['geometry']['location']['lng'])

    context['terminals'] = Terminal.objects.all()
    return render(request, 'mainpage/mainpage.html', context)
