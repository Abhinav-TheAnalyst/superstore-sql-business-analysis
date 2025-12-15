import os
import json
import pandas as pd

def main():
    inp = os.path.join('data', 'raw', 'Sample - Superstore.csv')
    out = os.path.join('dashboard', 'screenshots', 'products_negative_profit.json')
    if not os.path.exists(inp):
        print('Missing input:', inp)
        return
    df = pd.read_csv(inp, encoding='latin1')
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    prod_col = None
    for c in ['Product Name', 'Product', 'Product_Name']:
        if c in df.columns:
            prod_col = c
            break
    sales_col = None
    profit_col = None
    for c in ['Sales']:
        if c in df.columns:
            sales_col = c
    for c in ['Profit']:
        if c in df.columns:
            profit_col = c
    if prod_col is None or sales_col is None or profit_col is None:
        print('Required columns missing')
        return
    agg = df.groupby(prod_col).agg({sales_col: 'sum', profit_col: 'sum'})
    neg = agg[agg[profit_col] < 0].sort_values(by=sales_col, ascending=False).head(10)
    records = []
    for idx, row in neg.iterrows():
        records.append({'product': str(idx), 'sales': float(row[sales_col]), 'profit': float(row[profit_col])})
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    print('WROTE', out)

if __name__ == '__main__':
    main()
