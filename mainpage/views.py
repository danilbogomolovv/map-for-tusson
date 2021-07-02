from django.shortcuts import render
from django.http import HttpResponseRedirect
from lxml import etree
import xml.etree.ElementTree as ET
from .models import *
from .forms import *
import json
import googlemaps

def terminal_lists_for_drop_down_list(context, search_terminals):
    """ Функция вызывающая рассчитывающая все варианты для трех атрибутов терминала """
    terminal_names = []
    for i in search_terminals:
        terminal_names.append(i.cname)
    terminal_names = search_terminals_info(terminal_names)
    terminal_parts = []
    for i in search_terminals:
        terminal_parts.append(i.cparta)
    terminal_parts = search_terminals_info(terminal_parts)
    terminal_zones = []
    for i in search_terminals:
        terminal_zones.append(i.zona_name)
    terminal_zones = search_terminals_info(terminal_zones)
    if len(search_terminals) != len(Terminal.objects.all()):
        context['search_terminal_names'] = terminal_names
        context['search_terminal_parts'] = terminal_parts
        context['search_terminal_zones'] = terminal_zones
    else:
        context['terminal_names'] = terminal_names
        context['terminal_parts'] = terminal_parts
        context['terminal_zones'] = terminal_zones

 

def search_terminals_info(terminal_attr):

    """Функция для поиска всех вариантов какого-либо атрибута терминала и его количества вхождений"""

    terminal_with_count = {}
    for i in terminal_attr:
        count = terminal_attr.count(i)
        terminal_with_count[i] = count
    sort_terminal_names_with_count = sorted(terminal_with_count.items(), key=lambda x: x[1])
    sort_terminal_names_with_count.reverse()
    return sort_terminal_names_with_count  


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
        count = 1
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals.xml", parser=parser)
        root = tree.getroot()

        for child in root:

            for i in Zone.objects.all():
                if child[13].text == i.zona:
                    zona_name = i.name_zona
            try:
                gmaps = googlemaps.Client(key='AIzaSyC_CpD9oSCYYDu92Jq8EiIGklCgyelDbiw')
                query_str = ''
                if child[5].text != '':
                    query_str = query_str + child[5].text + ' область, '
                if child[6].text != '':
                    query_str = query_str + child[6].text + ' район, '
                query_str = query_str + child[8].text
                geocode_result = gmaps.geocode(child[8].text, language = 'ru')
                #attr = {}

                # try:
                #     attr['right_city_distrcit'] = geocode_result[0]['address_components'][2]['long_name']
                # except:
                #     pass
                # try:
                #     attr['right_district'] = geocode_result[0]['address_components'][4]['long_name']
                # except:
                #     pass
                # try:
                #     attr['right_area'] = geocode_result[0]['address_components'][5]['long_name']
                # except:
                #     pass
            
                # new_terminal = Terminal_for_check(ss_nom = child[18].text,
                #                                     cadres = child[8].text,
                #                                     cobl = child[5].text, craion = child[6].text, cgorod = child[7].text,
                #                                     right_adres = geocode_result[0]['formatted_address'],
                #                                     lat = geocode_result[0]['geometry']['location']['lat'],
                #                                     lng = geocode_result[0]['geometry']['location']['lng'],
                #                                     **attr)
                # new_terminal.save()
                # print('OK ' + str(count))
                # count = count + 1       
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
                print('-------------------------')
                print(e)
                print('-------------------------')
                new_error_terminal = ErrorTerminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text,
                                        zona_name = zona_name,
                                        ss_nom = child[18].text)
                new_error_terminal.save() 
                print('ERROR ' + str(count) + str(child[8].text))
                count = count + 1 
    context = {}
   # print(len(Terminal_for_check.objects.all()))
   # print(len(ErrorTerminal.objects.all()))
            
    terminal_lists_for_drop_down_list(context, Terminal.objects.all())

    context['terminals'] = Terminal.objects.all()
    context['allterminals'] = Terminal.objects.all()
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['display'] = 'none'
    context['search_name'] = ''
    context['search_parta'] = ''
    context['search_zone'] = ''
    if request.method == 'POST':
        zone_terminals = []
        zones = request.POST.getlist('zones')
        for i in zones:
            search_terminals_by_zone = Terminal.objects.filter(zona_name = i + ' филиал')
            for j in search_terminals_by_zone:
                zone_terminals.append(j)
        context['terminals'] = zone_terminals
    return render(request, 'mainpage/mainpage.html', context)  

def filter(request):
    context = {}
    context['terminals'] = Terminal.objects.all()
    context['display'] = 'none'
    terminal_lists_for_drop_down_list(context, Terminal.objects.all())
    if request.method == 'POST':
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform
        if filterform.is_valid():

            for i in list(filterform.cleaned_data):
                if filterform.cleaned_data[i] == '':
                    del filterform.cleaned_data[i]

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filterform.cleaned_data)):
                context['display'] = 'block'
                terminal_lists_for_drop_down_list(context, Terminal.objects.filter(**filterform.cleaned_data))
            context['terminals'] = Terminal.objects.filter(**filterform.cleaned_data)
            context['count_search_terminals'] = len(Terminal.objects.filter(**filterform.cleaned_data))           
    else:
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform   

    context['count_all_terminals'] = len(Terminal.objects.all())
    context['allterminals'] = Terminal.objects.all()
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

    terminal_lists_for_drop_down_list(context, Terminal.objects.filter(**filters))
    terminal_lists_for_drop_down_list(context, Terminal.objects.all())

    context['count_search_terminals'] =  len(Terminal.objects.filter(**filters))
    context['display'] = 'block'
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_zone'] = search_zone
    context['terminals'] = Terminal.objects.filter(**filters)
    context['allterminals'] = Terminal.objects.all()
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/mainpage.html', context)

def save(request):
    pass
    #root = ET.Element('VFPData')
    # ss_noms = []
    # for i in Terminal_for_check.objects.all():
    #     if i.ss_nom not in ss_noms:
    #         ss_noms.append(i.ss_nom)

    #         level1 = ET.SubElement(root, 'terminals')
    #         ss_nom = ET.SubElement(level1, 'ss_nom')
    #         ss_nom.text = str(i.ss_nom)
    #         cadres = ET.SubElement(level1, 'cadres')
    #         cadres.text = str(i.cadres)
    #         cobl = ET.SubElement(level1, 'cobl')
    #         cobl.text = str(i.cobl)
    #         craion = ET.SubElement(level1, 'craion')
    #         craion.text = str(i.craion)
    #         cgorod = ET.SubElement(level1, 'cgorod')
    #         cgorod.text = str(i.cgorod)
    #         right_adres = ET.SubElement(level1, 'right_adres')
    #         right_adres.text = str(i.right_adres)
    #         lat = ET.SubElement(level1, 'lat')
    #         lat.text = str(i.lat)
    #         lng = ET.SubElement(level1, 'lng')
    #         lng.text = str(i.lng)
    #         right_city_distrcit = ET.SubElement(level1, 'right_city_distrcit')
    #         right_city_distrcit.text = str(i.right_city_distrcit)
    #         right_district = ET.SubElement(level1, 'right_district')
    #         right_district.text = str(i.right_district)
    #         right_area = ET.SubElement(level1, 'right_area')
    #         right_area.text = str(i.right_area)

    # for i in ErrorTerminal.objects.all():
    #     level1 = ET.SubElement(root, 'terminals')
    #     ss_nom = ET.SubElement(level1, 'ss_nom')
    #     ss_nom.text = str(i.ss_nom)
    #     cadres = ET.SubElement(level1, 'cadres')
    #     cadres.text = str(i.cadres)

   



    # for i in Terminal.objects.all():
    #     level1 = ET.SubElement(root, 'terminals')
    #     cimei = ET.SubElement(level1, 'cimei')
    #     cimei.text = str(i.cimei)
    #     inr = ET.SubElement(level1, 'inr')
    #     inr.text = str(i.inr)
    #     ctid = ET.SubElement(level1, 'ctid')
    #     ctid.text = str(i.ctid)
    #     cmid = ET.SubElement(level1, 'cmid')
    #     cmid.text = str(i.cmid)
    #     cpodr = ET.SubElement(level1, 'cpodr')
    #     cpodr.text = str(i.cpodr)
    #     cadres = ET.SubElement(level1, 'cadres')
    #     cadres.text = str(i.cadres)
    #     cgorod = ET.SubElement(level1, 'cgorod')
    #     cgorod.text = str(i.cgorod)
    #     cobl = ET.SubElement(level1, 'cobl')
    #     cobl.text = str(i.cobl)
    #     craion = ET.SubElement(level1, 'craion')
    #     craion.text = str(i.craion)
    #     ddatan = ET.SubElement(level1, 'ddatan')
    #     ddatan.text = str(i.ddatan)
    #     cname = ET.SubElement(level1, 'cname')
    #     cname.text = str(i.cname)
    #     cparta = ET.SubElement(level1, 'cparta')
    #     cparta.text = str(i.cparta)
    #     cots = ET.SubElement(level1, 'cots')
    #     cots.text = str(i.cots)
    #     lat = ET.SubElement(level1, 'lat')
    #     lat.text = str(i.lat)
    #     lng = ET.SubElement(level1, 'lng')
    #     lng.text = str(i.lng)

    # ET.indent(root)
    # tree = ET.ElementTree(root)
    # tree.write('error_terminals.xml', xml_declaration=None, default_namespace=None, method="xml", encoding="Windows-1251") 
    # return HttpResponseRedirect('/')













 



