from pyspark.sql import functions as F

def clean_cust_name(column):
    """Cleans customer name column, removing special characters and extra spaces.
    Returns a new column."""
    c = F.regexp_replace(F.col(column), r"[^a-zA-Z' -]", "")
    return F.trim(F.regexp_replace(c, r"\s+", " "))    # collapse doubles, trim ends



def clean_phone(c):
    """Cleans phone number column, removing special characters and extra spaces.
    Returns a new column"""
    s = F.regexp_replace(c, r"^001", "")              # 1. strip leading 001
    s = F.split(s, "x").getItem(0)                     # 2. keep part before x (extension)
    d = F.regexp_replace(s, r"\D", "")                 # 3. digits only
    return F.when(F.length(d) == 10, d)                # 4. valid → 10 digits, else null