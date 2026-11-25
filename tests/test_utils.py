# tests/test_utils.py
import pytest
from scripts.utils import rename ,re

@pytest.mark.parametrize("inp, expected", [
    ("Customer ID",    "customer_id"),     # space → _
    ("Sub-Category",   "sub_category"),    # hyphen → _
    ("Row  ID",        "row_id"),          # repeated separators collapse to one _
    ("Order.Date",     "order_date"),      # dot → _
    ("ship_mode",      "ship_mode"),       # already snake_case: unchanged
    ("PRODUCT_ID",     "product_id"),      # lower-cased
    ("Postal Code 2",  "postal_code_2"),   # digits kept
])
def test_rename_single(inp, expected):
    assert rename([inp]) == [expected]


def test_rename_keeps_order_and_length():
    cols = ["Order ID", "Customer ID", "Product ID"]
    assert rename(cols) == ["order_id", "customer_id", "product_id"]


def test_rename_empty_list():
    assert rename([]) == []

