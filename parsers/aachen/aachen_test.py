from bs4 import BeautifulSoup as parse

from parsers.aachen.aachen import parse_legend


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
