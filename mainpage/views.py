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

q_objects = Q()
q_objects |= Q(zona_name__startswith='Минский')
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

def get_q_objects(request):

    """ Функция высчитывающая какие зоны с терминалами демонстрировать пользователю """

    if request.method == 'POST':
        zones = request.POST.getlist('zones')
        q_objects = Q()
        for z in zones:
            q_objects |= Q(zona_name__startswith=z)
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
    if len(search_terminals) != len(Terminal.objects.all()):
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
    
    if len(Zone.objects.all()) == 0:
        append_zones()

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
                new_terminal = Terminal(cimei = child[0].text, inr = child[1].text, ctid = child[2].text, cmid = child[3].text, cpodr = child[4].text,
                                        cobl = child[5].text, craion = child[6].text, cgorod = child[7].text, cadres = child[8].text,
                                        ddatan = child[9].text, cname = child[10].text, cparta = child[11].text, cots = child[12].text,
                                        czona = child[13].text, zona_name = zona_name, cvsoba = child[14].text, cunn = child[15].text,
                                        cbank = child[16].text, ctype = child[17].text, ss_nom = child[18].text,
                                        lat = child[19].text, lng = child[20].text, ddatap = child[21].text, cmemo = child[22].text, cstatus = child[23].text)
                new_terminal.save()
                print('OK ' + str(count))
                count = count + 1 
            except:
                ...       

    context = {}  
    
    if terminal_names_for_drop_down_list == [] or terminal_parts_for_drop_down_list == [] or terminal_cpodr_for_drop_down_list == [] or terminal_zones_for_drop_down_list == []:
        terminal_lists_for_drop_down_list(context)

    context['terminal_names'] = terminal_names_for_drop_down_list
    context['terminal_parts'] = terminal_parts_for_drop_down_list
    context['terminal_zones'] = terminal_zones_for_drop_down_list
    context['terminal_cpodr'] = terminal_cpodr_for_drop_down_list

   
    count_terminal_attribute('cparta', context)

    try:
        right_terminals = Terminal.objects.filter(get_q_objects(request))
    except Exception as e:
        right_terminals = Terminal.objects.filter(zona_name = 'Минский филиал')

    context['terminals'] = right_terminals.only('lat','lng').iterator()
    context['terminals_for_info'] = right_terminals.only('lat','lng','ctid','cparta','cname')
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['display'] = 'none'
    context['search_name'] = ''
    context['search_parta'] = ''
    context['search_cpodr'] = ''
    print("Длина : " + str(len(Terminal.objects.all())))
    return render(request, 'mainpage/mainpage.html', context)  

def filter(request):
    context = {}
    context['display'] = 'none'
    context['terminals'] = Terminal.objects.filter(ctid = 'f').iterator()

    if request.method == 'POST':
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform
        if filterform.is_valid():
            
            for i in list(filterform.cleaned_data):
                if filterform.cleaned_data[i] == '':
                    del filterform.cleaned_data[i]

            if len(Terminal.objects.all()) != len(Terminal.objects.filter(**filterform.cleaned_data)):
                context['display'] = 'block'
                terminal_lists_for_search_terminals(context, Terminal.objects.filter(**filterform.cleaned_data))
                context['terminals'] = Terminal.objects.filter(**filterform.cleaned_data).iterator()
                context['terminals_for_info'] = Terminal.objects.filter(**filterform.cleaned_data)
                context['count_search_terminals'] = len(Terminal.objects.filter(**filterform.cleaned_data))           
    else:
        filterform = FilterForm(request.POST)
        context['filterform'] = filterform   

    context['count_all_terminals'] = len(Terminal.objects.all())
    count_terminal_attribute('cparta', context)


    for i in Terminal._meta.get_fields()[1:20]:
        if str(i) != 'mainpage.Terminal.ddatan' and str(i) != 'mainpage.Terminal.czona':
            count_terminal_attribute(str(i).replace('mainpage.Terminal.', ''), context)
            print(i)

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

    search_cpodr = request.GET.get("cpodr", "")
    if search_cpodr != '':
        filters['cpodr'] = search_cpodr
    
    search_terminals = Terminal.objects.filter(**filters)   
    terminal_lists_for_search_terminals(context, search_terminals)

    context['count_search_terminals'] =  len(search_terminals)
    context['display'] = 'block'
    context['search_name'] = search_name
    context['search_parta'] = search_parta
    context['search_cpodr'] = search_cpodr
    context['terminals'] = search_terminals.iterator()
    context['terminals_for_info'] = search_terminals

    context['count_all_terminals'] = len(Terminal.objects.all())

    context['terminal_names'] = terminal_names_for_drop_down_list
    context['terminal_parts'] = terminal_parts_for_drop_down_list
    context['terminal_zones'] = terminal_zones_for_drop_down_list
    context['terminal_cpodr'] = terminal_cpodr_for_drop_down_list
    return render(request, 'mainpage/mainpage.html', context)

def terminals_for_repair(request):
    context = {}
    now = datetime.now().date()
    terminals_for_repair = Terminal.objects.filter(cstatus = 3)
    context['count_all_terminals'] = len(Terminal.objects.all())
    context['terminals'] = terminals_for_repair.only('lat','lng').iterator()
    context['terminals_for_info'] = terminals_for_repair.only('lat','lng','ctid','cparta','cname')  
    context['terminals_for_repair'] = terminals_for_repair.only('cname','ddatap','cmemo','cparta', 'cadres') 
    context['now_date'] = now
    context['check_for_repair'] = False
    context['display'] = 'none'

    for i in terminals_for_repair:
        if i.ddatap < now:
            context['check_for_repair'] = True
            break    
    return render(request, 'mainpage/terminals_for_repair.html', context)

def save(request):
    return HttpResponseRedirect('/')
