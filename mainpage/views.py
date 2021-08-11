from django.shortcuts import render
import os
from django.db.models import F, Q, When
from django.http import HttpResponseRedirect
from django.conf import settings
from lxml import etree
import xml.etree.ElementTree as ET
from .models import *
from .forms import *
import json as simplejson
import googlemaps
from datetime import datetime
from django.db.models import F

q_objects = Q()
#q_objects |= Q(zona_name__startswith='Минский')
list_q_objects = [q_objects]
terminal_names_for_drop_down_list = []
terminal_parts_for_drop_down_list = []
terminal_zones_for_drop_down_list = []
terminal_cpodr_for_drop_down_list = []

def append_zones():
    
    """ Функция считывающая все зоны из xml файла и добавляющая их в модели """

    parser = ET.XMLParser(encoding="windows-1251")
    tree = ET.parse("szonas.xml", parser = parser)
    root = tree.getroot()
    for child in root:
        new_zone = Zone(zona = child[0].text, name_zona = child[1].text)
        new_zone.save()
        print(child[1].text)

def append_terminals():

    """ Функция считывающая все терминалы из xml файла и добавляющая их в модели """

    count = 1
    parser = ET.XMLParser(encoding="windows-1251")
    tree = ET.parse("terminals.xml", parser=parser)
    root = tree.getroot()

    for child in root:

        for i in Zone.objects.all():
            if child[13].text == i.zona:
                zona_name = i.name_zona
        try:

            gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))

            geocode_result = gmaps.geocode(child[8].text, language = 'ru', region = 'BY')
    
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

def count_terminal_attribute(attr, context):

    """ Функция которая находит все индивидуальные вхождения для любого аттрибута терминала и возвращает список с этими вхождениями """
    
    result = []
    for i in list(Terminal.objects.values_list(attr, flat=True)):
        if i not in result:
            result.append(i)
    json_list = simplejson.dumps(result)
    context['available' + attr] = json_list

def count_repair_terminal_attribute(attr, context):

    """ Функция которая находит все индивидуальные вхождения для любого аттрибута терминала в ремонте и возвращает список с этими вхождениями """
    
    result = []
    for i in list(Terminal.objects.filter(cstatus=3).values_list(attr, flat=True)):
        if i not in result:
            result.append(i)
    json_list = simplejson.dumps(result)
    context['available' + attr] = json_list

def get_q_objects(request):

    """ Функция высчитывающая какие зоны с терминалами демонстрировать пользователю """

    zones = request.POST.getlist('zones')
    q_objects = Q()
    for z in zones:
        q_objects |= Q(zona_name__startswith=z)
    if not zones:
        return  Q(zona_name__startswith='f')
    if zones:
        list_q_objects.append(q_objects)
    if len(list_q_objects) > 2:
        list_q_objects.pop(-2)
    return list_q_objects[-1]

def terminal_lists_for_drop_down_list(context):

    """ Функция рассчитывающая все варианты и количество вхождений для четырех атрибутов всех терминалов """

    global terminal_names_for_drop_down_list
    terminal_names_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cname', flat=True), False)


    global terminal_parts_for_drop_down_list
    terminal_parts_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cparta', flat=True), False)


    global terminal_zones_for_drop_down_list
    terminal_zones_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('zona_name', flat=True), True)

    global terminal_cpodr_for_drop_down_list
    terminal_cpodr_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cpodr', flat=True), False)


def terminal_lists_for_search_terminals(context, search_terminals):

    """ Функция рассчитывающая все варианты и количество вхождений для трех атрибутов искомых терминалов """



    terminal_names = []
    for i in search_terminals:
        terminal_names.append(i.cname)
    terminal_names = search_terminals_info(terminal_names, False)
    terminal_parts = []
    for i in search_terminals:
        terminal_parts.append(i.cparta)
    terminal_parts = search_terminals_info(terminal_parts, False)
    terminal_zones = []
    for i in search_terminals:
        terminal_zones.append(i.zona_name)
    terminal_zones = search_terminals_info(terminal_zones, True)
    #if len(search_terminals) != len(Terminal.objects.all()):
    context['search_terminal_names'] = terminal_names
    context['search_terminal_parts'] = terminal_parts
    context['search_terminal_zones'] = terminal_zones


def search_terminals_info(terminal_attr, zona_check):

    """Функция для поиска всех вариантов какого-либо атрибута терминала и его количества вхождений"""

    to_list = list(terminal_attr)
    terminal_with_count = {}
    for i in to_list:
        count = to_list.count(i)
        if zona_check:
            for j in Zone.objects.all():
                if i == j.name_zona:
                    i = str(i) + ' (' + str(j.zona) + ') '
        terminal_with_count[i] = count
    sort_terminal_names_with_count = sorted(terminal_with_count.items(), key=lambda x: x[1])
    sort_terminal_names_with_count.reverse()
    return sort_terminal_names_with_count  


def index(request):
    context = {}
    check_terminals = {}
    print(list_q_objects)

    if len(Zone.objects.all()) == 0:
        append_zones()

    if len(Terminal.objects.all()) == 0:
        count = 1
        parser = ET.XMLParser(encoding="windows-1251")
        tree = ET.parse("terminals (15).xml", parser=parser)
        root = tree.getroot()

        for child in root:

            for i in Zone.objects.all():
                if child[13].text == i.zona:
                    zona_name = i.name_zona
            try:
                new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
                                        cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text,
                                        lat = child[19].text,
                                        lng = child[20].text, ddatap = child[21].text, cmemo = child[22].text, cstatus = child[23].text)
                new_terminal.save()

                mark_check = True

                for marker in Marker.objects.all():                  
                    if new_terminal.lat == marker.lat and new_terminal.lng == marker.lng:
                        marker.terminals.add(new_terminal)
                        marker.count = F('count') + 1
                        if new_terminal.cstatus == 3:
                            marker.status = 3
                        marker.save()
                        mark_check = False
                        break

                if mark_check:
                    new_marker = Marker(count = 1, lat = new_terminal.lat, lng = new_terminal.lng, status = new_terminal.cstatus, zona_name = new_terminal.zona_name)
                    new_marker.save()
                    new_marker.terminals.add(new_terminal)

                

                print('OK ' + str(count))
                count = count + 1
            except Exception as e:
                pass


#-----------------------------------------------------------------------ГЕОКОДИРОВАНИЕ НОВЫХ АДРЕСОВ-----------------------------------------------------------------
            

            # try:
            #     query_str = ''
            #     if child[5].text != '':
            #         query_str = query_str + child[5].text + ' область, '
            #     if child[6].text != '':
            #         query_str = query_str + child[6].text + ' район, '
            #     if child[7].text != '':
            #         query_str = query_str + child[7].text + ', '
            #     query_str = query_str + child[8].text
            #     gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
            #     if child[7].text != '':
            #         geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY", "city": str(child[7].text)})
            #     else:
            #         geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY"}) 

            #     right_components = ''
            #     for i in geocode_result[0]['address_components']:
            #         right_components = right_components + str(i['types']) + ' : ' + str(i['long_name']) + ',   '

            #     new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
            #                             cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
            #                             ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
            #                             czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
            #                             cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text,
            #                             right_adres = geocode_result[0]['formatted_address'], right_components = right_components,
            #                             lat = geocode_result[0]['geometry']['location']['lat'],
            #                             lng = geocode_result[0]['geometry']['location']['lng'], ddatap = child[21].text, cmemo = child[22].text, cstatus = child[23].text)
            #     new_terminal.save()
            #     print('OK ' + str(count))
            #     print(query_str)
            #     print(right_components)
            #     print('-----------------------------------------------------------')
            #     count = count + 1 
            # except Exception as e:
            #     new_error_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
            #                             cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
            #                             ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
            #                             czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
            #                             cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text,
            #                             right_adres = 'не найдено', right_components = 'не найдено',
            #                             lat = 'не найдено',
            #                             lng = 'не найдено', ddatap = child[21].text, cmemo = child[22].text, cstatus = child[23].text)
            #     # new_error_terminal = ErrorTerminal(ss_nom = child[18].text, cadres = child[8].text) 
            #     new_error_terminal.save()  
                
            #     print('ERROR' + str(count))  
            #     print(str(e))
            #     print('-----------------------------------------------------------')
            #     count = count + 1 


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # error_terminals = Terminal.objects.filter(lat = 'не найдено')
    # for i in error_terminals:
    #     print(i.cadres)
    #     for j in Zone.objects.all():
    #         if i.czona == j.zona:
    #             zona_name = j.name_zona
    #     try:
    #         query_str = ''
    #         if j.cobl != '':
    #             query_str = query_str + str(j.cobl) + ' область, '
    #         if j.craion != '':
    #             query_str = query_str + str(j.craion)  + ' район, '
    #         if j.cgorod != '':
    #             query_str = query_str + str(j.cgorod) + ', '
    #         query_str = query_str + str(j.cadres)
    #         gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
    #         if j.cgorod != '':
    #             geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY", "city": str(j.cgorod)})
    #         else:
    #             geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY"}) 

    #         right_components = ''
    #         for i in geocode_result[0]['address_components']:
    #             right_components = right_components + str(i['types']) + ' : ' + str(i['long_name']) + ',   '

    #         new_terminal = Terminal(cimei =j. cimei, inr = j.inr, ctid = j.ctid, cmid = j.cmid, cpodr = j.cpodr,
    #                                 cobl = j.cobl, craion = j.craion, cgorod = j.cgorod, cadres = j.cadres,
    #                                 ddatan = j.ddatan, cname = j.cname, cparta = j.cparta, cots = j.cots,
    #                                 czona = j.czona, zona_name = zona_name, cvsoba = j.cvsoba, cunn = j.cunn,
    #                                 cbank = j.cbank, ctype = j.ctype, ss_nom = j.ss_nom,
    #                                 right_adres = geocode_result[0]['formatted_address'], right_components = right_components,
    #                                 lat = geocode_result[0]['geometry']['location']['lat'],
    #                                 lng = geocode_result[0]['geometry']['location']['lng'], ddatap = j.ddatap, cmemo = j.cmemo, cstatus = j.cstatus)
    #         new_terminal.save()
    #         print('OK ' + str(count))
    #         print(query_str)
    #         print(right_components)
    #         print('-----------------------------------------------------------')
    #         count = count + 1 
    #     except Exception as e:
    #         print('error')



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    context = {}  
    
    if terminal_names_for_drop_down_list == [] or terminal_parts_for_drop_down_list == [] or terminal_cpodr_for_drop_down_list == [] or terminal_zones_for_drop_down_list == []:
        terminal_lists_for_drop_down_list(context)

    context['terminal_names'] = terminal_names_for_drop_down_list
    context['terminal_parts'] = terminal_parts_for_drop_down_list
    context['terminal_zones'] = terminal_zones_for_drop_down_list
    context['terminal_cpodr'] = terminal_cpodr_for_drop_down_list


    count_terminal_attribute('cparta', context)

    try:
        
        if str(get_q_objects(request)) != '(AND: )':
            right_terminals = Marker.objects.filter(get_q_objects(request)).iterator()
        else:
            right_terminals = Marker.objects.filter(zona_name = 'f ').iterator()

    except Exception as e:
        right_terminals = Terminal.objects.filter(zona_name = 'f ').iterator()


    #context['terminals'] = right_terminals.only('lat','lng').iterator()
    #context['terminals_for_info'] = right_terminals.only('lat','lng','ctid','cparta','cname','cadres','cstatus','ddatap')
    context['mark'] = right_terminals
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['display'] = 'none'
    context['search_name'] = ''
    context['search_parta'] = ''
    context['search_cpodr'] = ''
    context['zone_check'] = True
    print("Длина : " + str(len(Terminal.objects.all())))
    print(list_q_objects)
    return render(request, 'mainpage/mainpage.html', context)  

def filter(request):
    context = {}
    context['display'] = 'none'
    context['mark'] = Marker.objects.filter(status = '10').iterator()
    filters_for_terminals = {}
    if request.method == 'POST':
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform
        if filterform.is_valid():
            
            for i in list(filterform.cleaned_data):     
                if filterform.cleaned_data[i] == '':
                    del filterform.cleaned_data[i]
                else:
                    value = filterform.cleaned_data[i]
                    i = i.replace('terminals__','')
                    filters_for_terminals[i] = value
            

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filters_for_terminals)):
                context['display'] = 'block'
                terminal_lists_for_search_terminals(context, Terminal.objects.filter(**filters_for_terminals))
                context['mark'] = Marker.objects.filter(**filterform.cleaned_data).iterator()
                #context['terminals_for_info'] = Terminal.objects.filter(**filterform.cleaned_data)
                context['count_search_terminals'] = len(Terminal.objects.filter(**filters_for_terminals))           
    else:
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform   

    context['count_all_terminals'] = len(Terminal.objects.all())
    count_terminal_attribute('cparta', context)


    for i in Terminal._meta.get_fields()[1:20]:
        if str(i) != 'mainpage.Terminal.ddatan' and str(i) != 'mainpage.Terminal.czona':
            count_terminal_attribute(str(i).replace('mainpage.Terminal.', ''), context)
           

    return render(request, 'mainpage/filterform.html', context)  


def search(request):
    context = {}
    filters = {}
    filters_for_terminals = {}
    count_terminal_attribute('cparta', context)
    search_name = request.GET.get("name", "")
    if search_name != '':
        filters['terminals__cname'] = search_name
        filters_for_terminals['cname'] = search_name

    search_parta = request.GET.get("parta", "")
    if search_parta != '':
        filters['terminals__cparta'] = search_parta
        filters_for_terminals['cparta'] = search_parta

    search_cpodr = request.GET.get("cpodr", "")
    if search_cpodr != '':
        filters['terminals__cpodr'] = search_cpodr
        filters_for_terminals['cpodr'] = search_cpodr
    print(filters)
    #search_markers = Marker.objects.filter(**filters)
    search_terminals = Terminal.objects.filter(**filters_for_terminals)
    terminal_lists_for_search_terminals(context, search_terminals)
    context['count_search_terminals'] =  len(search_terminals)
    context['display'] = 'block'
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_cpodr'] = search_cpodr
    # context['terminals'] = search_terminals.iterator()
    # context['terminals_for_info'] = search_terminals
    context['mark'] = Marker.objects.filter(**filters).iterator()
    context['zone_check'] = False

    context['count_all_terminals'] = len(Terminal.objects.all())

    context['terminal_names'] = terminal_names_for_drop_down_list
    context['terminal_parts'] = terminal_parts_for_drop_down_list
    context['terminal_zones'] = terminal_zones_for_drop_down_list
    context['terminal_cpodr'] = terminal_cpodr_for_drop_down_list
    return render(request, 'mainpage/mainpage.html', context)

def terminals_for_repair(request):
    context = {}
    filters_for_terminals = {}
    #terminals_for_repair = Terminal.objects.filter(cstatus = 3)
    #context['terminals'] = terminals_for_repair.only('lat','lng').iterator()
    #context['terminals_for_info'] = terminals_for_repair.only('lat','lng','ctid','cparta','cname') 
    context['mark'] = Marker.objects.filter(status = 3).iterator() 
    if request.method == 'POST':
        RepairForm = FilterForm(request.POST)
        context['repair_form'] = RepairForm
        if RepairForm.is_valid():
            
            for i in list(RepairForm.cleaned_data):
                if RepairForm.cleaned_data[i] == '':
                    del RepairForm.cleaned_data[i]
                else:
                    value = RepairForm.cleaned_data[i]
                    i = i.replace('terminals__','')
                    filters_for_terminals[i] = value

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filters_for_terminals)):
                context['display'] = 'block'
                terminal_lists_for_search_terminals(context, Terminal.objects.filter(**filters_for_terminals))
                context['mark'] = Marker.objects.filter(**RepairForm.cleaned_data).filter(status=3).iterator()
                context['count_search_terminals'] = len(Terminal.objects.filter(**filters_for_terminals))  
    else:
        RepairForm = FilterForm(request.POST)
        context['repair_form'] = RepairForm

    now = datetime.now().date()
    
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['terminals_for_repair'] = Marker.objects.filter(status = 3).iterator() 
    context['now_date'] = now
    context['display'] = 'none'

    for i in Terminal._meta.get_fields()[1:20]:
        if str(i) != 'mainpage.Terminal.ddatan' and str(i) != 'mainpage.Terminal.czona':
            count_repair_terminal_attribute(str(i).replace('mainpage.Terminal.', ''), context)
            
    return render(request, 'mainpage/terminals_for_repair.html', context)

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
        ss_nom = ET.SubElement(level1, 'ss_nom')
        ss_nom.text = str(i.ss_nom)
        lat = ET.SubElement(level1, 'lat')
        lat.text = str(i.lat)
        lng = ET.SubElement(level1, 'lng')
        lng.text = str(i.lng)
        right_components = ET.SubElement(level1, 'right_components')
        right_components.text = str(i.right_components)
        right_adres = ET.SubElement(level1, 'right_adres')
        right_adres.text = str(i.right_adres)

    ET.indent(root)
    tree = ET.ElementTree(root)
    tree.write('saveterminals.xml', xml_declaration=None, default_namespace=None, method="xml", encoding="Windows-1251") 
    return HttpResponseRedirect('/')

def one_terminal(request):
    context = {}
    search_ctid = request.GET.get("ctid", "")
    one_terminal = Marker.objects.filter(terminals__ctid = search_ctid)
    context['mark'] = one_terminal.iterator()
    context['lat'] = one_terminal[0].lat
    context['lng'] = one_terminal[0].lng
    context['display'] = 'none'
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/one_terminal.html', context)  

def search_terminals(request):
    context = {}
    print('sr')
    search_ctid = request.GET.get("ctid", "")
    search_ctid = search_ctid.split(',')
    q_ctid = Q()
    for ctid in search_ctid:
        q_ctid |= Q(terminals__ctid__startswith=ctid)
    one_terminal = Marker.objects.filter(q_ctid)
    context['mark'] = one_terminal.iterator()
    context['display'] = 'none'
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/search_terminals.html', context)  