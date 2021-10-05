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
from .charts import *

q_objects = Q(zona_name__startswith='f')
#q_objects |= Q(zona_name__startswith='Минский')
list_q_objects = [q_objects]
terminal_names_for_drop_down_list = []
terminal_parts_for_drop_down_list = []
terminal_zones_for_drop_down_list = []
terminal_cpodr_for_drop_down_list = []

def append_zones():
    
    """ Функция считывающая все зоны из xml файла и добавляющая их в модели """

    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse("zona_utf8 (2).xml", parser = parser)
    root = tree.getroot()
    for child in root:
        new_zone = Zone(zona = child[0].text, name_zona = child[1].text, cpodr = child[2].text)
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
        list_q_objects.append(q_objects)
    # if not zones:
    #     return  Q(zona_name__startswith='f')
    # if zones:
    #     list_q_objects.append(q_objects)
    if len(list_q_objects) > 3:
        list_q_objects.pop(-2)
    return list_q_objects[-1]

def terminal_lists_for_drop_down_list(context):

    """ Функция рассчитывающая все варианты и количество вхождений для четырех атрибутов всех терминалов """
    
    # global terminal_names_for_drop_down_list
    # terminal_names_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cname', flat=True), False)
    # print('2')

    for i in search_terminals_info(Terminal.objects.values_list('cname', flat=True), False):
        print(i)
        Terminal_name_name_and_count.objects.create(attr_name = i[0], attr_count = int(i[1]))
        print(Terminal_name_name_and_count.objects.all())

    for i in search_terminals_info(Terminal.objects.values_list('cparta', flat=True), False):
        print(i)
        Terminal_part_name_and_count.objects.create(attr_name = i[0], attr_count = int(i[1]))
        print(Terminal_part_name_and_count.objects.all())
    for i in search_terminals_info(Terminal.objects.values_list('zona_name', flat=True), True):
        print(i)
        Terminal_zona_name_and_count.objects.create(attr_name = i[0], attr_count = int(i[1]))
        print(Terminal_zona_name_and_count.objects.all())
    for i in search_terminals_info(Terminal.objects.values_list('cpodr', flat=True), False):
        print(i)
        Terminal_podr_name_and_count.objects.create(attr_name = i[0], attr_count = int(i[1]))
        print(Terminal_podr_name_and_count.objects.all())
    # global terminal_parts_for_drop_down_list
    # terminal_parts_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cparta', flat=True), False)

    # print('3')

    # global terminal_zones_for_drop_down_list
    # terminal_zones_for_drop_down_list = search_terminals_info(Marker.objects.values_list('zona_name', flat=True), True)
    # print('4')

    # global terminal_cpodr_for_drop_down_list
    # terminal_cpodr_for_drop_down_list = search_terminals_info(Terminal.objects.values_list('cpodr', flat=True), False)
    # print('5')


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

    #Zone.objects.all().delete()
    if len(Zone.objects.all()) == 0:
        append_zones()

    #Office.objects.all().delete()
    if len(Office.objects.all()) == 0:
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse("spodr_utf8.xml", parser=parser)
        root = tree.getroot() 
         
        for child in root: 
                 
            for i in Zone.objects.all():
                if child[0].text == i.cpodr:
                    zona_name = i.name_zona

            gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
            geocode_result = gmaps.geocode(child[2].text, language = 'ru', components={"country":"BY"}) 

            new_office = Office(cpodr = child[0].text, podr_name = child[1].text, cadres = child[2].text, cfio = child[3].text,
                                zona_name = zona_name,lat = geocode_result[0]['geometry']['location']['lat'], 
                                lng = geocode_result[0]['geometry']['location']['lng'])
            new_office.save()



    if len(Terminal.objects.all()) == 0:
        count = 1
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse("term_utf8 (9).xml", parser=parser)
        root = tree.getroot()

        for child in root:

            for i in Zone.objects.all():
                if child[13].text == i.zona:
                    zona_name = i.name_zona
            try:
            #     #print(child[19].text, child[20].text)
            #     if child[19].text == None and child[20].text == None:

            #         try:
     
            #             query_str = ''
            #             if child[5].text != '':
            #                 query_str = query_str + child[5].text + ' область, '
            #             if child[6].text != '':
            #                 query_str = query_str + child[6].text + ' район, '
            #             if child[7].text != '':
            #                 query_str = query_str + child[7].text + ', '
            #             query_str = query_str + child[8].text
            #             gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API'))
            #             if child[7].text != '':
            #                 geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY", "city": str(child[7].text)})
            #             else:
            #                 geocode_result = gmaps.geocode(query_str, language = 'ru', components={"country":"BY"}) 

            #             right_components = ''
            #             for i in geocode_result[0]['address_components']:
            #                 right_components = right_components + str(i['types']) + ' : ' + str(i['long_name']) + ', '

            #             new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
            #                                     cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
            #                                     ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
            #                                     czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
            #                                     cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text, right_components = right_components,
            #                                     right_adres = geocode_result[0]['formatted_address'],
            #                                     lat = geocode_result[0]['geometry']['location']['lat'],
            #                                     lng = geocode_result[0]['geometry']['location']['lng'], cmemo = child[21].text, ddatap = child[22].text, cstatus = child[23].text)
            #             new_terminal.save()
            #             print('geocode')
            #             mark_check = True
            #         except:
            #             new_error_terminal = ErrorTerminal(ss_nom = child[18].text, cadres = child[8].text) 
            #             new_error_terminal.save()  

            #     else :
                new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
                                        cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text,
                                        lat = child[19].text,
                                        lng = child[20].text, cmemo = child[21].text, ddatap = child[22].text, cstatus = child[23].text)
                new_terminal.save()

                mark_check = True                      




                for marker in Marker.objects.all():                  
                    if new_terminal.lat == marker.lat and new_terminal.lng == marker.lng:
                        marker.terminals.add(new_terminal)
                        marker.count = F('count') + 1
                        if new_terminal.cstatus == 3:
                            marker.status = 3
                        if new_terminal.cstatus == 2:
                            marker.status = 2
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


    #---------------------------------------ДОБАВИТЬ НОРМАЛЬНУЮ ПРОВЕРКУ!!!!----------------------------------------

    if len(Terminal_name_name_and_count.objects.all()) == 0 and len(Terminal_part_name_and_count.objects.all()) == 0 and len(Terminal_podr_name_and_count.objects.all()) == 0 and len(Terminal_zona_name_and_count.objects.all()) == 0:
        terminal_lists_for_drop_down_list(context)

    context['terminal_names'] = Terminal_name_name_and_count.objects.all().iterator()
    context['terminal_parts'] = Terminal_part_name_and_count.objects.all().iterator()
    context['terminal_zones'] = Terminal_zona_name_and_count.objects.all().iterator()
    context['terminal_cpodr'] = Terminal_podr_name_and_count.objects.all().iterator()
    
    count_terminal_attribute('cparta', context)

    # try:
        
    #     if str(get_q_objects(request)) != '(AND: )':
    #         right_terminals = Marker.objects.filter(get_q_objects(request)).distinct().iterator()
    #     else:
    #         right_terminals = Marker.objects.filter(zona_name = 'f ').distinct().iterator()

    # except Exception as e:
    #     right_terminals = Terminal.objects.filter(zona_name = 'f ').distinct().iterator()

    for i in Office.objects.all():
        print(i.zona_name)
    context['mark'] = Marker.objects.filter(get_q_objects(request)).distinct().iterator()
    for i in Office.objects.filter(get_q_objects(request)).distinct().iterator():
        print(i.cadres)
    context['offices'] = Office.objects.filter(get_q_objects(request)).distinct().iterator()
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['display'] = 'none'
    context['search_name'] = ''
    context['search_parta'] = ''
    context['search_cpodr'] = ''
    context['zone_check'] = True
    #print("Длина : " + str(len(Terminal.objects.all())))
    
    #print(list_q_objects)

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
    filters_for_offices = {}
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
        filters_for_offices['cpodr'] = search_cpodr
        context['offices'] = Office.objects.filter(**filters_for_offices)
    print(filters)
    search_terminals = Terminal.objects.filter(**filters_for_terminals)
    terminal_lists_for_search_terminals(context, search_terminals)
    context['count_search_terminals'] =  len(search_terminals)
    context['display'] = 'block'
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_cpodr'] = search_cpodr
    context['mark'] = Marker.objects.filter(**filters).distinct().iterator()

    context['zone_check'] = False

    context['count_all_terminals'] = len(Terminal.objects.all())

    context['terminal_names'] = Terminal_name_name_and_count.objects.all().iterator()
    context['terminal_parts'] = Terminal_part_name_and_count.objects.all().iterator()
    context['terminal_zones'] = Terminal_zona_name_and_count.objects.all().iterator()
    context['terminal_cpodr'] = Terminal_podr_name_and_count.objects.all().iterator()
    return render(request, 'mainpage/mainpage.html', context)

def terminals_for_repair(request):
    context = {}
    filters_for_terminals = {}
    context['mark'] = Marker.objects.filter(status = 3).distinct().iterator() 
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
                context['mark'] = Marker.objects.filter(**RepairForm.cleaned_data).filter(status=3).distinct().iterator()
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

def terminals_for_installation(request):
    context = {}
    filters_for_terminals = {}
    context['mark'] = Marker.objects.filter(status = 2).distinct().iterator() 
    if request.method == 'POST':
        InstallationForm = FilterForm(request.POST)
        context['repair_form'] = InstallationForm
        if InstallationForm.is_valid():
            
            for i in list(InstallationForm.cleaned_data):
                if InstallationForm.cleaned_data[i] == '':
                    del InstallationForm.cleaned_data[i]
                else:
                    value = InstallationForm.cleaned_data[i]
                    i = i.replace('terminals__','')
                    filters_for_terminals[i] = value

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filters_for_terminals)):
                context['display'] = 'block'
                terminal_lists_for_search_terminals(context, Terminal.objects.filter(**filters_for_terminals))
                context['mark'] = Marker.objects.filter(**InstallationForm.cleaned_data).filter(status=2).distinct().iterator()
                context['count_search_terminals'] = len(Terminal.objects.filter(**filters_for_terminals))  
    else:
        InstallationForm = FilterForm(request.POST)
        context['repair_form'] = InstallationForm

    now = datetime.now().date()
    
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['terminals_for_repair'] = Marker.objects.filter(status = 2).iterator() 
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
    context['mark'] = one_terminal.distinct().iterator()
    context['lat'] = one_terminal[0].lat
    context['lng'] = one_terminal[0].lng
    context['display'] = 'none'
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/one_terminal.html', context)  

def search_terminals(request):
    context = {}
    search_ctid = request.GET.get("ctid", "")
    search_ctid = search_ctid.split(',')
    q_ctid = Q()
    for ctid in search_ctid:
        q_ctid |= Q(terminals__ctid__startswith=ctid)
    one_terminal = Marker.objects.filter(q_ctid)
    context['mark'] = one_terminal.distinct().iterator()
    context['display'] = 'none'
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/search_terminals.html', context)  

def route(request):

    context = {}
    tids_and_addresses = {}
    search_ctid = request.GET.get("ctid", "")
    if search_ctid != '':
        search_ctid = search_ctid.split(',')
    start = request.GET.get("start", "")
    end = request.GET.get("end", "")
    time_of_departure = request.GET.get("time_of_departure", "")
    time = request.GET.get("time", "")

    points = []
    for i in Office.objects.all():
        points.append(str(i.cadres) + ' ')

    context['availablepoints'] = points
    context['count_all_terminals'] = len(Terminal.objects.all())
    if search_ctid != '':
        q_ctid = Q()
        for ctid in search_ctid:
            q_ctid |= Q(terminals__ctid__startswith=ctid)
        search_objects = Marker.objects.filter(q_ctid)
        context['mark'] = search_objects.distinct().iterator()
        context['first'] = start
        context['last'] = end
        context['waypoints'] = search_objects.distinct().iterator()
        context['check'] = True
        context['time_of_departure'] = time_of_departure
        # for i in search_objects:
        #     for j in i.terminals.all():
        #         for tid in search_ctid:
        #             if tid == j.ctid:
        #                 tids_and_addresses[tid] = j.cadres

        # context['tids_and_addresses'] = tids_and_addresses
    else:
        context['check'] = False

    return render(request, 'mainpage/route.html', context)


def charts(request):
    context = {}
    attributes = {'cobl':'Области', 'cpodr':'Партнеры','cstatus':'Статусы'}
    search_chart_name = request.GET.get("chart_name", "")
    data ={}
    context['display'] = 'none'
    if search_chart_name != '':
        data = get_terminal_chart(Terminal.objects.all(), str(search_chart_name), str(attributes[search_chart_name]), request.GET.get("chart_type", ""))
    else:
        data['img'] = ''
        data['result'] = ''
    # for i in Terminal._meta.get_fields()[2:27]:
    #     print(str(i).replace('mainpage.Terminal.', ''))
    context['chart'] = data['img']
    context['result'] = data['result']
    context['attributes'] = attributes
    context['count_all_terminals'] = len(Terminal.objects.all())
    return render(request, 'mainpage/charts.html', context)

def add_new_marker(request):
    new_lat_lng = request.GET.get("latlng", "").replace('(','').replace(')','').split(', ')
    new_lat = new_lat_lng[0]
    new_lng = new_lat_lng[1]
    tids = request.GET.get("terminals", "")



    if tids != '': 
        print('not empty')
        tids = tids.split(',')
        new_marker = Marker(lat = new_lat, lng = new_lng, count = len(tids), status = 0)
        
        for tid in tids:
            marks = Marker.objects.filter(terminals__ctid__startswith = tid)
            for i in marks:
                for j in i.terminals.all():
                    if j.ctid == tid:

                        i.count -= 1
                        i.terminals.remove(j)
                        i.save()
                        j.lat = new_lat
                        j.lng = new_lng
                        j.save()
                        term = Terminal_zona_name_and_count.objects.get(attr_name__startswith = j.zona_name)
                        term.attr_count += 1
                        term.save()
                        new_marker.zona_name = j.zona_name
                        new_marker.save()
                        new_marker.terminals.add(j)
                        
                        
    else:
        print('empty')
        new_marker = Marker(lat = new_lat, lng = new_lng, count = 0, zona_name = 'Не определено', status = 0)

        new_marker.save()

        for i in Terminal_zona_name_and_count.objects.all():

            if i.attr_name == 'Не определено':
                
                i.attr_count = F('attr_count') + 1
                i.save()
                check_for_add = False
                break
            else:
                check_for_add = True

        if check_for_add:
            Terminal_zona_name_and_count.objects.create(attr_name = 'Не определено', attr_count = 1)
                

    return HttpResponseRedirect('/')

def delete_marker(request):
    del_lat = request.GET.get("lat", "")
    del_lng = request.GET.get("lng", "")

    del_marker = Marker.objects.get(lat = del_lat, lng = del_lng)
    del_mark_zone = Terminal_zona_name_and_count.objects.get(attr_name__startswith = del_marker.zona_name)
    del_mark_zone.attr_count -= 1
    del_mark_zone.save()
    del_marker.delete()

    return HttpResponseRedirect('/')

def add_terminal_to_marker(request):

    lat = request.GET.get("lat", "")
    lng = request.GET.get("lng", "")
    tids = request.GET.get("terminals", "")
    if tids != '':
        tids = tids.split(',')

    for tid in tids:
        marks = Marker.objects.filter(terminals__ctid__startswith = tid)
        for i in marks:
            for j in i.terminals.all():
                if j.ctid == tid:

                    i.count -= 1
                    i.terminals.remove(j)

                    if i.count == 0:
                        i.zona_name = 'Не определено'

                    j.lat = lat
                    j.lng = lng
                    i.save()
                    j.save()
                    destination_marker = Marker.objects.get(lat = lat, lng = lng)
                    destination_marker.terminals.add(j)
                    destination_marker.count = F('count') + 1
                    destination_marker.zona_name = j.zona_name
                    destination_marker.save()



    return HttpResponseRedirect('/')






