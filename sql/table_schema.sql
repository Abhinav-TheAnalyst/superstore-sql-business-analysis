-- Suggested table schema for importing the cleaned CSV into a relational DB.
-- Adapt types to your engine (Postgres, MySQL, SQLite).

CREATE TABLE superstore (
    order_id TEXT PRIMARY KEY,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    region TEXT,
    state TEXT,
    city TEXT,
    postal_code INTEGER,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales NUMERIC,
    quantity INTEGER,
    discount NUMERIC,
    profit NUMERIC,
    order_year INTEGER,
    order_month TEXT
);

-- Indexes to speed up typical queries
CREATE INDEX idx_superstore_region ON superstore(region);
CREATE INDEX idx_superstore_category ON superstore(category);
CREATE INDEX idx_superstore_order_date ON superstore(order_date);