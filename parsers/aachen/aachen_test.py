import datetime

from bs4 import BeautifulSoup as parse
import lxml.etree as ET

import openmensa_model as OpenMensa
from parsers.aachen.aachen import convert_to_openmensa_feed, parse_legend, parse_meal
from . import model as Aachen


def test_legend():
    html = parse(
        '<div class="bottom-wrap"><p class="price-note">Alle Angaben gelten für Studierende, Gäste zahlen einen Menüaufpreis von 1,50 € für folgende Gerichte: Tellergericht/Süßspeise, Vegetarisch, Klassiker, Empfehlung des Tages</p><div><p><b>Zusatzstoffe: </b>(1) Farbstoff, (2) Konservierungsstoff, (3) Antioxidationsmittel, (4) Geschmacksverstärker, (5) geschwefelt, (6) Geschwärzt, (8) Phosphat, (9) Süßungsmittel</p></div><div><p><b>Allergene: </b>(A) glutenhaltiges Getreide, (B) Sellerie, (C) Krebstiere, (D) Eier, (E) Fisch, (F) Erdnüsse, (G) Sojabohnen, (H) Milch, (J) Senf, (K) Sesamsamen, (L) Schwefeldioxid, (A1) Weizen, (A2) Roggen, (A3) Gerste, (A4) Hafer</p></div></div>',
        'lxml')
    actual = parse_legend(html)
    expected = {
        '1': 'Farbstoff',
        '2': 'Konservierungsstoff',
        '3': 'Antioxidationsmittel',
        '4': 'Geschmacksverstärker',
        '5': 'geschwefelt',
        '6': 'Geschwärzt',
        '8': 'Phosphat',
        '9': 'SüßungsmittelAllergene',
        'A': 'glutenhaltiges Getreide',
        'A1': 'Weizen',
        'A2': 'Roggen',
        'A3': 'Gerste',
        'A4': 'Hafer',
        'B': 'Sellerie',
        'C': 'Krebstiere',
        'D': 'Eier',
        'E': 'Fisch',
        'F': 'Erdnüsse',
        'G': 'Sojabohnen',
        'H': 'Milch',
        'J': 'Senf',
        'K': 'Sesamsamen',
        'L': 'Schwefeldioxid'
    }
    assert expected == actual


def test_model_conversion():
    day = OpenMensa.Day(datetime.date(2018, 2, 5))
    category = Aachen.Category(
        'TestCategory',
        price=OpenMensa.PriceWithRoles(180, [
            OpenMensa.Role('testRoleDefault'),
            OpenMensa.Role('testRoleSupplement', 100)
        ])
    )
    meal = Aachen.Meal('TestMeal', note_keys=['1', 'A'])
    category.append(meal)
    day.append(category)
    custom_model = [day]

    actual = convert_to_openmensa_feed(
        custom_model,
        {'1': 'FirstNote', 'A': 'SecondNote', 'A1': 'UnusedNote'}
    )

    canteen = OpenMensa.Canteen()
    openmensa_day = OpenMensa.Day(datetime.date(2018, 2, 5))
    openmensa_category = OpenMensa.Category('TestCategory')
    openmensa_meal = OpenMensa.Meal(
        'TestMeal',
        price=OpenMensa.PriceWithRoles(180, [
            OpenMensa.Role('testRoleDefault'),
            OpenMensa.Role('testRoleSupplement', 100)
        ]),
        notes=['FirstNote', 'SecondNote']
    )
    openmensa_category.append(openmensa_meal)
    openmensa_day.append(openmensa_category)
    canteen.insert(openmensa_day)

    assert canteen == actual


def test_meal_creation():
    html = parse('<tr class="main-dish"><td><p class="dish-text">'
                 'Wellenbandnudeln (A,D,A1) mit Shrimps <br>'
                 ' Tomaten-Cognac-Rahm (C,H,L) | Rucola-Tomaten-Salat (1,5,L)</p></td></tr>',
                 'lxml')

    meal_container = html.td
    actual = parse_meal(meal_container)

    expected = Aachen.Meal(
        "Wellenbandnudeln mit Shrimps | Tomaten-Cognac-Rahm | Rucola-Tomaten-Salat",
        ['A', 'D', 'A1', 'C', 'H', 'L', '1', '5'])

    assert expected == actual


def test_meal_to_xml():
    meal = OpenMensa.Meal('TestMeal', 180, ['BSecondNote', 'aThirdNote', 'AFirstNote'])

    expected = ET.fromstring(
        '<meal><name>TestMeal</name><note>AFirstNote</note><note>BSecondNote</note><note>aThirdNote</note><price>1.80</price></meal>')

    assert ET.tostring(expected) == ET.tostring(meal.to_xml())
