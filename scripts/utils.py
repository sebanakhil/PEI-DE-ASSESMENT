import re
from pyspark.sql import functions as F

def rename(columns):
    """Rename columns to snake case"""
    return [re.sub(r"[^A-Za-z0-9]+","_",column).lower() for column in columns]


def to_bronze(df, table, source):
    """Write to bronze table"""
    final_df = (df.withColumn("_source",F.lit(source))
                   .withColumn("_ingested_at",F.current_timestamp())
    )

    (final_df.write
            .mode('overwrite')
            .option('overwriteSchema', True)
            .saveAsTable(table)
    )
    return f"Successfully written to table {table}"