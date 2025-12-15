Contributing & Running
=====================

Quick notes for reviewers and contributors.

1. Raw data

- The raw dataset is not committed. Place `Sample - Superstore.csv` in `data/raw/` locally to reproduce results.

2. Reproduce locally (minimal)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r archive_removed\requirements.txt
python archive_removed\scripts\clean_data.py --input "data/raw/Sample - Superstore.csv" --output "data/processed/superstore_cleaned.csv"
```

3. Run SQL

- Load `data/processed/superstore_cleaned.csv` into your preferred DB (SQLite, Postgres) and run the SQL files in `sql/` in order.

4. Notes

- If you want me to provide PNG charts or a small SQLite dump, I can generate those locally and add them to `dashboard/screenshots/` on request.
