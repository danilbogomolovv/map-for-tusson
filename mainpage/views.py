from django.shortcuts import render
from django.http import HttpResponseRedirect
from lxml import etree
import xml.etree.ElementTree as ET
from .models import Terminal, ErrorTerminal, ExistTerminal, TerminalName
import googlemaps


def sort_terminals_parameters(context):
    terminal_names = []
    terminal_parts = []
    terminal_parts_with_count = {}
    terminal_names_with_count = {}

    for i in Terminal.objects.all():
        terminal_names.append(i.cname)
    for i in terminal_names:
        count = terminal_names.count(i)
        terminal_names_with_count[i] = count
    sort_terminal_names_with_count = sorted(terminal_names_with_count.items(), key=lambda x: x[1])
    sort_terminal_names_with_count.reverse()

    for i in Terminal.objects.all():
        terminal_parts.append(i.cparta)
    for i in terminal_parts:
        count = terminal_parts.count(i)
        terminal_parts_with_count[i] = count
    sort_terminal_parts_with_count = sorted(terminal_parts_with_count.items(), key=lambda x: x[1])
    sort_terminal_parts_with_count.reverse()


    context['terminal_names'] = sort_terminal_names_with_count
    context['terminal_parts'] = sort_terminal_parts_with_count



def index(request):
    context = {}
    if len(Terminal.objects.all()) == 0: 
        count = 0
        lats = []
        lngs = []
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals4.xml", parser=parser)
        root = tree.getroot()
        for child in root:
            try:
                gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
                geocode_result = gmaps.geocode(child[8].text)
                if geocode_result[0]['geometry']['location']['lat'] not in lats and geocode_result[0]['geometry']['location']['lng'] not in lngs:
                    new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                            cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                            ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                            lat = geocode_result[0]['geometry']['location']['lat'],
                                            lng = geocode_result[0]['geometry']['location']['lng'])
                    new_terminal.save()
                    lats.append(geocode_result[0]['geometry']['location']['lat'])
                    lngs.append(geocode_result[0]['geometry']['location']['lng'])

                    print('OK ' + str(count) + str(child[8].text))
                    count = count + 1
                else:
                    new_exist_terminal = ExistTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                            cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                            ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text)
                    new_exist_terminal.save()   
                    print('EXIST ' + str(count) + str(child[8].text))
                    count = count + 1 

            except Exception as e:
                new_error_terminal = ErrorTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text)  
                new_error_terminal.save() 
                print('ERROR ' + str(count) + str(child[8].text))
                count = count + 1 

 
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


    sort_terminals_parameters(context)
    context['terminals'] = Terminal.objects.all()
    context['existterminals'] = ExistTerminal.objects.all()
    search_name = request.GET.get("name", "")
    search_parta = request.GET.get("parta", "")
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    return render(request, 'mainpage/mainpage.html', context)  


def search(request, name = "", parta = ""):
    context = {}

    search_name_terminals = []
    search_parta_terminals = []
    search_terminals = []
    search_name = request.GET.get("name", "")
    search_parta = request.GET.get("parta", "")

    if search_name != "":
        for i  in Terminal.objects.all():
            if i.cname == search_name:
                search_name_terminals.append(i)
                
    if search_parta != "":
        for i in Terminal.objects.all():
            if i.cparta == search_parta:
                search_parta_terminals.append(i)

    if search_name != "" and search_parta != "":
        for i in Terminal.objects.all():
            if i.cname == search_name and i.cparta == search_parta:
                search_terminals.append(i)


    sort_terminals_parameters(context)
    context['search_name'] = search_name
    context['search_parta'] = search_parta

    if search_name == "" and search_parta == "":
        context['terminals'] = Terminal.objects.all()
    elif search_name != "" and search_parta == "":
        context['terminals'] = search_name_terminals
    elif search_parta != "" and search_name == "":
        context['terminals'] = search_parta_terminals
    elif search_parta != "" and search_name != "":
        context['terminals'] = search_terminals

    context['existterminals'] = ExistTerminal.objects.all()
    return render(request, 'mainpage/mainpage.html', context)

def save(request):
    root = ET.Element('VFPData')

    for i in Terminal.objects.all():
        level1 = ET.SubElement(root, 'terminals')
        cimei = ET.SubElement(level1, 'cimei')
        cimei.text = str(i.cimei)
        inr = ET.SubElement(level1, 'inr')
        inr.text = str(i.inr)
        ctid = ET.SubElement(level1, 'ctid')
        ctid.text = str(i.ctid)
        cmid = ET.SubElement(level1, 'cmid')
        cmid.text = str(i.cmid)
        cpodr = ET.SubElement(level1, 'cpodr')
        cpodr.text = str(i.cpodr)
        cadres = ET.SubElement(level1, 'cadres')
        cadres.text = str(i.cadres)
        cgorod = ET.SubElement(level1, 'cgorod')
        cgorod.text = str(i.cgorod)
        cobl = ET.SubElement(level1, 'cobl')
        cobl.text = str(i.cobl)
        craion = ET.SubElement(level1, 'craion')
        craion.text = str(i.craion)
        ddatan = ET.SubElement(level1, 'ddatan')
        ddatan.text = str(i.ddatan)
        cname = ET.SubElement(level1, 'cname')
        cname.text = str(i.cname)
        cparta = ET.SubElement(level1, 'cparta')
        cparta.text = str(i.cparta)
        cots = ET.SubElement(level1, 'cots')
        cots.text = str(i.cots)
        lat = ET.SubElement(level1, 'lat')
        lat.text = str(i.lat)
        lng = ET.SubElement(level1, 'lng')
        lng.text = str(i.lng)

    ET.indent(root)
    tree = ET.ElementTree(root)
    tree.write('saveterminals.xml', xml_declaration=None, default_namespace=None, method="xml", encoding="Windows-1251") 
    return HttpResponseRedirect('/')
