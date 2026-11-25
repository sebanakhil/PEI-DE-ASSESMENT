
def dq_check_schema(actual_columns , expected_columns):
    """Checks if the schema of the actual dataframe matches the expected schema"""
    actual_columns = set(actual_columns) -set(["_rescued_data"])
    if set(actual_columns)  != set(expected_columns):
        raise Exception(f"Schema does not match expected schema. Actual: {actual_columns}, Expected: {expected_columns}")
    else:
        print("Schema valid")

def dq_check_rows(actual, expected):
    """Checks if the number of rows in the actual dataframe matches the expected number of rows"""
    if actual != expected:
        raise Exception(f"Number of rows does not match. Actual: {actual}, Expected: {expected}")
    else:
        print("Number of rows valid")