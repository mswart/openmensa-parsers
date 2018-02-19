from itertools import zip_longest

import lxml.etree as ET
import pytest

from openmensa_model import Category, Meal, Notes, Prices


def test_category_xml():
    category = Category('Test Category', [Meal('Test Meal')])
    expected_xml = ET.fromstring(
        '<category name="Test Category">'
        '<meal><name>Test Meal</name></meal>'
        '</category>'
    )
    assert ET.tostring(category.to_xml()) == ET.tostring(expected_xml)


def test_meal_sets_default_prices_and_notes():
    meal = Meal('Empty meal')
    assert meal.prices is None
    assert meal.notes == Notes()


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


def test_prices_raises_error_if_no_amount_set():
    with pytest.raises(ValueError):
        Prices()


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


def test_notes_sets_default_list():
    notes = Notes()
    assert notes.note_list == []


def test_notes_xml():
    notes = Notes(['Second note', 'First note'])
    expected_xmls = [
        ET.fromstring('<note>First note</note>'),
        ET.fromstring('<note>Second note</note>'),
    ]
    for note_xml, expected_xml in zip_longest(notes.to_xml(), expected_xmls):
        assert ET.tostring(note_xml) == ET.tostring(expected_xml)
