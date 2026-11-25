from scripts.transforms import round_profit


def test_round_profit(spark):
    df = spark.createDataFrame([(1, 10.126), (2, -3.334), (3, 5.0), (4, None)],
                               "row_id int, profit double")
    out = round_profit(df)

    assert [r.profit for r in out.orderBy("row_id").collect()] == [10.13, -3.33, 5.0, None]
    assert out.count() == df.count()                 # no rows lost
    assert out.columns == df.columns                 # no columns added or dropped