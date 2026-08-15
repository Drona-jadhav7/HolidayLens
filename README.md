
# HolidayLens

Generic tool for comparing official government holiday datasets with the Python `holidays` library.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
holidaylens compare --country IN --subdiv MH --year 2026 --official data/india/mh/2026.csv
holidaylens compare --country IN --subdiv PB --year 2026 --official data/india/pb/2026.csv
holidaylens compare --country IN --subdiv TG --year 2026 --official data/india/tg/2026.csv
```

Or:

```bash
python -m holiday_gap.cli compare --country IN --subdiv PB --year 2026 --official data/india/pb/2026.csv
```

## CSV format

```csv
date,name,type
2026-01-26,Republic Day,general
```

Quote names containing commas.

The comparator reports MATCH, REVIEW, MISSING, EXTRA and possible DATE MISMATCH.
It compares dates first and does not contain Maharashtra/Punjab-specific aliases.

The included datasets are working research examples. Verify them against authoritative
government notifications before using them as evidence for a contribution to `holidays`.
