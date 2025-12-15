"""Lightweight cleaning script for the Superstore CSV.

Usage (PowerShell):
    python scripts\\clean_data.py --input "data/raw/Superstore.csv" --output "data/processed/superstore_cleaned.csv"

The script performs small, well-documented cleaning steps so the CSV is ready for SQL analysis.
"""
import argparse
import os
import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df = df.rename(columns=lambda c: c.strip().lower().replace(' ', '_'))

    # Parse dates
    for col in ('order_date', 'ship_date'):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Trim string columns
    obj_cols = df.select_dtypes(['object']).columns
    df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())

    # Ensure numeric columns
    for col in ('sales', 'profit', 'discount', 'quantity'):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing postal codes with 0 and ensure int where possible
    if 'postal_code' in df.columns:
        df['postal_code'] = pd.to_numeric(df['postal_code'], errors='coerce').fillna(0).astype(int)

    # Drop rows with no order id
    if 'order_id' in df.columns:
        df = df[df['order_id'].notna()]

    # Add derived columns useful for analysis
    if 'order_date' in df.columns:
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.to_period('M').astype(str)

    return df


def main():
    parser = argparse.ArgumentParser(description='Clean Superstore CSV to analysis-ready CSV')
    parser.add_argument('--input', required=True, help='path to raw Superstore.csv')
    parser.add_argument('--output', required=True, help='path for cleaned CSV')
    args = parser.parse_args()

    inp = args.input
    out = args.output

    if not os.path.exists(inp):
        raise SystemExit(f"Input file not found: {inp}")

    os.makedirs(os.path.dirname(out), exist_ok=True)

    # Try common encodings with a safe fallback for files that are not UTF-8
    encodings_to_try = ('utf-8', 'latin1', 'cp1252')
    last_err = None
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(inp, encoding=enc, low_memory=False)
            break
        except Exception as e:
            last_err = e
            df = None
    if df is None:
        raise SystemExit(f"Failed to read input CSV with tried encodings {encodings_to_try}: {last_err}")
    df = clean(df)

    # Keep a sensible column order (common fields first)
    cols = [c for c in [
        'order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_id', 'customer_name',
        'segment', 'country', 'region', 'state', 'city', 'postal_code',
        'product_id', 'category', 'sub_category', 'product_name',
        'sales', 'quantity', 'discount', 'profit', 'order_year', 'order_month'
    ] if c in df.columns]

    df.to_csv(out, index=False, columns=cols)
    print(f"Wrote cleaned data to: {out}")


if __name__ == '__main__':
    main()
