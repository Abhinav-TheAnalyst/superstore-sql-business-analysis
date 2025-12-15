This folder contains a set of SQL scripts to reproduce the analysis in a step-by-step manner.

Run them in order: `01_data_cleaning.sql` → `02_sales_overview.sql` → ... → `07_final_insights.sql`.

Notes:
- SQL syntax may need small adjustments depending on your RDBMS (Postgres, MySQL, SQLite).
- Use `sql/table_schema.sql` to create the table, then import `data/processed/superstore_cleaned.csv`.
