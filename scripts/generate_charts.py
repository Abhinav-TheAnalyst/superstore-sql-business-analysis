import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_csv_with_fallback(path):
    encodings = ["utf-8", "latin1", "cp1252"]
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    # last attempt without specifying encoding
    return pd.read_csv(path)


def ensure_datetime(df, col_candidates):
    for c in col_candidates:
        if c in df.columns:
            try:
                df[c] = pd.to_datetime(df[c], errors='coerce')
                return c
            except Exception:
                continue
    return None


def make_profit_by_region(df, out_path):
    if 'Region' not in df.columns or 'Profit' not in df.columns:
        return False
    agg = df.groupby('Region', dropna=False)['Profit'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    sns.barplot(x=agg.index, y=agg.values, palette='muted')
    plt.title('Total Profit by Region')
    plt.ylabel('Profit')
    plt.xlabel('Region')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_discount_vs_profit(df, out_path):
    if 'Discount' not in df.columns or 'Profit' not in df.columns:
        return False
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x='Discount', y='Profit', alpha=0.6)
    sns.regplot(data=df, x='Discount', y='Profit', scatter=False, color='red', lowess=True)
    plt.title('Discount vs Profit')
    plt.ylabel('Profit')
    plt.xlabel('Discount')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_top_customers(df, out_path, top_n=10):
    cust_col = None
    for name in ['Customer Name', 'Customer', 'CustomerName', 'Customer_Name']:
        if name in df.columns:
            cust_col = name
            break
    if cust_col is None or 'Profit' not in df.columns:
        return False
    agg = df.groupby(cust_col)['Profit'].sum().sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(8,6))
    sns.barplot(x=agg.values, y=agg.index, palette='deep')
    plt.title(f'Top {top_n} Customers by Profit')
    plt.xlabel('Profit')
    plt.ylabel('Customer')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def main():
    parser = argparse.ArgumentParser(description='Generate dashboard PNGs from Superstore CSV')
    parser.add_argument('input_csv', help='Path to input CSV')
    parser.add_argument('out_dir', help='Output directory for PNGs')
    args = parser.parse_args()

    inp = args.input_csv
    out = args.out_dir
    os.makedirs(out, exist_ok=True)

    print(f'Reading {inp} ...')
    df = read_csv_with_fallback(inp)
    # common cleaning: strip column names
    df.columns = [c.strip() for c in df.columns]
    # coerce numeric columns
    for col in ['Profit', 'Sales', 'Discount', 'Quantity']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # ensure order date
    ensure_datetime(df, ['Order Date', 'OrderDate', 'Order_Date'])

    results = []
    p1 = os.path.join(out, 'profit_by_region.png')
    ok = make_profit_by_region(df, p1)
    results.append(('profit_by_region', ok, p1))

    p2 = os.path.join(out, 'discount_vs_profit.png')
    ok = make_discount_vs_profit(df, p2)
    results.append(('discount_vs_profit', ok, p2))

    p3 = os.path.join(out, 'top_customers.png')
    ok = make_top_customers(df, p3)
    results.append(('top_customers', ok, p3))

    for name, ok, path in results:
        if ok:
            print(f'WROTE: {path}')
        else:
            print(f'SKIPPED: {name} (missing columns)')


if __name__ == '__main__':
    main()
