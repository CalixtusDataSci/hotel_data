Project: Hotel Booking — data cleaning

Author: Nwaeke Calixtus, Esq

Contents
- `scripts/clean_data.py`: CLI script that reads the original CSV, applies conservative cleaning (parse dates, coerce numeric fields, normalize strings, remove zero-guest rows, drop duplicates), and writes a cleaned CSV.
- `requirements.txt`: minimal dependency list.

Quick start

1) Create a Python virtual environment and install requirements

```bash
python -m venv .venv
.venv\\Scripts\\activate    # on Windows
pip install -r requirements.txt
```

2) Run the cleaner (paths relative to repository root)

```bash
python scripts/clean_data.py --input hotels.csv --output data/cleaned_hotels.csv
```

Next steps (suggested)
- Review or convert `Untitled.ipynb` into a documented analysis notebook or create `notebooks/data_cleaning.ipynb` that calls `scripts/clean_data.py` and includes exploratory plots and validation checks.
- Add lightweight unit tests for the `clean()` function to lock expected behaviors.
