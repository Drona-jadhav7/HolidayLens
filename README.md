# HolidayLens

**HolidayLens** is a data-quality and verification tool for holiday calendars.

It compares an authoritative holiday reference dataset against the output of the Python [`holidays`](https://github.com/vacanza/python-holidays) library and identifies potential discrepancies such as:

* Missing holidays
* Extra holidays
* Different holiday names
* Different holiday dates
* Coverage gaps

HolidayLens is designed primarily as a **developer and research tool** for finding potential inaccuracies and missing coverage in holiday libraries.

It does **not** aim to become another holiday-calendar website or a replacement for the `holidays` library.

---

## Why HolidayLens?

Holiday calendars can vary between:

* countries
* states and provinces
* subdivisions
* years
* government notifications
* religious or regional observances

A holiday library may therefore contain an incorrect date, miss a holiday, include an outdated holiday, or use a different name from the authoritative source.

Finding these problems manually can be difficult.

HolidayLens provides a repeatable workflow:

```text
Authoritative source
        │
        ▼
Reference dataset
        │
        ▼
     HolidayLens
        │
        ├── Normalize names
        ├── Apply aliases
        ├── Match holidays
        └── Compare dates
        │
        ▼
Potential discrepancies
        │
        ▼
Human verification
        │
        ▼
Upstream issue / pull request
```

The important distinction is that HolidayLens identifies **potential discrepancies**. It does not automatically declare that the `holidays` library is wrong.

Every finding should be verified against an authoritative source before an upstream change is proposed.

---

# Features

HolidayLens currently provides:

### Reference data loading

Load holiday information from CSV files containing:

```text
date,name,category,source
```

Example:

```csv
date,name,category,source
2026-01-26,Republic Day,public,https://example.gov.in/holidays
2026-05-01,Maharashtra Day,public,https://example.gov.in/holidays
```

### `holidays` library integration

HolidayLens can load holiday data directly from the Python `holidays` package.

For example:

```python
load_holidays(
    "IN",
    subdiv="MH",
    years=2026,
)
```

### Name normalization

Holiday names can differ between sources.

HolidayLens normalizes names before comparison so that harmless naming differences do not automatically become false discrepancies.

### Alias support

Known equivalent names can be represented using canonical names and aliases.

### Comparison engine

HolidayLens currently identifies:

```text
MATCH
MISSING
EXTRA
NAME_MISMATCH
DATE_MISMATCH
```

### Coverage calculation

HolidayLens calculates the percentage of reference holidays that are matched exactly.

### Human-readable reports

The CLI produces reports suitable for manual investigation.

### JSON output

The same audit can be emitted as structured JSON for scripts, CI systems, and future integrations.

### Provenance

Reference records retain their source information so that detected discrepancies can be traced back to the source used for verification.

---

# Project status

HolidayLens is currently an early usable version.

The core workflow is implemented and tested.

Current test status:

```text
53 tests passing
```

The current version is intentionally focused on the core auditing workflow rather than a large collection of features.

---

# Installation

## Requirements

HolidayLens requires:

* Python 3.10 or newer
* the `holidays` Python package

Python 3.13 is also supported by the current development environment.

---

## Clone the repository

```bash
git clone https://github.com/Drona-jadhav7/HolidayLens.git
cd HolidayLens
```

---

## Create a virtual environment

### Windows / Git Bash

```bash
py -m venv .venv
source .venv/Scripts/activate
```

If your environment already provides the virtual environment, activate it with:

```bash
source .venv/Scripts/activate
```

---

## Install HolidayLens

For development:

```bash
py -m pip install -e .
```

Install development dependencies:

```bash
py -m pip install -e ".[dev]"
```

---

# Project structure

HolidayLens uses a `src` layout:

```text
HolidayLens/
├── data/
│   └── official/
│       └── IN/
│           ├── MH/
│           │   └── 2026.csv
│           ├── MP/
│           │   └── 2026.csv
│           └── ...
│
├── src/
│   └── holidaylens/
│       ├── __init__.py
│       ├── aliases.py
│       ├── compare.py
│       ├── library.py
│       ├── matching.py
│       ├── models.py
│       ├── normalization.py
│       ├── provenance.py
│       ├── report.py
│       ├── sources.py
│       └── cli.py
│
├── tests/
│   ├── test_compare.py
│   ├── test_library.py
│   ├── test_matching.py
│   ├── test_models.py
│   ├── test_provenance.py
│   ├── test_report.py
│   ├── test_sources.py
│   └── test_cli.py
│
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# Reference data

HolidayLens expects authoritative reference data in CSV format.

The minimum required columns are:

```text
date
name
```

Optional columns are:

```text
category
source
```

The complete recommended format is:

```csv
date,name,category,source
2026-01-26,Republic Day,public,https://example.gov.in/holidays
2026-05-01,Maharashtra Day,public,https://example.gov.in/holidays
```

## Field descriptions

### `date`

The holiday date in ISO format:

```text
YYYY-MM-DD
```

Example:

```text
2026-05-01
```

### `name`

The name used by the authoritative source.

Example:

```text
Maharashtra Day
```

### `category`

The type of holiday.

For example:

```text
public
```

If omitted, HolidayLens currently defaults it to:

```text
public
```

### `source`

The authoritative source from which the record was collected.

For example:

```text
https://example.gov.in/holidays
```

If omitted, HolidayLens currently defaults it to:

```text
unknown
```

For real auditing work, providing the source is strongly recommended.

---

# Reference-data directory

The current CLI convention is:

```text
data/official/<COUNTRY>/<SUBDIVISION>/<YEAR>.csv
```

For example:

```text
data/official/IN/MH/2026.csv
```

where:

* `IN` = India
* `MH` = Maharashtra
* `2026` = year

A country-wide reference dataset can use:

```text
data/official/IN/2026.csv
```

---

# Using the CLI

After installation, the main command is:

```bash
holidaylens
```

Show help:

```bash
holidaylens --help
```

Show audit help:

```bash
holidaylens audit --help
```

---

# Run an audit

For Maharashtra, India, in 2026:

```bash
holidaylens audit --country IN --subdivision MH --year 2026
```

The equivalent module invocation is:

```bash
py -m holidaylens.cli audit --country IN --subdivision MH --year 2026
```

---

# Example output

A typical report looks like:

```text
HolidayLens Report
────────────────────────────────
Country:       IN
Subdivision:   MH
Year:          2026

Reference:     24
Dataset:       21
Coverage:      66.7%

Matched:       16
Missing:       5
Extra:         2
Name mismatch: 2
Date mismatch: 1

Missing Holidays
────────────────────────────────
2026-02-15 | Mahashivratri
2026-05-01 | Buddha Pournima
2026-08-15 | Parsi New Year (Shahenshahi)
2026-09-14 | Ganesh Chaturthi
2026-11-10 | Diwali (Bali Pratipada)

Extra Holidays
────────────────────────────────
2026-03-04 | Holi
2026-09-04 | Janmashtami (Vaishnava)

Name Mismatches
────────────────────────────────
2026-03-03 | Holi (Second Day) ↔ Holi

Date Mismatches
────────────────────────────────
Bakri Id (Id-Uz-Zuha): 2026-05-28 → 2026-05-27
```

The exact output will depend on the reference data and the current version of the `holidays` library.

---

# JSON output

The CLI supports structured JSON output.

Use:

```bash
holidaylens audit \
  --country IN \
  --subdivision MH \
  --year 2026 \
  --format json
```

The output contains:

* country
* subdivision
* year
* reference count
* dataset count
* coverage
* summary counts
* individual comparison records

Example structure:

```json
{
  "country": "IN",
  "subdivision": "MH",
  "year": 2026,
  "reference_count": 24,
  "dataset_count": 21,
  "coverage": 66.7,
  "summary": {
    "matching": 16,
    "missing": 5,
    "extra": 2,
    "name_mismatch": 2,
    "date_mismatch": 1
  },
  "comparisons": [
    {
      "status": "match",
      "reference": {
        "date": "2026-01-26",
        "name": "Republic Day",
        "category": "public",
        "source": "government"
      },
      "dataset": {
        "date": "2026-01-26",
        "name": "Republic Day",
        "category": "public",
        "source": "holidays"
      }
    }
  ]
}
```

JSON output is useful for future automation and CI integration.

---

# Comparison statuses

HolidayLens currently uses five comparison statuses.

## `MATCH`

The reference and library contain equivalent holidays on the same date.

```text
Reference:
2026-01-26 — Republic Day

Library:
2026-01-26 — Republic Day

Result:
MATCH
```

---

## `MISSING`

A holiday exists in the reference dataset but HolidayLens cannot find a corresponding library holiday.

```text
Reference:
2026-09-14 — Ganesh Chaturthi

Library:
No corresponding holiday

Result:
MISSING
```

This can indicate a potential missing holiday in the library.

It must still be verified against the authoritative source and the library's intended scope.

---

## `EXTRA`

A holiday exists in the library but does not have a corresponding reference record.

```text
Reference:
No corresponding holiday

Library:
2026-03-04 — Holi

Result:
EXTRA
```

An extra result does not automatically mean the library is wrong.

The reference dataset might be incomplete, or the library might intentionally include an observance that the reference source does not.

---

## `NAME_MISMATCH`

The reference and library contain holidays on the same date but use different names.

```text
Reference:
2026-03-03 — Holi (Second Day)

Library:
2026-03-03 — Holi

Result:
NAME_MISMATCH
```

This can be a harmless naming difference, which is why HolidayLens includes normalization and aliases.

---

## `DATE_MISMATCH`

The reference and library contain holidays with equivalent names but different dates.

```text
Reference:
2026-05-28 — Bakri Id (Id-Uz-Zuha)

Library:
2026-05-27 — Bakri Id (Id-Uz-Zuha)

Result:
DATE_MISMATCH
```

Date mismatches are particularly important to investigate because movable holidays can change depending on official notifications, regional observance, or calendar calculations.

---

# How matching works

HolidayLens does not simply compare strings.

The comparison process is approximately:

```text
Reference holiday
       │
       ▼
Normalize name
       │
       ▼
Apply aliases / canonical names
       │
       ▼
Compare with library holidays
       │
       ├── same date + equivalent name
       │        ↓
       │      MATCH
       │
       ├── same date + different name
       │        ↓
       │   NAME_MISMATCH
       │
       ├── different date + equivalent name
       │        ↓
       │   DATE_MISMATCH
       │
       └── no corresponding holiday
                ↓
             MISSING
```

After reference records are processed, unused library records become `EXTRA`.

This approach attempts to distinguish meaningful discrepancies from simple naming differences.

---

# Coverage

HolidayLens calculates:

```text
exact matches
────────────── × 100
reference holidays
```

For example:

```text
16 exact matches
──────────────── × 100 = 66.7%
24 reference holidays
```

Coverage represents **exact reference-to-library matches**.

A high coverage percentage does not prove that a calendar is correct, and a lower percentage does not automatically prove that the library is incorrect.

Coverage is an investigation metric.

---

# Using a custom reference file

The CLI allows a reference CSV to be specified directly.

Example:

```bash
holidaylens audit \
  --country IN \
  --subdivision MH \
  --year 2026 \
  --reference ./my-reference.csv
```

This is useful when:

* testing a new source
* experimenting with a corrected dataset
* validating a government notification
* developing a new subdivision dataset

The custom reference file must follow the HolidayLens CSV format.

---

# Python API

HolidayLens can also be used directly from Python.

## Load reference data

```python
from holidaylens.sources import load_csv

reference = load_csv("data/official/IN/MH/2026.csv")
```

## Load the `holidays` library data

```python
from holidaylens.library import load_holidays

dataset = load_holidays(
    "IN",
    subdiv="MH",
    years=2026,
)
```

## Compare datasets

```python
from holidaylens.compare import compare

results = compare(reference, dataset)
```

## Generate a summary

```python
from holidaylens.report import summarize

summary = summarize(results)

print(summary)
```

Example:

```python
{
    "matching": 16,
    "missing": 5,
    "extra": 2,
    "name_mismatch": 2,
    "date_mismatch": 1,
}
```

## Generate a human-readable report

```python
from holidaylens.report import format_report

report = format_report(
    results,
    country="IN",
    subdivision="MH",
    year=2026,
    reference_count=len(reference),
    dataset_count=len(dataset),
)

print(report)
```

## Generate structured report data

```python
from holidaylens.report import report_data

data = report_data(
    results,
    country="IN",
    subdivision="MH",
    year=2026,
    reference_count=len(reference),
    dataset_count=len(dataset),
)
```

The returned object is JSON-serializable.

---

# Exit codes

The CLI uses exit codes so it can eventually be used in automated workflows.

## `0`

The audit completed and all results were exact matches.

```text
MATCH only
```

## `1`

The audit completed successfully, but one or more discrepancies were found.

For example:

```text
MISSING
EXTRA
NAME_MISMATCH
DATE_MISMATCH
```

This is useful for CI and automated auditing.

## `2`

The audit could not be performed because of an input or configuration problem.

Examples include:

* missing reference CSV
* invalid CSV
* invalid reference data
* invalid arguments

---

# Testing

HolidayLens uses `pytest`.

Run the complete test suite:

```bash
py -m pytest -q
```

The current development version has:

```text
53 tests passing
```

The test suite covers:

* models
* reference CSV loading
* metadata handling
* library loading
* normalization
* matching
* aliases
* comparison statuses
* coverage
* reports
* provenance
* CLI behavior
* JSON output

---

# Development

Install development dependencies:

```bash
py -m pip install -e ".[dev]"
```

Run tests:

```bash
py -m pytest -q
```

Run Ruff:

```bash
ruff check .
```

---

# Example: Finding a real upstream issue

One of the main purposes of HolidayLens is to help discover real issues in holiday libraries.

For example, suppose an authoritative government source says:

```text
2026-03-03 — Holi
```

while the library produces:

```text
2026-03-03 — Holi
2026-03-04 — Holi
```

HolidayLens can identify the additional library date:

```text
Extra Holidays
────────────────────────────────
2026-03-04 | Holi
```

The next step should **not** be to immediately modify the library.

Instead:

```text
1. Detect discrepancy
        ↓
2. Inspect authoritative source
        ↓
3. Confirm the applicable state/subdivision
        ↓
4. Confirm the year
        ↓
5. Determine whether the reference dataset is complete
        ↓
6. Reproduce the library behavior
        ↓
7. Decide whether it is actually an upstream bug
        ↓
8. Add a regression test
        ↓
9. Fix the upstream implementation
```

This distinction is central to HolidayLens.

---

# Relationship with `holidays`

HolidayLens is designed to complement the [`holidays`](https://github.com/vacanza/python-holidays) project.

The two projects have different purposes.

### `holidays`

Provides programmatic holiday calendars.

For example:

```python
import holidays

india = holidays.country_holidays(
    "IN",
    subdiv="MH",
    years=2026,
)
```

### HolidayLens

Audits holiday data quality.

It asks:

```text
Does the library output agree with an authoritative source?
```

HolidayLens therefore acts as a **verification and discovery layer** around the holiday library.

---

# What HolidayLens is not

HolidayLens is not intended to be:

* a replacement for `holidays`
* a consumer holiday-calendar website
* a general-purpose calendar application
* a source of truth by itself
* an automatic bug-fixing system

The authoritative source remains the basis for determining whether a discrepancy is valid.

---

# Important limitations

Holiday data can be complicated.

A discrepancy does not necessarily mean that one dataset is wrong.

Possible explanations include:

* different definitions of a public holiday
* regional observance
* optional holidays
* government notifications issued after a dataset was created
* lunar-calendar calculations
* substitute holidays
* holidays that apply only to certain institutions
* incomplete reference data
* differences in holiday naming
* changes to government notifications

Therefore:

> **HolidayLens findings should be treated as candidates for investigation, not automatic proof of an upstream bug.**

Human verification against authoritative sources remains an important part of the workflow.

---

# Recommended workflow for contributors

If you want to use HolidayLens to investigate an issue in `holidays`, use this workflow:

### 1. Find an authoritative source

Prefer sources such as:

* government holiday notifications
* official government calendars
* official gazettes
* central/state government websites
* other authoritative institutional sources

Record the source URL in the reference CSV.

### 2. Create the reference dataset

For example:

```text
data/official/IN/MH/2026.csv
```

### 3. Run HolidayLens

```bash
holidaylens audit \
  --country IN \
  --subdivision MH \
  --year 2026
```

### 4. Investigate discrepancies

Look at:

```text
MISSING
EXTRA
NAME_MISMATCH
DATE_MISMATCH
```

### 5. Verify the finding

Check the authoritative source manually.

Make sure the discrepancy is not caused by:

* an incomplete reference dataset
* an alias issue
* a different holiday category
* a regional rule
* an intentional library behavior

### 6. Reproduce the library behavior

Confirm the result independently using the `holidays` package.

### 7. Fix the upstream project

If the discrepancy is a genuine issue, prepare an upstream change with:

* a clear explanation
* authoritative source
* regression test
* minimal code change

### 8. Record the finding

Keep the reference dataset and HolidayLens result so the discovery is reproducible.

---

# Design philosophy

HolidayLens follows a few principles.

## Evidence first

A discrepancy should be backed by an authoritative source whenever possible.

## Reproducibility

Another contributor should be able to run the same audit and reproduce the finding.

## Small scope

HolidayLens should remain focused on holiday-data verification rather than becoming a large holiday platform.

## Human verification

Automation should help contributors discover problems, not blindly change holiday data.

## Upstream usefulness

The ultimate value of a finding is whether it can help improve the upstream holiday library.

---

# Roadmap

Possible future improvements include:

* Better reference-data path/configuration handling
* Additional official datasets
* More robust source management
* Additional CLI commands
* Stable JSON schema
* CI integration
* Automated audit reports
* Better issue/finding generation
* More sophisticated duplicate detection
* More regional/subdivision coverage
* Historical-year comparison
* Additional authoritative source adapters

These features will be added only when they improve the core goal of finding and verifying real holiday-data issues.

---

# Contributing

Contributions are welcome.

A useful contribution can be:

* adding an authoritative reference dataset
* improving matching logic
* adding tests
* improving documentation
* fixing a false positive
* identifying a genuine holiday-data discrepancy
* improving CLI behavior
* improving provenance handling

Before adding a new rule or dataset, consider whether it improves HolidayLens's ability to identify **real, actionable holiday-data issues**.

---

# License

HolidayLens is released under the license included in this repository.

See [`LICENSE`](LICENSE) for details.

---

# Acknowledgements

HolidayLens is designed to support and complement the open-source [`holidays`](https://github.com/vacanza/python-holidays) project.

The project is motivated by improving the reliability and coverage of programmatic holiday calendars through comparison with authoritative sources.

---

# Current example

A simple audit can be run with:

```bash
holidaylens audit \
  --country IN \
  --subdivision MH \
  --year 2026
```

For machine-readable output:

```bash
holidaylens audit \
  --country IN \
  --subdivision MH \
  --year 2026 \
  --format json
```

The goal is simple:

```text
Authoritative holiday data
            ↓
        HolidayLens
            ↓
Potential discrepancies
            ↓
       Verification
            ↓
   Better holiday data
```

**HolidayLens helps contributors look at holiday data with a lens for accuracy, coverage, and evidence.**
