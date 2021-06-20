from django.shortcuts import render
from lxml import etree
import xml.etree.ElementTree as ET
from .models import Terminal, ErrorTerminal, ExistTerminal, TerminalName
import googlemaps


def index(request, name=""):
    context = {}
    terminal_names = []
    if len(Terminal.objects.all()) == 0: 
        count = 0
        lats = []
        lngs = []
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals.xml", parser=parser)
        root = tree.getroot()
        for child in root:
            try:
                gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
                geocode_result = gmaps.geocode(child[5].text)
                if geocode_result[0]['geometry']['location']['lat'] not in lats and geocode_result[0]['geometry']['location']['lng'] not in lngs:
                    new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                            cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                            ddatan = child[9].text, cname = child[10].text, lat = geocode_result[0]['geometry']['location']['lat'],
                                            lng = geocode_result[0]['geometry']['location']['lng'])
                    new_terminal.save()
                    lats.append(geocode_result[0]['geometry']['location']['lat'])
                    lngs.append(geocode_result[0]['geometry']['location']['lng'])

                    print('OK ' + str(count) + str(child[5].text))
                    count = count + 1
                else:
                    new_exist_terminal = ExistTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                            cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                            ddatan = child[9].text, cname = child[10].text)
                    new_exist_terminal.save()   
                    print('EXIST ' + str(count) + str(child[5].text))
                    count = count + 1 

            except Exception as e:
                new_error_terminal = ErrorTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cadres = child[5].text, cgorod = child[6].text, cobl = child[7].text, craion = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text)  
                new_error_terminal.save() 
                print('ERROR ' + str(count) + str(child[5].text))
                count = count + 1 

#        for i in terminal_names:
#
#            new_terminal_name = TerminalName(terminal_name = i);
#            new_terminal_name.save()


#    count = 0
 
    for i in ErrorTerminal.objects.all():   
        print(i.cadres)
    print('ERROR ' + str(len(ErrorTerminal.objects.all())))  
    print('OK ' + str(len(Terminal.objects.all()))) 
#        try:
#        gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
#        geocode_result = gmaps.geocode(i.cadres)
#        if geocode_result != []:
#            new_terminal = Terminal(cimei = i.cimei, inr = i.inr, ctid = i.ctid, cmid = i.cmid, cpodr = i.cpodr,
#                                    cadres = i.cadres, cgorod = i.cgorod, cobl = i.cobl, craion = i.craion,
#                                    ddatan = i.ddatan, cname = i.cname, lat = geocode_result[0]['geometry']['location']['lat'],
#                                    lng = geocode_result[0]['geometry']['location']['lng'])
#            new_terminal.save()
#            print('OK ' + str(count))
#            count = count + 1
#            i.delete()
#        except Exception as e:
#        else:
#            print('ERROR ' + str(count))
#            count = count + 1
#    print('ERROR ' + str(len(ErrorTerminal.objects.all())))  
#    print('OK ' + str(len(Terminal.objects.all())))
    
    search_terminals = []

    for i in Terminal.objects.all():
        if i.cname not in terminal_names:
            terminal_names.append(i.cname)

    search_name = request.GET.get("name", "")

    for i  in Terminal.objects.all():
        if i.cname == search_name:
            search_terminals.append(i)

    context['search_name'] = search_name
    if search_name == "":
        context['terminals'] = Terminal.objects.all()
    else:
        context['terminals'] = search_terminals
    context['existterminals'] = ExistTerminal.objects.all()
    context['terminal_names'] = terminal_names
    return render(request, 'mainpage/mainpage.html', context)
