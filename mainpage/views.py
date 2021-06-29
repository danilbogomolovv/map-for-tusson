from django.shortcuts import render
from django.http import HttpResponseRedirect
from lxml import etree
import xml.etree.ElementTree as ET
from .models import *
from .forms import *
import json
import googlemaps

# def sort_terminals_parameters(context):
#     terminal_names = []
#     terminal_parts = []
#     terminal_zones = []
#     terminal_parts_with_count = {}
#     terminal_names_with_count = {}
#     terminal_zones_with_count = {}

#     for i in Terminal.objects.all():
#         terminal_names.append(i.cname)
#         terminal_parts.append(i.cparta)
#         terminal_zones.append(i.zona_name)

#     for i in terminal_names:
#         count = terminal_names.count(i)
#         terminal_names_with_count[i] = count
#     sort_terminal_names_with_count = sorted(terminal_names_with_count.items(), key=lambda x: x[1])
#     sort_terminal_names_with_count.reverse()
   
#     for i in terminal_parts:
#         count = terminal_parts.count(i)
#         terminal_parts_with_count[i] = count
#     sort_terminal_parts_with_count = sorted(terminal_parts_with_count.items(), key=lambda x: x[1])
#     sort_terminal_parts_with_count.reverse()
    
#     for i in terminal_zones:
#         count = terminal_zones.count(i)
#         terminal_zones_with_count[i] = count
#     sort_terminal_zones_with_count = sorted(terminal_zones_with_count.items(), key=lambda x: x[1])
#     sort_terminal_zones_with_count.reverse()

#     context['terminal_names'] = sort_terminal_names_with_count
#     context['terminal_parts'] = sort_terminal_parts_with_count
#     context['terminal_zones'] = sort_terminal_zones_with_count

def search_terminals_info(context, search_terminals):
    terminal_names = []
    terminal_parts = []
    terminal_zones = []
    terminal_parts_with_count = {}
    terminal_names_with_count = {}
    terminal_zones_with_count = {}

    for i in search_terminals:
        terminal_names.append(i.cname)
        terminal_parts.append(i.cparta)
        terminal_zones.append(i.zona_name)

    for i in terminal_names:
        count = terminal_names.count(i)
        terminal_names_with_count[i] = count
    sort_terminal_names_with_count = sorted(terminal_names_with_count.items(), key=lambda x: x[1])
    sort_terminal_names_with_count.reverse()
   
    for i in terminal_parts:
        count = terminal_parts.count(i)
        terminal_parts_with_count[i] = count
    sort_terminal_parts_with_count = sorted(terminal_parts_with_count.items(), key=lambda x: x[1])
    sort_terminal_parts_with_count.reverse()
    
    for i in terminal_zones:
        count = terminal_zones.count(i)
        terminal_zones_with_count[i] = count
    sort_terminal_zones_with_count = sorted(terminal_zones_with_count.items(), key=lambda x: x[1])
    sort_terminal_zones_with_count.reverse()
    if len(search_terminals) != len(Terminal.objects.all()):
        context['search_terminal_names'] = sort_terminal_names_with_count
        context['search_terminal_parts'] = sort_terminal_parts_with_count
        context['search_terminal_zones'] = sort_terminal_zones_with_count
    else:
        context['terminal_names'] = sort_terminal_names_with_count
        context['terminal_parts'] = sort_terminal_parts_with_count
        context['terminal_zones'] = sort_terminal_zones_with_count


def index(request):
    context = {}

    if len(Zone.objects.all()) == 0:
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("szonas.xml", parser = parser)
        root = tree.getroot()
        for child in root:
            new_zone = Zone(zona = child[0].text, name_zona = child[1].text)
            new_zone.save()
            print(child[1].text)


    if len(Terminal.objects.all()) == 0: 
        count = 0
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals (1).xml", parser=parser)
        root = tree.getroot()

        for child in root:

            for i in Zone.objects.all():
                if child[13].text == i.zona:
                    zona_name = i.name_zona
            try:
                gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
                geocode_result = gmaps.geocode(child[8].text, language = 'ru')

                new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
                                        cbank = child[16].text, ctype = child[17].text, right_adres = geocode_result[0]['formatted_address'],
                                        lat = geocode_result[0]['geometry']['location']['lat'],
                                        lng = geocode_result[0]['geometry']['location']['lng'])
                new_terminal.save()
                print('OK ' + str(count))
                count = count + 1
            except Exception as e:
                new_error_terminal = ErrorTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text, zona_name = zona_name)
                new_error_terminal.save() 
                print('ERROR ' + str(count) + str(child[8].text))
                count = count + 1 
    context = {}
    # gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
    # datalist = []
    # for i in Terminal.objects.all():

    #     geocode_result = gmaps.geocode(i.cadres, language = 'ru')
    #     geocode_result[0]['adres_from_alibi'] = str(i.cadres)
    #     data = geocode_result[0]
    #     datalist.append(data)

    # with open('data.json', 'w', encoding='utf-8') as f:
    #     for i in datalist:
    #         json.dump(i, f, ensure_ascii=False, indent=4)


    search_terminals_info(context, Terminal.objects.all())
    context['terminals'] = Terminal.objects.all()
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['display'] = 'none'
    search_name = request.GET.get("name", "")
    search_parta = request.GET.get("parta", "")
    search_zone = request.GET.get("zone", "")
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_zone'] = search_zone
    return render(request, 'mainpage/mainpage.html', context)  

def filter(request):
    context = {}
    context['terminals'] = Terminal.objects.all()
    context['display'] = 'none'
    search_terminals_info(context, Terminal.objects.all())
    if request.method == 'POST':
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform
        context['search_name'] = ''
        context['search_parta'] = ''
        context['search_zone'] = ''
        if filterform.is_valid():

            for i in list(filterform.cleaned_data):
                if filterform.cleaned_data[i] == '':
                    del filterform.cleaned_data[i]

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filterform.cleaned_data)):
                context['display'] = 'block'
                search_terminals_info(context, Terminal.objects.filter(**filterform.cleaned_data))
            context['terminals'] = Terminal.objects.filter(**filterform.cleaned_data)
            context['count_search_terminals'] = len(Terminal.objects.filter(**filterform.cleaned_data))           
    else:
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform   

    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/filterform.html', context)  


def search(request):
    context = {}
    filters = {}

    search_name = request.GET.get("name", "")
    if search_name != '':
        filters['cname'] = search_name

    search_parta = request.GET.get("parta", "")
    if search_parta != '':
        filters['cparta'] = search_parta

    search_zone = request.GET.get("zone", "")
    if search_zone != '':
        filters['zona_name'] = search_zone

    search_terminals_info(context, Terminal.objects.filter(**filters))
    search_terminals_info(context, Terminal.objects.all())
    context['count_search_terminals'] =  len(Terminal.objects.filter(**filters))
    context['display'] = 'block'
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_zone'] = search_zone
    context['terminals'] = Terminal.objects.filter(**filters)
    context['count_all_terminals'] = len(Terminal.objects.all())
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













 
  #  count = 0
  #  for i in ErrorTerminal.objects.all():   
 #       gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
 #       geocode_result = gmaps.geocode(i.cadres)
 #       if geocode_result != []:
 #           new_terminal = Terminal(cimei = i.cimei, inr = i.inr, ctid = i.ctid, cmid = i.cmid, cpodr = i.cpodr,
 #                                   cadres = i.cadres, cgorod = i.cgorod, cobl = i.cobl, craion = i.craion,
 #                                   ddatan = i.ddatan, cname = i.cname, cparta = i.cparta, cots = i.cots,
 #                                   czona = i.czona, zona_name = i.zona_name, lat = geocode_result[0]['geometry']['location']['lat'],
 #                                   lng = geocode_result[0]['geometry']['location']['lng'])
 #           new_terminal.save()
 #           print('OK ' + str(count))
 #           count = count + 1


