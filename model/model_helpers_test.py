import pytest

from model.model_helpers import PricesBuilder
from model.openmensa_model import Prices


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
