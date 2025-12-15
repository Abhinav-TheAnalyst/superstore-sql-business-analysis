**Environment & Requirements**

This short note explains the Python environment, why the packages in `requirements.txt` are chosen, and how to set things up on Windows PowerShell.

- **Python version:** 3.8+ recommended.
- **Create and activate venv (PowerShell):**

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

- **Install packages:**

```powershell
pip install -r requirements.txt
```

- **Why these packages:**
  - `pandas`: core data loading and cleaning.
  - `numpy`: numeric helpers used by pandas.
  - `pyarrow`: optional fast parquet/io helpers (useful if saving parquet later).
  - `sqlalchemy`: optional helper if you want to load CSV into a local SQL database via Python.

- **Optional plotting extras:**
  - `plotly` (for interactive visuals used in the notebook). Install with `pip install plotly`.
  - `kaleido` (to export plotly figures to PNG): `pip install kaleido`.

- **Troubleshooting:**
  - If `scripts/clean_data.py` fails due to date parsing, ensure your CSV has `Order Date` and `Ship Date` columns spelled the same as the original file.
  - If the notebook cannot display Plotly figures, try running `pip install notebook plotly` and open the notebook with `jupyter notebook`.

---

If you want, I can add a `requirements-dev.txt` that includes `jupyter`, `plotly`, and `kaleido` so the main `requirements.txt` remains minimal.
