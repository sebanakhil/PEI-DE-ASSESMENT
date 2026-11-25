# PEI Data Engineering Assessment

PySpark pipeline that turns the raw sales files (orders, customers, products) into cleaned, enriched and aggregated Delta tables using a medallion layout (Landing → Bronze → Silver → Gold), with SQL aggregates and unit tests.

## Architecture

```
Order.json    ─► bronze.orders    ─► silver.orders    ─┐
Customer.xlsx ─► bronze.customer  ─► silver.customer  ─┼─► gold.orders_enriched ─► gold.profit_summary ─► SQL aggregates
Product.csv   ─► bronze.products  ─► silver.products  ─┘
                                     silver.product_classification (lookup)
LANDING[./data/]           BRONZE                SILVER                          GOLD
```

| Layer | Contents |
|---|---|
| Landing | Source files in the /data folder of the repo |
| Bronze | Source data as-is (all strings), snake_case column names, `_source` and `_ingested_at` lineage columns |
| Silver | Cleaned and typed data: customer names and phones cleaned, dates parsed, product classification lookup |
| Gold | Enriched orders (Task 3) and profit aggregate (Task 4) |

## Repository structure

```
PEI-Assessment/
├── 00_Data_Exploration     # profiling of the source files and key findings
├── 01_pipeline             # end-to-end pipeline, Tasks 1–5
├── 02_unit_tests                # runs the pytest suite
├── scripts/
│   ├── cleaning.py         # clean_cust_name, clean_phone
│   ├── transforms.py       # round_profit
│   ├── utils.py            # rename (snake_case columns), to_bronze
│   └── dq.py               # dq_check_schema, dq_check_rows
└── tests/
│   ├── conftest.py         # spark fixture
│   ├── test_cleaning.py
│   ├── test_transforms.py
│   ├── test_utils.py
│   └── test_dq.py
└── data/
│   ├── Customer.xlsx
│   ├── Orders.json
│   └── Products.csv
```

## How to run

1. Upload `Order.json`, `Customer.xlsx` and `Product.csv` to the volume `/Volumes/DE_ASSESSMENT/LANDING/input` (the first cells of `01_pipeline` create the catalog, schemas and volume).
2. Run `01_pipeline` top to bottom. It builds all Bronze, Silver and Gold tables and runs the Task 5 SQL queries.
3. Run `02_tests` to execute the unit tests (`pytest` is installed in the first cell).

`00_Data_Exploration` is optional and documents how the cleaning rules were derived.



## Assumptions

1. Bronze keeps the source data unchanged apart from column names.
2. Invalid phone numbers are set to null.
3. Orders are classified through the `product_id` prefix, not by joining on `product_id`. This avoids duplicating order lines for the 33 duplicated product IDs.
4. Orders are left-joined, so no order is dropped.
5. `order_year` is derived from `order_date`.
6. Profit is rounded to 2 dp in the enriched table, and aggregates sum the rounded values.
7. Expected row counts (orders 9,994; customers 793; products 1,851) are fixed for this dataset and checked on load.

