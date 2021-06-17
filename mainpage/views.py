from django.shortcuts import render
from lxml import etree
import xml.etree.ElementTree as ET
from .models import Terminal

def index(request):
    context = {}

    if len(Terminal.objects.all()) == 0: 
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals.xml", parser=parser)
        root = tree.getroot()
        for child in root:
            new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                    cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                    ddatan = child[9].text, cname = child[10].text)
            new_terminal.save()
            #print(child[0].text)
            #print(child[1].text)
            #print(child[2].text)
            #print(child[3].text)
            #print(child[4].text)
            #print(child[5].text)
            #print(child[6].text)
            #print(child[7].text)
            #print(child[8].text)
            #print(child[9].text)
            #print(child[10].text)
            #for info in child:
            #    print(info.text)
            #print('----------------------------------------------------------------------')
            #print(child.tag, child.attrib)
    else:
        print(len(Terminal.objects.all()))

    context['terminals'] = Terminal.objects.all()
    return render(request, 'mainpage/mainpage.html', context)
