# tests/test_dq.py
import pytest
from scripts.dq import dq_check_schema, dq_check_rows      # adjust to your module path


# ── dq_check_schema ─────────────────────────────────────────────────────
def test_schema_match_passes(capsys):
    dq_check_schema(["a", "b", "c"], ["a", "b", "c"])
    assert "Schema valid" in capsys.readouterr().out


def test_schema_order_does_not_matter():
    dq_check_schema(["c", "a", "b"], ["a", "b", "c"])           # no exception = pass


def test_schema_ignores_rescued_data():
    dq_check_schema(["a", "b", "_rescued_data"], ["a", "b"])


def test_schema_missing_column_raises():
    with pytest.raises(Exception, match="Schema does not match"):
        dq_check_schema(["a", "b"], ["a", "b", "c"])


def test_schema_extra_column_raises():
    with pytest.raises(Exception, match="Schema does not match"):
        dq_check_schema(["a", "b", "c", "d"], ["a", "b", "c"])


def test_schema_renamed_column_raises():
    with pytest.raises(Exception):
        dq_check_schema(["a", "B"], ["a", "b"])                 # case-sensitive


def test_schema_on_real_dataframe(spark):
    df = spark.createDataFrame([(1, "x")], "customer_id int, customer_name string")
    dq_check_schema(df.columns, ["customer_id", "customer_name"])


# ── dq_check_rows ───────────────────────────────────────────────────────
def test_rows_match_passes(capsys):
    dq_check_rows(793, 793)
    assert "Number of rows valid" in capsys.readouterr().out


@pytest.mark.parametrize("actual, expected", [(792, 793), (794, 793), (0, 793)])
def test_rows_mismatch_raises(actual, expected):
    with pytest.raises(Exception, match=f"Actual: {actual}, Expected: {expected}"):
        dq_check_rows(actual, expected)


def test_rows_on_real_dataframe(spark):
    df = spark.range(5)
    dq_check_rows(df.count(), 5)