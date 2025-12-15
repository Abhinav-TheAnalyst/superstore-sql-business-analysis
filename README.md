# Superstore — SQL & Data Analysis

Analysis of the "Sample – Superstore" dataset. This repository shows an SQL-first workflow, reproducible data cleaning, and static chart exports suitable for a portfolio or interview.

Author: Abhinav Verma — https://github.com/Abhinav-TheAnalyst

Table of contents
-----------------
- [Project overview](#project-overview)
- [Quick links](#quick-links)
- [Environment & Python version](#environment--python-version)
- [Quick start (reproduce visuals)](#quick-start-reproduce-visuals)
- [KPIs (from latest run)](#kpis-from-latest-run)
- [Visuals (embedded)](#visuals-embedded)
- [SQL + Notebook](#sql--notebook)
- [Files changed / added by last run](#files-changed--added-by-last-run)
- [Next improvements](#next-improvements)

Project overview
----------------
This repo provides:

- a lightweight cleaning & charting script (`scripts/generate_charts.py`)
- ordered SQL analysis scripts in `sql/` (01 → 07)
- a short exploratory notebook (`notebooks/analysis.ipynb`)
- a small dashboard folder with exported PNGs (`dashboard/screenshots/`)

Quick links
-----------
- Raw dataset (not committed): `data/raw/Sample - Superstore.csv`
- Chart outputs: `dashboard/screenshots/` (PNG + `kpis.json`)
- Chart generator: `scripts/generate_charts.py`
- Notebook: `notebooks/analysis.ipynb`
- Executive summary: `reports/executive_summary.md`

Environment & Python version
----------------------------
- Tested with: Python 3.10+ (the workspace used Python 3.14 during generation). Use Python 3.10 or newer.
- Primary libraries: `pandas`, `matplotlib`, `seaborn`, `nbconvert` (for notebook export).

Install (PowerShell)
--------------------
```powershell
cd "d:\python projects\git\superstore dataset"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas matplotlib seaborn jupyter nbconvert
```

Quick start — reproduce visuals
------------------------------
1. Place the dataset at `data/raw/Sample - Superstore.csv`.
2. Generate charts and KPIs:

```powershell
python scripts\generate_charts.py "data/raw/Sample - Superstore.csv" "dashboard/screenshots/"
```

3. Optionally execute the notebook and export HTML (may require additional packages):

```powershell
python -m nbconvert --to html --execute "notebooks/analysis.ipynb" --output "notebooks/analysis_executed.html"
```

KPIs (from the latest run)
-------------------------
The chart generator writes `dashboard/screenshots/kpis.json`. The latest values are:

- **Total sales:** `2,297,200.86`
- **Total profit:** `286,397.02`
- **Top region by profit:** `West`

Visuals (embedded)
-------------------
All visuals were created with `matplotlib` + `seaborn` and saved to `dashboard/screenshots/`.

- **Profit by region**

   ![Profit by region](dashboard/screenshots/profit_by_region.png)

   Short interpretation: The `West` region shows the highest aggregated profit in this dataset.

- **Discount vs Profit**

   ![Discount vs Profit](dashboard/screenshots/discount_vs_profit.png)

   Short interpretation: The scatter shows many low-profit observations at higher discount levels; a smoothed trend is included.

- **Top customers (by profit)**

   ![Top customers](dashboard/screenshots/top_customers.png)

   Short interpretation: A small set of customers contributes a large share of profit.

- **Sales by category**

   ![Sales by category](dashboard/screenshots/sales_by_category.png)

- **Monthly sales trend**

   ![Monthly sales trend](dashboard/screenshots/monthly_sales_trend.png)

- **Top products by sales**

   ![Top products](dashboard/screenshots/top_products.png)

- **Discount distribution**

   ![Discount distribution](dashboard/screenshots/discount_distribution.png)

- **Correlation heatmap**

   ![Correlation heatmap](dashboard/screenshots/correlation_heatmap.png)

SQL + Notebook
--------------
- SQL scripts are located in `sql/` and are intended to be run in order (01 → 07). They contain the main analysis logic and final insights.
- The notebook `notebooks/analysis.ipynb` provides a runnable exploratory analysis; an executed HTML export is available at `notebooks/analysis_executed.html`.

Files changed / added by the last run
-----------------------------------
- `scripts/generate_charts.py` — expanded chart generator (new/updated)
- `dashboard/screenshots/*.png` — generated visuals
- `dashboard/screenshots/kpis.json` — KPI summary for quick reference
- `notebooks/analysis_executed.html` — executed notebook export

Next improvements (optional)
---------------------------
- Add `requirements.txt` to pin versions for reproducibility (I can add this).
- Produce higher-resolution images (`dpi=300`) for presentation/print.
- Add Plotly interactive exports and save `.html` interactive charts (requires `plotly` + `kaleido`).
- Create a GitHub Actions workflow to regenerate visuals and export the notebook on push.

Contributing
------------
If you'd like me to apply any of the optional improvements above, reply with the feature you want (for example: `requirements`, `high-res`, `plotly`, or `ci`). I will implement and push the changes.

Contact
-------
Author: Abhinav Verma — https://github.com/Abhinav-TheAnalyst
