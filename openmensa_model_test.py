import lxml.etree as ET

from openmensa_model import Price, Role


def test_price_sets_default_role():
    price = Price(123)
    assert price.role == Role.OTHERS


def test_price_xml():
    price = Price(100)

    expected_xml = ET.fromstring('<price role="other">1.00</price>')
    assert ET.tostring(price.to_xml()) == ET.tostring(expected_xml)
