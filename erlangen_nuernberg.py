#!python3
from urllib.request import *

from bs4 import BeautifulSoup as parse
import re
import datetime
import traceback
import sys

from pyopenmensa.feed import LazyBuilder

from utils import Parser

date_regex = re.compile('(?P<day>[0-9].)\.(?P<month>[0-9].)\.(?P<year>[0-9]*)')
fressen_regex = re.compile('(?P<pre>.*)(?P<essen>Essen [1-9]|Tagesangebot|Aktionsessen [1-9])(?P<post>.*)')
refs_regex = re.compile('\[(?P<refs>.*)\]')
pricing_regex = re.compile('(?P<stud>[0-9]*,[0-9].|-).* (?P<bed>[0-9]*,[0-9].|-).* (?P<guest>[0-9]*,[0-9].|-).*')

roles = ('student', 'employee', 'other')

def get_session_cookie(url):
    info = urlopen(url).info()
    return info.get('Set-Cookie')

def get_data(url, cookie):
    r = Request(url)
    r.add_header('Cookie', cookie)
    return urlopen(r).read()

def get_next_day_data(url, cookie):
    data = 'mybutton=vorwärts'
    r = Request(url, data=data.encode("UTF-8"))
    r.add_header('Cookie', cookie)
    return urlopen(r).read()

def has_next_day(doc):
    button = doc.find_all('input', class_='btn btn-default btn-sm btn-speise')[1]
    return 'disabled' not in str(button)

def get_meal_div(document):
    return document.find_all('div', class_='col-md-7 col-sm-7')[0].find_all('div')[1]

def is_new_meal_entry(tag):
    return fressen_regex.search(str(tag)) is not None

def get_pre_meal_data(tag):
    return fressen_regex.search(str(tag)).group('pre')

def get_middle_meal_data(tag):
    return fressen_regex.search(str(tag)).group('essen')

def get_post_meal_data(tag):
    return fressen_regex.search(str(tag)).group('post')

def get_meal_list(div):
    food_list = []
    tag_list = []
    is_first_meal_entry = True
    for tag in div.contents:
        if 'form' in str(tag):
            break
        else:
            if is_new_meal_entry(tag):
                # we need to split tag data since parasoup does not accept the broaken html stdandart that allows
                # non closing tags like <br> :'(
                if get_pre_meal_data(tag):
                    tag_list.append(get_pre_meal_data(tag))
                if is_first_meal_entry:
                    is_first_meal_entry = False
                else:
                    food_list.append(tag_list)
                tag_list = []
                tag_list.append(get_middle_meal_data(tag))
                tag_list.append(get_post_meal_data(tag))
            else:
                tag_list.append(tag)
    food_list.append(tag_list)
    return food_list


def get_pricing(tag_list):
    plist = []
    for tag in tag_list:
        if '€' in str(tag):
            result = pricing_regex.search(str(tag))
            plist.append(result.group('stud'))
            plist.append(result.group('bed'))
            plist.append(result.group('guest'))
    return plist

def get_special_meal_type(tag_list):
    for tag in tag_list:
        if is_new_meal_entry(tag):
            if 'Essen' not in fressen_regex.search(str(tag)).group('essen'):
                return fressen_regex.search(str(tag)).group('essen')
        return ''
    return ''

def parse_meal(date, tag_list, canteen):
    food_type = get_food_types(tag_list)
    if get_special_meal_type(tag_list):
        food_type = get_special_meal_type(tag_list) + ": " + food_type
    if not food_type:
        food_type = 'Essen'
    notes_string = build_notes_string(tag_list)
    food_description = get_food_description(tag_list)
    prices = get_pricing(tag_list)
    canteen.addMeal(date, food_type, food_description, [notes_string], prices, roles)

def get_food_description(tag_list):
    description = ''
    for tag in tag_list:
        if 'str' in str(type(tag)) or 'NavigableString' in str(type(tag)):
            string = str(tag)
            if '€' not in string and not is_new_meal_entry(tag):
                description += string
    description = description.replace('  ', ' ').replace('\n', '')
    return description


def parse_meal_of_day(div, canteen):
    if(mensa_is_open(div)):
        date = get_date(div)
        meal_list = get_meal_list(div)
        for meal in meal_list:
            parse_meal(date, meal, canteen)
    else:
        canteen.setDayClosed(get_date(div))

def mensa_is_open(div):
    return 'Speiseplan' in str(div) and 'Derzeit sind keine aktuellen' not in str(div)

def get_date(div):
    raw = div.find_all('button')[0].string
    result = date_regex.search(raw)
    day = result.group('day')
    month = result.group('month')
    year = result.group('year')
    return day+'.'+month+'.'+year

def date_broaken(div):
    try:
        get_date(div)
        return False
    except Exception as e:
        return True

def get_food_types(tag_list):
    food_type = ''
    for tag in tag_list:
        if '<img' in str(tag):
            food_type += get_food_type(tag) + ' '
    return food_type

def get_food_type(foot_img):
    img_src = foot_img.get('src')
    if 'R.png' in img_src:
        return 'Rind'
    if 'S.png' in img_src:
        return 'Schwein'
    if 'G.png' in img_src:
        return 'Geflügel'
    if 'V.png' in img_src:
        return 'Vegetarisch'
    if 'F.png' in img_src:
        return 'Fisch'
    if 'L.png' in img_src:
        return 'Lamm'
    if 'W.png' in img_src:
        return 'Wild'
    if 'veg.png' in img_src:
        return 'Vegan'
    if 'MSC.png' in img_src:
        return 'MSC Fisch'
    return ''

def get_food_refs(tag_list):
    refs = []
    for tag in tag_list:
        if '<sup>' in str(tag):
            refs.extend(refs_regex.search(tag.contents[0].contents[0]).group('refs').split(','))
    return refs

def build_notes_string(tag_list):
    refs = get_food_refs(tag_list)
    food_is = ''
    food_contains = ''
    for r in refs:
        # parse food is footnotes
        if r == '1':
            food_is += 'mit Farbstoffen, '
        elif r == '4':
            food_is += 'geschwärzt, '
        elif r == '5':
            food_is += 'mit Süßungsmittel, '
        elif r == '7':
            food_is += 'mit Antioxidationsmittel, '
        elif r == '8':
            food_is += 'mit Geschmacksverstärker, '
        elif r == '9':
            food_is += 'geschwefelt, '
        elif r == '10':
            food_is += 'geschwärzt, '
        elif r == '11':
            food_is += 'gewachst, '
        elif r == '12':
            food_is += 'mit Phosphat, '
        # parse allergic footnotes
        elif r == 'a1':
            food_contains += 'Gluten, '
        elif r == 'a2':
            food_contains += 'Krebstiere, '
        elif r == 'a3':
            food_contains += 'Eier, '
        elif r == 'a4':
            food_contains += 'Fisch, '
        elif r == 'a5':
            food_contains += 'Erdnüsse, '
        elif r == 'a6':
            food_contains += 'Soja, '
        elif r == 'a7':
            food_contains += 'Milch/Laktose, '
        elif r == 'a8':
            food_contains += 'Schalenfrüchte, '
        elif r == 'a9':
            food_contains += 'Sellerie, '
        elif r == 'a10':
            food_contains += 'Senf, '
        elif r == 'a11':
            food_contains += 'Sesam, '
        elif r == 'a12':
            food_contains += 'Schwefeldioxid/Sulfite, '
        elif r == 'a13':
            food_contains += 'Lupinen, '
        elif r == 'a14':
            food_contains += 'Weichtiere, '
        else:
            food_contains += 'undefinierte Chemikalien:' + r + ', '
    notes = ''
    if food_is != '':
        notes += 'Gericht ist ' + food_is
    if food_contains != '':
        if food_is == '':
            notes += 'Gericht enthält '
        else:
            notes += 'und enthält '
        notes += food_contains
    if notes != '':
        nl = list(notes)
        del nl[len(nl) - 1]
        nl[len(nl) - 1] = '.'
        notes = ''.join(nl)
    return notes

def parse_url(url, today=False):
    session_cookie = get_session_cookie(url)
    canteen = LazyBuilder()

    content = get_data(url, session_cookie)
    document = parse(content, 'lxml')
    meal_div = get_meal_div(document)
    # sometims the website or its developer is broken so we need to have a workaround for that
    if date_broaken(meal_div):
        now = datetime.datetime.now()
        canteen.setDayClosed(str(now.day) + "." + str(now.month) + "." + str(now.year))
    else:
        parse_meal_of_day(meal_div, canteen)
        while has_next_day(meal_div):
            content = get_next_day_data(url, session_cookie)
            document = parse(content, 'lxml')
            meal_div = get_meal_div(document)
            parse_meal_of_day(meal_div, canteen)

    return canteen.toXMLFeed()



parser = Parser('erlangen_nuernberg',
                handler=parse_url,
                shared_prefix='http://www.werkswelt.de/index.php?id=')
parser.define('er-langemarck', suffix='lmpl')
parser.define('er-sued', suffix='sued')
parser.define('n-schuett', suffix='isch')
parser.define('n-regens', suffix='regb')
parser.define('n-stpaul', suffix='spau')
parser.define('n-mensateria', suffix='mohm')
parser.define('n-hohfederstr', suffix='hohf')
parser.define('n-baerenschanzstr', suffix='baer')
parser.define('eichstaett', suffix='eich')
parser.define('ingolstadt', suffix='ingo')
parser.define('ansbach', suffix='ansb')
parser.define('triesdorf', suffix='trie')
