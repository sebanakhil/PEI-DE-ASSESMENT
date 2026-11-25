# tests/test_cleaning.py
import pytest
from pyspark.sql import functions as F
from scripts.cleaning import clean_cust_name, clean_phone     # adjust to your module path


def check(spark, fn, cases):
    """Apply fn to each input; fail with every mismatch listed."""
    df = spark.createDataFrame(cases, "inp string, exp string")
    bad = (df.withColumn("got", fn)
             .filter(~F.col("got").eqNullSafe(F.col("exp")))      # null == null counts as equal
             .collect())
    assert not bad, "\n".join(f"{r.inp!r}: expected {r.exp!r}, got {r.got!r}" for r in bad)


# ── clean_cust_name ─────────────────────────────────────────────────────
def test_name_valid_unchanged(spark):
    check(spark, clean_cust_name("inp"), [
        ("John Smith",       "John Smith"),
        ("Mary-Ann O'Neil",  "Mary-Ann O'Neil"),     # hyphen and apostrophe kept
    ])

def test_name_removes_junk(spark):
    check(spark, clean_cust_name("inp"), [
        ("John123",          "John"),
        ("J0hn Sm1th",       "Jhn Smth"),
        ("Bob (Jr.)",        "Bob Jr"),
        ("Anna_Lee!",        "AnnaLee"),
    ])

def test_name_whitespace(spark):
    check(spark, clean_cust_name("inp"), [
        ("  John   Smith  ", "John Smith"),          # trim + collapse
        ("John 9 Smith",     "John Smith"),          # gap left by removed digit collapsed
    ])

def test_name_null_stays_null(spark):
    check(spark, clean_cust_name("inp"), [(None, None)])

def test_name_only_junk_becomes_empty(spark):
    # Documents current behaviour: returns "" not null
    check(spark, clean_cust_name("inp"), [("@#$123", "")])


# ── clean_phone ─────────────────────────────────────────────────────────
def test_phone_formats(spark):
    check(spark, clean_phone(F.col("inp")), [
        ("4155550123",          "4155550123"),
        ("415-555-0123",        "4155550123"),
        ("(415) 555-0123",      "4155550123"),
        ("415.555.0123",        "4155550123"),
    ])

def test_phone_strips_001(spark):
    check(spark, clean_phone(F.col("inp")), [
        ("001-415-555-0123",    "4155550123"),
        ("0014155550123",       "4155550123"),
    ])

def test_phone_drops_extension(spark):
    check(spark, clean_phone(F.col("inp")), [
        ("415-555-0123x2345",   "4155550123"),
        ("415-555-0123 x99",    "4155550123"),
    ])

def test_phone_invalid_becomes_null(spark):
    check(spark, clean_phone(F.col("inp")), [
        ("#ERROR!",             None),
        ("555-0123",            None),       # 7 digits
        ("415-555-01234",       None),       # 11 digits
        ("",                    None),
        (None,                  None),
    ])


# ── Known gaps: documented, expected to fail until the function is improved ──
@pytest.mark.parametrize("inp, exp", [
    pytest.param("415-555-0123X2345", "4155550123", marks=pytest.mark.xfail(reason="uppercase X not split")),
    pytest.param("+1-415-555-0123",   "4155550123", marks=pytest.mark.xfail(reason="+1 country code not stripped")),
    pytest.param(" 001-415-555-0123", "4155550123", marks=pytest.mark.xfail(reason="leading space blocks ^001")),
])
def test_phone_known_gaps(spark, inp, exp):
    check(spark, clean_phone(F.col("inp")), [(inp, exp)])

@pytest.mark.xfail(reason="accented letters removed by a-zA-Z")
def test_name_accents(spark):
    check(spark, clean_cust_name("inp"), [("José García", "José García")])