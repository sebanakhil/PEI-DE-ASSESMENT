from pyspark.sql import DataFrame, functions as F


def round_profit(df: DataFrame, col: str = "profit", scale: int = 2) -> DataFrame:
    """Round the profit column to `scale` decimal places (Task 3)."""
    return df.withColumn(col, F.round(F.col(col), scale))