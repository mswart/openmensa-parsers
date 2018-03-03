import pytest

from model.model_helpers import NotesBuilder, PricesBuilder, PricesCategoryBuilder
from model.openmensa_model import Category, Meal, Notes, Prices


# PricesBuilder
def test_given_all_roles_then_builds_prices():
    builder = PricesBuilder(other=0, pupils=240, students=120, employees=1)
    prices = builder.build_prices(100)

    assert prices == Prices(other=100, pupils=340, students=220, employees=101)


def test_given_no_roles_then_raises():
    with pytest.raises(ValueError):
        PricesBuilder()


def test_given_some_roles_then_builds_prices_with_those_roles_only():
    builder = PricesBuilder(pupils=123, employees=321)
    prices = builder.build_prices(100)

    assert prices == Prices(pupils=223, employees=421)


# NotesBuilder
def test_given_legend_and_keys_then_builds_notes():
    legend = {
        '1': 'First',
        '2': 'Second',
        '3': 'Third',
    }
    builder = NotesBuilder(legend)
    note_keys = ['1', '3']
    notes = builder.build_notes(note_keys)

    assert notes == Notes(['First', 'Third'])


def test_given_keys_not_in_legend_then_keeps_them_by_default():
    legend = {'A': 'map me'}
    builder = NotesBuilder(legend)
    note_keys = ['keep me', 'A']
    notes = builder.build_notes(note_keys)

    assert notes == Notes(['keep me', 'map me'])


def test_given_flag_to_ignore_keys_not_found_then_ignores_them():
    legend = {'1': 'map me'}
    builder = NotesBuilder(legend, ignore_not_found=True)
    note_keys = ['ignore me', '1']
    notes = builder.build_notes(note_keys)

    assert notes == Notes(['map me'])


# PricesCategoryBuilder
def test_given_prices_then_replaces_prices_in_meals():
    prices = Prices(other=100)
    builder = PricesCategoryBuilder(prices)

    meals = [Meal('First Meal'), Meal('Second Meal')]
    category = builder.build_category('Test Category', meals)

    assert category == Category('Test Category', meals=[
        Meal('First Meal', prices=prices),
        Meal('Second Meal', prices=prices)
    ])


def test_given_meal_with_own_prices_then_raises_error_mentioning_flag():
    prices = Prices(other=100)
    builder = PricesCategoryBuilder(prices)

    meals = [Meal('Meal with own price', prices=Prices(other=200))]
    with pytest.raises(ValueError) as e:
        builder.build_category('Test Category', meals)
        print(e)
    assert 'overwrite_existing' in str(e.value)


def test_given_override_flag_and_meal_with_own_prices_then_overwrites():
    prices = Prices(other=100)
    builder = PricesCategoryBuilder(prices, overwrite_existing=True)

    meals = [Meal('Overwrite my prices', prices=Prices(pupils=200))]
    category = builder.build_category('Test Category', meals)

    assert category == Category('Test Category', meals=[
        Meal('Overwrite my prices', prices=prices),
    ])
