from itertools import zip_longest

import lxml.etree as ET

from openmensa_model import Meal, Notes, Prices


def test_meal_xml():
    meal = Meal('Test Meal', Prices(134), Notes(['Test note']))
    expected_xml = ET.fromstring(
        '<meal>'
        '<name>Test Meal</name>'
        '<note>Test note</note>'
        '<price role="other">1.34</price>'
        '</meal>'
    )
    assert ET.tostring(meal.to_xml()) == ET.tostring(expected_xml)


def test_prices_sets_default_role():
    prices = Prices(123)
    assert prices.prices['other'] == 123


def test_prices_xml():
    prices = Prices(123, students=100, employees=234)

    expected_xmls = [
        ET.fromstring('<price role="employees">2.34</price>'),
        ET.fromstring('<price role="other">1.23</price>'),
        ET.fromstring('<price role="students">1.00</price>'),
    ]

    for price_xml, expected_xml in zip_longest(prices.to_xml(), expected_xmls):
        assert ET.tostring(price_xml) == ET.tostring(expected_xml)


def test_notes_xml():
    notes = Notes(['Second note', 'First note'])
    expected_xmls = [
        ET.fromstring('<note>First note</note>'),
        ET.fromstring('<note>Second note</note>'),
    ]
    for note_xml, expected_xml in zip_longest(notes.to_xml(), expected_xmls):
        assert ET.tostring(note_xml) == ET.tostring(expected_xml)
