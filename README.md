# HolidayLens

**HolidayLens** is an open-source data-quality and verification tool for analyzing holiday calendars and identifying inconsistencies, missing entries, incorrect dates, and coverage gaps in holiday datasets.

> **See what's missing. Verify what's there. Improve holiday data.**

---

## 🎯 Why HolidayLens?

Holiday calendars look simple, but maintaining accurate holiday data across countries, states, regions, and years can be surprisingly difficult.

Holiday information may vary because of:

* Regional and state-specific holidays
* Different official names for the same observance
* Holidays that change dates every year
* Public, optional, and restricted holidays
* Government-declared holidays
* One-off or exceptional holidays
* Differences between official calendars and software datasets

HolidayLens aims to make these differences **visible, measurable, and easier to investigate**.

---

## ✨ What HolidayLens Does

HolidayLens compares an authoritative holiday source against a holiday dataset and identifies differences.

### Core capabilities

* 🔎 Detect missing holidays
* 📅 Detect incorrect or mismatched dates
* ➕ Detect holidays present in the dataset but absent from the reference
* 🏷️ Identify holiday-name differences
* 🌍 Support countries and regional subdivisions
* 📊 Generate comparison and coverage reports
* 🧪 Validate holiday datasets
* 📁 Work with structured official holiday data
* 🤖 Provide a foundation for automated holiday-data testing

A typical comparison looks like:

```text
HolidayLens Report
India / Maharashtra / 2026
────────────────────────────────

Official holidays: 18
Library holidays:  17

✓ Matching:          16
✗ Missing:             1
⚠ Extra:               0
⚠ Date mismatches:     1
```

---

## 🏗️ How It Works

HolidayLens separates **data collection**, **normalization**, **comparison**, and **reporting**.

```text
             Official Source
                   │
                   ▼
            ┌─────────────┐
            │   Import    │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ Normalize   │
            └──────┬──────┘
                   │
                   │
                   ▼
            ┌─────────────┐
            │   Compare   │◄──── Holiday Dataset
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │   Report    │
            └─────────────┘
```

The reference source is treated as the basis for verification rather than embedding country-specific assumptions directly into the comparison engine.

---

## 📋 Example

Suppose an official Maharashtra holiday calendar contains:

```text
2026-03-03    Holi
2026-05-01    Maharashtra Day
2026-09-14    Ganesh Chaturthi
```

while the dataset being tested contains:

```text
2026-03-04    Holi
2026-05-01    Maharashtra Day
```

HolidayLens can report:

```text
Missing holidays
────────────────────────────
Ganesh Chaturthi    2026-09-14

Date mismatches
────────────────────────────
Holi
Official: 2026-03-03
Dataset:  2026-03-04
```

This makes the result useful for developers maintaining holiday libraries and for researchers investigating calendar accuracy.

---

## 🧩 Project Architecture

The project is designed around small, independent components:

```text
src/
└── holidaylens/
    ├── __init__.py
    ├── cli.py
    ├── models.py
    ├── sources.py
    ├── library.py
    ├── normalize.py
    ├── matching.py
    ├── compare.py
    └── report.py
```

### Components

| Module         | Responsibility                               |
| -------------- | -------------------------------------------- |
| `models.py`    | Core holiday data structures                 |
| `sources.py`   | Loading reference/official data              |
| `library.py`   | Loading holiday data from supported datasets |
| `normalize.py` | Normalizing names and data                   |
| `matching.py`  | Matching holidays between datasets           |
| `compare.py`   | Detecting differences                        |
| `report.py`    | Generating reports                           |
| `cli.py`       | Command-line interface                       |

The architecture is intentionally designed so that additional data sources can be added without rewriting the comparison engine.

---

## 📂 Data Model

HolidayLens will use a normalized representation of a holiday.

Conceptually:

```text
Holiday
├── date
├── name
├── category
└── source
```

For example:

```json
{
  "date": "2026-09-14",
  "name": "Ganesh Chaturthi",
  "category": "public",
  "source": "Official Maharashtra Holiday Calendar"
}
```

This common representation allows HolidayLens to compare information from different sources consistently.

---

## 🌍 Regional Support

HolidayLens is designed to handle both national and regional calendars.

For example:

```text
India
├── Maharashtra
├── Gujarat
├── Karnataka
├── West Bengal
└── ...
```

The comparison engine should remain independent of individual regions.

Region-specific information belongs in the **data layer**, not in hard-coded comparison logic.

---

## 🔬 Data Quality Checks

HolidayLens is intended to eventually provide several levels of validation.

### Holiday presence

```text
Official → Dataset

✓ Present
✗ Missing
⚠ Unexpected
```

### Date accuracy

```text
Official: 2026-09-14
Dataset:  2026-09-15

→ Date mismatch
```

### Name consistency

```text
Official: Ganesh Chaturthi
Dataset:  Ganesh Chaturthi / Vinayak Chaturthi

→ Possible name variation
```

Name differences should not automatically be treated as errors. HolidayLens should distinguish between a **true mismatch** and a **known naming variation**.

---

## 📊 Future Reporting

HolidayLens is planned to support multiple report formats.

### Terminal

```text
HolidayLens Report
────────────────────────────

Country:     India
Subdivision: MH
Year:        2026

Official:    18
Dataset:     17

Matching:    16
Missing:      1
Extra:        0
Mismatch:     1
```

### JSON

Useful for CI pipelines and other software:

```json
{
  "country": "IN",
  "subdivision": "MH",
  "year": 2026,
  "matching": 16,
  "missing": 1,
  "extra": 0,
  "date_mismatches": 1
}
```

---

## 🛠️ Development

HolidayLens is currently being developed from the ground up.

The project will prioritize:

* Clear architecture
* Reproducible results
* Strong test coverage
* Transparent data sources
* Minimal hard-coded assumptions
* Easy contribution
* Automated validation

---

## 🧪 Testing

Tests will cover individual components as well as complete comparisons.

Planned test areas include:

```text
tests/
├── test_normalize.py
├── test_matching.py
└── test_compare.py
```

The goal is for every reported discrepancy to be reproducible and explainable.

---

## 🚧 Project Status

**Early development**

HolidayLens is currently being built from scratch.

### Current roadmap

* [ ] Project foundation
* [ ] Holiday data model
* [ ] Official data importer
* [ ] Holiday dataset adapter
* [ ] Data normalization
* [ ] Matching engine
* [ ] Difference detection
* [ ] Terminal reports
* [ ] JSON reports
* [ ] CLI
* [ ] Automated tests
* [ ] CI integration
* [ ] Documentation
* [ ] First complete country/regional dataset

---

## 🤝 Contributing

Contributions are welcome.

Possible contribution areas include:

* Adding official holiday datasets
* Improving normalization
* Improving matching algorithms
* Adding country or regional support
* Writing tests
* Improving documentation
* Finding and documenting data-quality issues

Before contributing, please ensure that changes are backed by reliable sources whenever possible.

---

## 📜 Data Philosophy

HolidayLens does **not** attempt to determine holidays based on assumptions.

Instead:

> **Authoritative sources provide the reference; HolidayLens performs the analysis.**

This distinction is important because holiday rules can vary by jurisdiction and can change from year to year.

When a discrepancy is found, the goal is to provide enough information for a developer or researcher to investigate the underlying source.

---

## 🔭 Long-Term Vision

HolidayLens aims to become a reusable quality-assurance layer for holiday data.

The long-term goal is to make it possible to answer questions such as:

> **“How accurate is this holiday dataset for this country, region, and year?”**

with measurable evidence.

Ultimately, HolidayLens could support:

```text
Official Calendars
       │
       ▼
   HolidayLens
       │
       ├── Accuracy
       ├── Coverage
       ├── Consistency
       ├── Historical Changes
       └── Anomaly Detection
              │
              ▼
       Developers / Researchers
```

---

## 📄 License

HolidayLens will be released under an open-source license.

The final license will be added when the project repository is initialized.

---

## ⭐ Project

**HolidayLens**

*See what's missing. Verify what's there. Improve holiday data.*
