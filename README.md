# HolidayLens v2

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-75%20passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Upstream](https://img.shields.io/badge/auditing-vacanza%2Fpython--holidays-orange.svg)](https://github.com/vacanza/python-holidays)

**HolidayLens v2** is an automated multi-region data-quality, harvesting, and verification engine for calendar libraries.

It programmatically extracts official notices from government gazettes, central banks, and financial exchanges, normalizes them into version-controlled reference datasets, compares them across multiple scopes against the Python [`holidays`](https://github.com/vacanza/python-holidays) library (`vacanza/python-holidays`), and produces actionable discrepancy reports and ready-to-file GitHub issue templates.

---

## Table of Contents

- [Why HolidayLens?](#why-holidaylens)
- [Quickstart in 60 Seconds](#quickstart-in-60-seconds)
- [Installation Guide](#installation-guide)
  - [Requirements](#requirements)
  - [Clone & Virtual Environment](#clone--virtual-environment)
  - [Install HolidayLens](#install-holidaylens)
  - [Run the Test Suite](#run-the-test-suite)
- [Core Architecture & Capabilities](#core-architecture--capabilities)
  - [1. Three Orthogonal Auditing Scopes](#1-three-orthogonal-auditing-scopes)
  - [2. Deterministic Storage & Provenance Tracking](#2-deterministic-storage--provenance-tracking)
  - [3. Linguistic & Transliteration Normalization](#3-linguistic--transliteration-normalization)
  - [4. Five Discrepancy Classifications](#4-five-discrepancy-classifications)
- [CLI Reference](#cli-reference)
  - [`holidaylens audit`](#1-holidaylens-audit--single-calendar-auditing)
  - [`holidaylens suite`](#2-holidaylens-suite--batch-multi-country-runner)
  - [`holidaylens extract`](#3-holidaylens-extract--official-data-harvesting)
  - [`holidaylens report`](#4-holidaylens-report--github-issue-generator)
  - [`holidaylens list`](#5-holidaylens-list--registered-extractor-directory)
- [Real-World Case Study: Diwali & Muhurat Trading on NSE](#real-world-case-study-diwali--muhurat-trading-on-nse)
- [Reference Data Layout & Schema](#reference-data-layout--schema)
  - [Directory Hierarchy](#directory-hierarchy)
  - [CSV Schema](#csv-schema)
- [Developer Guide](#developer-guide)
  - [Creating a New Official Extractor](#creating-a-new-official-extractor)
  - [Registering Linguistic Aliases](#registering-linguistic-aliases)
- [Recommended Contributor Workflow](#recommended-contributor-workflow)
- [Project Structure](#project-structure)
- [License & Acknowledgements](#license--acknowledgements)

---

## Why HolidayLens?

Holiday calendars are deceptively complex. Rules shift between national governments, state departments, central banking authorities, and stock exchanges:

* **Movable religious holidays** (e.g. Diwali, Eid, Vesak, Songkran) follow astronomical or lunar calculations that are announced via state gazettes and can vary year-to-year or between states.
* **Banking closures** (e.g. India RBI Section 25 Negotiable Instruments Act or Bank of Thailand) govern financial institutions and may diverge from general civil holidays.
* **Trading exchanges** (e.g. NSE/BSE in India, JPX in Japan, SGX in Singapore) enforce unique trading session schedules, such as special 1-hour evening trading sessions on festival days.
* **Transliteration variations** (Devanagari, Romaji, Kanji, Malay, Thai, Hangul) create false naming discrepancies if not normalized.

HolidayLens automates the discovery of genuine data gaps without manual guesswork:

```text
Official Gazette / Central Bank / Stock Exchange
                       │
                       ▼
       HolidayLens Extractor Subsystem
                       │
                       ▼
    Deterministic Reference Dataset (CSV + Provenance)
                       │
                       ▼
       HolidayLens Multi-Scope Compare Engine
       ├── Unicode accent stripping & token Jaccard similarity
       ├── Canonical alias & transliteration dictionary
       └── Scope alignment (Public vs Bank vs Financial)
                       │
                       ▼
            Actionable Discrepancy Report
                       │
                       ▼
    Automated GitHub Issue / Pull Request Markdown
                       │
                       ▼
        Validated Upstream Contribution
```

---

## Quickstart in 60 Seconds

Run a full batch audit across Asian countries for 2026:

```bash
# Set PYTHONPATH if running from a local checkout without pip install
python -m holidaylens.cli suite --year 2026
```

Audit the National Stock Exchange of India (XNSE) trading calendar:

```bash
python -m holidaylens.cli audit --country IN --category financial --market XNSE --year 2026
```

Export structured JSON and convert it into a ready-to-submit GitHub issue template:

```bash
# 1. Audit and save to JSON
python -m holidaylens.cli audit --country IN --category financial --market XNSE --year 2026 --format json --output reports/in_xnse_2026.json

# 2. Generate GitHub issue markdown
python -m holidaylens.cli report reports/in_xnse_2026.json --output reports/issue_xnse.md
```

Extract public holidays directly using the Japan Cabinet Office (CAO) extractor:

```bash
python -m holidaylens.cli extract --country JP --category government --year 2026
```

---

## Installation Guide

### Requirements

* **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.13, and 3.14)
* **`holidays` package** (`vacanza/python-holidays >= 0.46`)

### Clone & Virtual Environment

Clone the repository:

```bash
git clone https://github.com/Drona-jadhav7/HolidayLens.git
cd HolidayLens
```

Create and activate a virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install HolidayLens

Install HolidayLens in editable development mode:

```bash
pip install -e .
```

To include test and development dependencies:

```bash
pip install -e ".[dev]"
```

### Run the Test Suite

Verify that all unit and integration tests pass:

```bash
python -m pytest
```

```text
============================= 75 passed in 1.89s ==============================
```

---

## Core Architecture & Capabilities

HolidayLens v2 is built on four architectural pillars:

### 1. Three Orthogonal Auditing Scopes

Rather than flattening all holidays into a single generic list, HolidayLens distinguishes between three orthogonal scopes:

| Scope | Category Parameter | Target Authority | Target Function in `holidays` |
|---|---|---|---|
| **Scope A: Public / Civil** | `--category public` | Government Ministries, Official Gazettes | `holidays.country_holidays()` |
| **Scope B: Banking** | `--category bank` | Central Banks (RBI, BOT, MAS) | `holidays.country_holidays(categories=("public", "bank"))` |
| **Scope C: Financial / Trading** | `--category financial --market <MIC>` | Stock Exchanges (XNSE, XBOM, XTKS, XSES, XKRX) | `holidays.financial_holidays(market)` |

### 2. Deterministic Storage & Provenance Tracking

Every reference dataset in `data/official/` maintains cryptographic integrity and full origin provenance:
- **`source`**: The exact URL of the gazette notification, regulatory order, or exchange circular.
- **`authority`**: The issuing entity (e.g. *Reserve Bank of India*, *National Stock Exchange of India*, *Cabinet Office, Government of Japan*).
- **`retrieved_at`**: UTC timestamp of data harvesting.
- **`checksum`**: SHA-256 digest computed via [`compute_checksum()`](file:///d:/MY/HolidayLens/src/holidaylens/provenance.py#L51).

### 3. Linguistic & Transliteration Normalization

To prevent superficial spelling or transliteration differences from triggering false positives:
- **Unicode Accent Stripping**: Normalizes NFKD combining marks (e.g., `é` -> `e`).
- **Punctuation & Case Neutralization**: Converts to lowercase, strips punctuation, collapses whitespace.
- **Jaccard Token Similarity**: Measures word-token overlap to recognize reordered multi-word phrases.
- **Canonical Alias Map**: [`holidaylens.aliases`](file:///d:/MY/HolidayLens/src/holidaylens/aliases.py) maps hundreds of regional language terms to standard library forms (e.g., Devanagari/Marathi *Gudhi Padwa* -> *Gudi Padwa*, Kanji *元日* -> *New Year's Day*, Malay *Hari Raya Aidilfitri* -> *Eid al Fitr*, Tagalog *Araw ng Kagitingan* -> *Day of Valor*).

### 4. Five Discrepancy Classifications

Every holiday comparison result falls into one of five statuses:

| Status | Meaning | Action Needed |
|---|---|---|
| **`MATCH`** | Date and normalized canonical name match exactly. | Verified accurate. |
| **`MISSING`** | Holiday exists in the official gazette/notice but is absent from the library. | High priority upstream bug candidate. |
| **`EXTRA`** | Holiday exists in the library but is absent from the authoritative source. | Check whether the library included an unofficial observance. |
| **`NAME_MISMATCH`** | Dates match, but names differ beyond known aliases. | Check if an alias or transliteration should be added. |
| **`DATE_MISMATCH`** | Names match, but dates differ. | Critical check: possible movable festival date error or missing substitution rule. |

---

## CLI Reference

HolidayLens exposes five unified subcommands:

```text
holidaylens [-h] {audit,suite,extract,report,list} ...
```

---

### 1. `holidaylens audit` – Single Calendar Auditing

Compares an official reference calendar against the `holidays` library.

```bash
holidaylens audit --country <CODE> --year <YEAR> [options]
```

#### Options:
* `--country` *(required)*: ISO 3166-1 alpha-2 country code (e.g. `IN`, `JP`, `SG`, `MY`, `PH`, `TH`, `KR`).
* `--year` *(required)*: Four-digit year to audit (e.g. `2026`).
* `--subdivision`: State or province code (e.g. `--subdivision MH`).
* `--category`: One of `public` (default), `bank`, or `financial`.
* `--market`: Market Identifier Code (required for `financial`, e.g. `XNSE`, `XBOM`, `XTKS`).
* `--reference`: Path to an explicit reference CSV file. If omitted, HolidayLens automatically searches `data/official/<COUNTRY>/...`.
* `--format`: Output format: `text` (default) or `json`.
* `--output`: Path to write the JSON report to (used with `--format json`).

#### Examples:

**Audit national public holidays (human-readable table):**
```bash
holidaylens audit --country SG --year 2026
```

**Audit state-level holidays (Maharashtra, India):**
```bash
holidaylens audit --country IN --subdivision MH --year 2026
```

**Audit central bank holidays (Reserve Bank of India):**
```bash
holidaylens audit --country IN --category bank --year 2026
```

**Audit stock exchange trading schedule (NSE India):**
```bash
holidaylens audit --country IN --category financial --market XNSE --year 2026
```

**Export structured JSON report:**
```bash
holidaylens audit --country IN --category financial --market XNSE --year 2026 --format json --output reports/in_xnse_2026.json
```

---

### 2. `holidaylens suite` – Batch Multi-Country Runner

Executes batch data-quality audits across all available countries, subdivisions, and scopes in `data/official/`.

```bash
holidaylens suite --year <YEAR> [--data-dir <DIR>]
```

#### Options:
* `--year` *(required)*: Four-digit year to audit (e.g. `2026`).
* `--data-dir`: Custom path to official reference directory (defaults to `data/official`).

#### Example:
```bash
holidaylens suite --year 2026
```

#### Sample Output:
```text
Suite Results: 2026
--------------------------------
Total audits:  12
Passed:        5
Failed:        7
Errors:        0

  [FAIL] IN/AS                coverage=14.3% (public)
  [FAIL] IN/MH                coverage=50.0% (public)
  [FAIL] IN/MP                coverage=44.0% (public)
  [FAIL] IN/UK                coverage=73.7% (public)
  [FAIL] IN/national          coverage=30.4% (bank)
  [FAIL] IN/national          coverage=76.5% (financial)
  [PASS] JP/national          coverage=100.0% (public)
  [PASS] SG/national          coverage=100.0% (public)
  [PASS] MY/national          coverage=100.0% (public)
  [PASS] PH/national          coverage=100.0% (public)
  [FAIL] TH/national          coverage=100.0% (public)
  [PASS] KR/national          coverage=100.0% (public)
```

> **Note on exit codes:** The `suite` command exits with `0` if all audits passed with 100% exact coverage, and `1` if any discrepancies were discovered (ideal for automated CI assertions).

---

### 3. `holidaylens extract` – Official Data Harvesting

Harvests official holiday schedules using country-specific and category-specific extractors.

```bash
holidaylens extract --country <CODE> --category <CAT> --year <YEAR> [--output <PATH>]
```

#### Options:
* `--country` *(required)*: ISO country code (e.g. `JP`, `IN`, `SG`, `MY`, `PH`, `TH`, `KR`).
* `--category`: Extractor category (e.g. `government`, `bank`, `financial`). Default: `government`.
* `--year` *(required)*: Year to extract.
* `--output`: Output CSV file path. If omitted, outputs tab-delimited records to stdout.

#### Examples:

**Print extracted Japan holidays to terminal:**
```bash
holidaylens extract --country JP --category government --year 2026
```

**Save extracted Singapore MOM holidays to CSV:**
```bash
holidaylens extract --country SG --category government --year 2026 --output data/official/SG/government/2026.csv
```

---

### 4. `holidaylens report` – GitHub Issue Generator

Transforms a structured JSON audit report into a ready-to-submit GitHub issue markdown file formatted for `vacanza/python-holidays`.

```bash
holidaylens report <REPORT_JSON> [--output <FILE.md>]
# or
holidaylens report --input <REPORT_JSON> [--output <FILE.md>]
```

#### Options:
* `<input>` or `--input`: Path to the input JSON report generated by `holidaylens audit --format json`.
* `--output`: Path to save the markdown file. If omitted, prints markdown to stdout.

#### Example:
```bash
holidaylens report reports/in_xnse_2026.json --output reports/issue_xnse.md
```

#### Generated Markdown Preview:
```markdown
# [IN] Holiday data gaps for 2026 (subdivision=N/A, category=financial)

## Summary

| Metric | Value |
|--------|-------|
| Country | `IN` |
| Subdivision | `N/A` |
| Year | 2026 |
| Category | financial |
| Coverage | 76.5% |
| Missing | 2 |
| Extra | 0 |
| Name Mismatch | 2 |
| Date Mismatch | 0 |

## Missing Holidays

The following holidays appear in official government records but are absent from `python-holidays`:

| Date | Name | Source |
|------|------|--------|
| 2026-08-15 | Independence Day | https://www.nseindia.com/regulations/listing-compliance/nse-market-timings-holidays |
| 2026-11-08 | Diwali Laxmi Pujan (Muhurat Trading) | https://www.nseindia.com/regulations/listing-compliance/nse-market-timings-holidays |

## Name Mismatches

| Date | Official Name | Library Name |
|------|--------------|--------------|
| 2026-05-28 | Bakri Id | Bakri Id (estimated) |
| 2026-06-26 | Muharram | Muharram (estimated) |

## Reproduction

```bash
holidaylens audit --country IN --year 2026 --format json
```

Generated by [HolidayLens](https://github.com/vacanza/python-holidays)
```

---

### 5. `holidaylens list` – Registered Extractor Directory

Displays all extractors currently registered in the engine:

```bash
holidaylens list
```

#### Output:
```text
Country    Category        Class
--------------------------------------------------
IN         bank            IndiaRBIExtractor
IN         financial       IndiaNSEExtractor
IN         government      IndiaGovExtractor
JP         government      JapanCAOExtractor
KR         government      SouthKoreaGovExtractor
MY         government      MalaysiaGovExtractor
PH         government      PhilippinesGovExtractor
SG         government      SingaporeMOMExtractor
TH         bank            ThailandGovExtractor
TH         government      ThailandGovExtractor
```

---

## Real-World Case Study: Diwali & Muhurat Trading on NSE

One of the real-world motivating discoveries during HolidayLens v2 testing was the National Stock Exchange of India (XNSE) trading calendar behavior:

### The Phenomenon
On Diwali (Laxmi Pujan), stock exchanges in India remain closed for regular trading hours, but host a special **1-hour evening "Muhurat Trading" session**. Because exchanges observe Diwali as a holiday event, official trading circulars explicitly list Diwali (Laxmi Pujan) as a holiday.

### The Discrepancy
When Diwali falls on a weekend (Saturday or Sunday), the `holidays.financial_holidays('XNSE')` implementation drops the holiday entirely because it assumes markets are already closed on weekends. However:
1. In 2026, Diwali falls on Sunday, November 8. The official NSE calendar lists Diwali (Laxmi Pujan), but `python-holidays` omitted it.
2. In years like **2030, 2033, and 2036**, Diwali falls on weekends and is completely missing from `financial_holidays('XNSE')`.

### Detection & Reproduction
Running [`check.py`](file:///d:/MY/HolidayLens/check.py) scans XNSE across years:

```bash
python check.py
```

```text
Scanning XNSE for Diwali (Laxmi Pujan) / Muhurat Trading from 2016 to 2036...

[FOUND] 2024: 'Diwali Laxmi Pujan' is listed on 2024-11-01 (Friday)
[FOUND] 2025: 'Diwali Laxmi Pujan' is listed on 2025-10-21 (Tuesday)
[FOUND] 2026: 'Diwali Balipratipada' is listed on 2026-11-10 (Tuesday)
[MISSING] 2030: Diwali / Muhurat Trading is entirely missing from XNSE.
[MISSING] 2033: Diwali / Muhurat Trading is entirely missing from XNSE.
[MISSING] 2036: Diwali / Muhurat Trading is entirely missing from XNSE.

--- Diagnostic Summary ---
Issue Verified: Diwali is missing in the following years: [2030, 2033, 2036]
Conclusion: The framework consistently drops Diwali whenever it falls on a weekend, failing to implement the 1-hour Muhurat Trading exception.
```

HolidayLens v2 catches this automatically and packages the findings into a validated GitHub issue ready for upstream submission.

---

## Reference Data Layout & Schema

### Directory Hierarchy

Authoritative reference datasets are version-controlled in `data/official/`:

```text
data/official/
├── ET/
│   └── 2026.csv                    <-- Ethiopia national public holidays
├── IN/
│   ├── AS/2026.csv                 <-- India state subdivision (Assam)
│   ├── MH/2026.csv                 <-- India state subdivision (Maharashtra)
│   ├── MP/2026.csv                 <-- India state subdivision (Madhya Pradesh)
│   ├── UK/2026.csv                 <-- India state subdivision (Uttarakhand)
│   ├── bank/2026.csv               <-- India RBI banking schedule
│   └── stock/2026.csv              <-- India NSE financial trading schedule
├── JP/
│   └── government/2026.csv         <-- Japan Cabinet Office (内閣府) holidays
├── SG/
│   └── government/2026.csv         <-- Singapore Ministry of Manpower holidays
├── MY/
│   └── government/2026.csv         <-- Malaysia Cabinet Division holidays
├── PH/
│   └── government/2026.csv         <-- Philippines Official Gazette holidays
├── TH/
│   └── government/2026.csv         <-- Thailand Bank of Thailand / Cabinet holidays
└── KR/
    └── government/2026.csv         <-- South Korea Ministry of Personnel Management
```

### CSV Schema

Reference CSVs use UTF-8 encoding with a required header row:

```csv
date,name,category,source,authority,subdivision
2026-01-26,Republic Day,public,https://mmrda.maharashtra.gov.in/en/public-holidays,Government of India,MH
2026-11-08,Diwali Laxmi Pujan (Muhurat Trading),financial,https://www.nseindia.com,National Stock Exchange of India,
```

#### Fields:
* **`date`** *(required)*: ISO 8601 date (`YYYY-MM-DD`).
* **`name`** *(required)*: Official holiday name as specified in the gazette or circular.
* **`category`** *(optional)*: `public`, `bank`, `financial`, or `government` (defaults to `public`).
* **`source`** *(optional)*: The authoritative web URL or gazette reference.
* **`authority`** *(optional)*: The issuing official institution.
* **`subdivision`** *(optional)*: ISO 3166-2 state/province subdivision code (e.g. `MH`).

---

## Developer Guide

### Creating a New Official Extractor

To add an automated extractor for a new country or authority:

1. Create a new module under `src/holidaylens/extractors/asia/` (or a new regional subpackage):

```python
from pathlib import Path
from holidaylens.extractors.base import BaseExtractor, ExtractionResult
from holidaylens.extractors.registry import register
from holidaylens.models import Holiday
from holidaylens.sources import load_csv

@register("TW", "government")
class TaiwanGovExtractor(BaseExtractor):
    """Extract official public holidays for Taiwan."""

    country_code = "TW"
    category = "government"
    source_url = "https://www.dgpa.gov.tw"
    authority_name = "Directorate-General of Personnel Administration"

    def __init__(self, *, data_dir: str | Path = "data/official") -> None:
        self.data_dir = Path(data_dir)

    def extract(self, year: int) -> ExtractionResult:
        result = ExtractionResult(metadata=self.build_metadata(year))
        csv_path = self.data_dir / "TW" / "government" / f"{year}.csv"

        if csv_path.exists():
            result.holidays = load_csv(csv_path)
        else:
            result.warnings.append(f"No reference CSV found at {csv_path}")

        return result
```

2. Export the new extractor module in [`src/holidaylens/extractors/asia/__init__.py`](file:///d:/MY/HolidayLens/src/holidaylens/extractors/asia/__init__.py).

3. The `@register` decorator automatically binds it to the registry. It will immediately show up in `holidaylens list` and become available via `holidaylens extract --country TW --year 2026`.

### Registering Linguistic Aliases

When official notices use language variations, register them in [`src/holidaylens/aliases.py`](file:///d:/MY/HolidayLens/src/holidaylens/aliases.py):

```python
_MY_COUNTRY_ALIASES: dict[str, str] = {
    # Key: normalized official name -> Value: normalized canonical library name
    "chao phraya day": "national memorial day",
}

ALIASES.update(_MY_COUNTRY_ALIASES)
```

---

## Recommended Contributor Workflow

If you are using HolidayLens to research and propose an improvement to the `python-holidays` library, follow this verified workflow:

```text
1. Find Authoritative Source (Gazette, Central Bank, Regulatory Circular)
                           │
                           ▼
2. Create or Update Reference CSV in data/official/<COUNTRY>/...
                           │
                           ▼
3. Run HolidayLens Audit:
   holidaylens audit --country <CC> --year <YYYY> --format json --output report.json
                           │
                           ▼
4. Generate GitHub Issue Markdown:
   holidaylens report report.json --output issue.md
                           │
                           ▼
5. Review the Generated Issue Template
   Verify whether missing/mismatched holidays are true gaps vs out-of-scope observances
                           │
                           ▼
6. Implement Minimal Upstream PR
   Fork vacanza/python-holidays, add missing rule/dates, submit PR linking authoritative source
```

---

## Project Structure

```text
HolidayLens/
├── data/
│   └── official/                       # Authoritative reference datasets
│       ├── ET/                         # Ethiopia
│       ├── IN/                         # India (AS, MH, MP, UK, bank, stock)
│       ├── JP/                         # Japan (Cabinet Office)
│       ├── SG/                         # Singapore (Ministry of Manpower)
│       ├── MY/                         # Malaysia (Cabinet Division)
│       ├── PH/                         # Philippines (Official Gazette)
│       ├── TH/                         # Thailand (Bank of Thailand / Cabinet)
│       └── KR/                         # South Korea (Ministry of Personnel Management)
│
├── src/
│   └── holidaylens/
│       ├── __init__.py                 # Top-level package exports
│       ├── aliases.py                  # Canonical name & regional transliteration dictionary
│       ├── compare.py                  # Core comparison engine
│       ├── library.py                  # Integration with python-holidays loaders
│       ├── matching.py                 # Token overlap, fuzzy match, & alias resolution
│       ├── models.py                   # Dataclasses: Holiday, SourceMetadata, AuditResult
│       ├── normalization.py            # Accent stripping & string normalization pipeline
│       ├── provenance.py               # SHA-256 file checksums & official source registries
│       ├── report.py                   # Terminal format, JSON export, GitHub issue generator
│       ├── sources.py                  # CSV parsing, writing, & path resolution
│       ├── suite.py                    # Multi-country batch runner & aggregator
│       ├── cli.py                      # Subcommand CLI: audit, suite, extract, report, list
│       └── extractors/
│           ├── __init__.py             # Extractor subsystem package
│           ├── base.py                 # BaseExtractor & ExtractionResult dataclasses
│           ├── registry.py             # Decorator-based registry & auto-discovery
│           └── asia/                   # Asian region extractors (IN, JP, SG, MY, PH, TH, KR)
│
├── tests/                              # Comprehensive test suite (75 tests passing)
│   ├── test_cli.py                     # Subcommand CLI tests
│   ├── test_compare.py                 # Comparison engine tests
│   ├── test_extractors.py              # Extractor & registry tests
│   ├── test_library.py                 # holidays loader wrapper tests
│   ├── test_matching.py                # Matching & alias tests
│   ├── test_models.py                  # Dataclass initialization tests
│   ├── test_provenance.py              # Checksum & source validation tests
│   ├── test_report.py                  # Report formatting & issue template tests
│   ├── test_sources.py                 # CSV loading & writing tests
│   └── test_suite.py                   # Batch suite execution tests
│
├── check.py                            # Standalone Muhurat Trading diagnostic scanner
├── pyproject.toml                      # Project metadata & build configuration
├── README.md                           # Documentation
└── LICENSE                             # MIT License
```

---

## License & Acknowledgements

HolidayLens is released under the **MIT License**. See the [`LICENSE`](LICENSE) file for complete details.

HolidayLens is built to support and complement the open-source [**`vacanza/python-holidays`**](https://github.com/vacanza/python-holidays) project. We express immense gratitude to the maintainers and contributors of `python-holidays` for establishing the standard for open-source holiday calculation.
