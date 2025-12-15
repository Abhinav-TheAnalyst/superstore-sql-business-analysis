import os
import sys
import argparse
import json
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


def find_col(df, candidates):
    """Return the first matching column name from candidates (case-insensitive) or None."""
    cols = {c.strip().lower(): c for c in df.columns}
    for cand in candidates:
        key = cand.strip().lower()
        if key in cols:
            return cols[key]
    return None


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
    region_col = find_col(df, ['Region'])
    profit_col = find_col(df, ['Profit'])
    if region_col is None or profit_col is None:
        return False
    agg = df.groupby(region_col, dropna=False)[profit_col].sum().sort_values(ascending=False)
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
    discount_col = find_col(df, ['Discount'])
    profit_col = find_col(df, ['Profit'])
    if discount_col is None or profit_col is None:
        return False
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x=discount_col, y=profit_col, alpha=0.6)
    try:
        sns.regplot(data=df, x=discount_col, y=profit_col, scatter=False, color='red', lowess=True)
    except Exception:
        pass
    plt.title('Discount vs Profit')
    plt.ylabel('Profit')
    plt.xlabel('Discount')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_top_customers(df, out_path, top_n=10):
    cust_col = find_col(df, ['Customer Name', 'Customer', 'CustomerName', 'Customer_Name'])
    profit_col = find_col(df, ['Profit'])
    if cust_col is None or profit_col is None:
        return False
    agg = df.groupby(cust_col)[profit_col].sum().sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(8,6))
    sns.barplot(x=agg.values, y=agg.index, palette='deep')
    plt.title(f'Top {top_n} Customers by Profit')
    plt.xlabel('Profit')
    plt.ylabel('Customer')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_sales_by_category(df, out_path):
    cat = find_col(df, ['Category'])
    sales = find_col(df, ['Sales'])
    if cat is None or sales is None:
        return False
    agg = df.groupby(cat)[sales].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    sns.barplot(x=agg.index, y=agg.values, palette='pastel')
    plt.title('Sales by Category')
    plt.ylabel('Sales')
    plt.xlabel('Category')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_monthly_sales_trend(df, out_path):
    date_col = find_col(df, ['Order Date', 'OrderDate', 'Order_Date'])
    sales = find_col(df, ['Sales'])
    if date_col is None or sales is None:
        return False
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    ts = df.set_index(date_col).resample('M')[sales].sum()
    plt.figure(figsize=(10,5))
    ts.plot(marker='o')
    plt.title('Monthly Sales Trend')
    plt.ylabel('Sales')
    plt.xlabel('Month')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_top_products(df, out_path, top_n=10):
    prod = find_col(df, ['Product Name', 'Product', 'Product_Name'])
    sales = find_col(df, ['Sales'])
    if prod is None or sales is None:
        return False
    agg = df.groupby(prod)[sales].sum().sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(8,6))
    sns.barplot(x=agg.values, y=agg.index, palette='muted')
    plt.title(f'Top {top_n} Products by Sales')
    plt.xlabel('Sales')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_discount_distribution(df, out_path):
    discount = find_col(df, ['Discount'])
    if discount is None:
        return False
    plt.figure(figsize=(8,5))
    sns.histplot(df[discount].dropna(), bins=30, kde=True)
    plt.title('Discount Distribution')
    plt.xlabel('Discount')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def make_correlation_heatmap(df, out_path):
    cols = []
    for c in ['Sales', 'Profit', 'Discount', 'Quantity']:
        col = find_col(df, [c])
        if col:
            cols.append(col)
    if len(cols) < 2:
        return False
    corr = df[cols].corr()
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return True


def compute_kpis(df):
    sales = find_col(df, ['Sales'])
    profit = find_col(df, ['Profit'])
    region = find_col(df, ['Region'])
    out = {}
    if sales:
        out['total_sales'] = float(df[sales].dropna().sum())
    if profit:
        out['total_profit'] = float(df[profit].dropna().sum())
    if region and profit:
        top_region = df.groupby(region)[profit].sum().idxmax()
        out['top_region_by_profit'] = str(top_region)
    # average discount and avg profit per order
    discount_col = find_col(df, ['Discount'])
    if discount_col:
        out['avg_discount'] = float(df[discount_col].dropna().mean())

    if profit:
        out['avg_profit_per_order'] = float(df[profit].dropna().mean())

    # top 3 regions by profit
    if region and profit:
        top_regions = df.groupby(region)[profit].sum().sort_values(ascending=False).head(3).index.tolist()
        out['top_3_regions_by_profit'] = [str(x) for x in top_regions]

    # top 10 customers by profit
    cust_col = find_col(df, ['Customer Name', 'Customer', 'CustomerName', 'Customer_Name'])
    if cust_col and profit:
        top_customers = df.groupby(cust_col)[profit].sum().sort_values(ascending=False).head(10)
        out['top_10_customers_by_profit'] = [str(x) for x in top_customers.index.tolist()]

    # discount threshold where average profit becomes negative (binned)
    if discount_col and profit:
        try:
            bins = pd.cut(df[discount_col].dropna(), bins=20)
            grp = df.dropna(subset=[discount_col, profit]).groupby(bins)[profit].mean()
            neg_bins = grp[grp < 0]
            if not neg_bins.empty:
                # choose the left edge of first negative bin as threshold
                first_bin = neg_bins.index[0]
                threshold = float(first_bin.left)
                out['discount_threshold_loss'] = threshold
        except Exception:
            pass

    return out


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
    chart_defs = [
        ('profit_by_region.png', make_profit_by_region),
        ('discount_vs_profit.png', make_discount_vs_profit),
        ('top_customers.png', make_top_customers),
        ('sales_by_category.png', make_sales_by_category),
        ('monthly_sales_trend.png', make_monthly_sales_trend),
        ('top_products.png', make_top_products),
        ('discount_distribution.png', make_discount_distribution),
        ('correlation_heatmap.png', make_correlation_heatmap),
    ]

    for fname, func in chart_defs:
        path = os.path.join(out, fname)
        try:
            ok = func(df, path) if func.__code__.co_argcount == 2 else func(df, path)
        except TypeError:
            ok = func(df, path)
        results.append((fname, ok, path))

    for name, ok, path in results:
        if ok:
            print(f'WROTE: {path}')
        else:
            print(f'SKIPPED: {name} (missing columns)')

    # compute KPIs
    kpis = compute_kpis(df)
    kpi_path = os.path.join(out, 'kpis.json')
    with open(kpi_path, 'w', encoding='utf-8') as f:
        json.dump(kpis, f, indent=2)
    print(f'WROTE: {kpi_path}')


if __name__ == '__main__':
    main()
