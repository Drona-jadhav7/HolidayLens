"""Canonical alias dictionary & regional transliterations.

Maps regional and transliterated holiday names to their canonical
English forms used by the Python ``holidays`` library.  Entries are
keyed by the *normalized* form (output of ``normalize_name``).
"""

from __future__ import annotations

from holidaylens.normalization import normalize_name


# ---------------------------------------------------------------------------
# India – Maharashtra state gazette names → holidays library canonical names
# ---------------------------------------------------------------------------
_INDIA_MH_ALIASES: dict[str, str] = {
    "maharashtra din": "maharashtra day",
    "gudhi padwa": "gudi padwa",
    "ramzan id id ul fitra shawal 1": "eid al fitr",
    "mahavir janmakalyanak": "mahavira s birthday",
    "dr babasaheb ambedkar jayanti": "dr b r ambedkar s birthday",
    "dasara": "dussehra",
    "id e milad": "prophet s birthday",
    "moharum": "ashura",
    "mahatma gandhi jayanti": "mahatma gandhi s birthday",
    "guru nanak jayanti": "guru nanak s birthday",
    "buddha pournima": "buddha purnima",
    "bakri id id uz zuha": "eid al adha",
    "chhatrapati shivaji maharaj jayanti": "chhatrapati shivaji maharaj jayanti",
    "diwali amavasya laxmi pujan": "diwali",
    "diwali bali pratipada": "diwali",
    "parsi new year shahenshahi": "parsi new year",
    "holi second day": "holi",
}

# ---------------------------------------------------------------------------
# India – RBI / bank holidays
# ---------------------------------------------------------------------------
_INDIA_BANK_ALIASES: dict[str, str] = {
    "annual closing of bank accounts": "annual closing of bank accounts",
    "christmas day": "christmas",
}

# ---------------------------------------------------------------------------
# India – NSE/BSE stock exchange aliases
# ---------------------------------------------------------------------------
_INDIA_STOCK_ALIASES: dict[str, str] = {
    "muhurat trading": "diwali",
    "laxmi pujan": "diwali",
    "diwali laxmi pujan muhurat trading": "diwali",
    "diwali laxmi pujan": "diwali",
    "diwali balipratipada": "diwali balipratipada",
    "diwali bali pratipada": "diwali balipratipada",
    "settlement holiday": "settlement holiday",
    "bakri id estimated": "eid al adha",
    "muharram estimated": "ashura",
    "dr baba saheb ambedkar jayanti": "dr b r ambedkar s birthday",
    "mahavir jayanti": "mahavira s birthday",
    "christmas day": "christmas",
}

# ---------------------------------------------------------------------------
# Japan – Cabinet Office (CAO) aliases (Romaji & Kanji)
# ---------------------------------------------------------------------------
_JAPAN_ALIASES: dict[str, str] = {
    "ganjitsu": "new year s day",
    "seijin no hi": "coming of age day",
    "kenkoku kinen no hi": "national foundation day",
    "foundation day": "national foundation day",
    "tenno tanjobi": "emperor s birthday",
    "shunbun no hi": "vernal equinox day",
    "showa no hi": "showa day",
    "kenpo kinenbi": "constitution memorial day",
    "constitution day": "constitution memorial day",
    "midori no hi": "greenery day",
    "kodomo no hi": "children s day",
    "umi no hi": "marine day",
    "yama no hi": "mountain day",
    "keiro no hi": "respect for the aged day",
    "shubun no hi": "autumnal equinox day",
    "supotsu no hi": "sports day",
    "bunka no hi": "culture day",
    "kinro kansha no hi": "labor thanksgiving day",
    # Japanese Kanji
    "元日": "new year s day",
    "成人の日": "coming of age day",
    "建国記念の日": "national foundation day",
    "天皇誕生日": "emperor s birthday",
    "春分の日": "vernal equinox day",
    "昭和の日": "showa day",
    "憲法記念日": "constitution memorial day",
    "みどりの日": "greenery day",
    "こどもの日": "children s day",
    "振替休日": "substitute holiday",
    "海の日": "marine day",
    "山の日": "mountain day",
    "敬老の日": "respect for the aged day",
    "国民の休日": "national holiday",
    "秋分の日": "autumnal equinox day",
    "スポーツの日": "sports day",
    "文化の日": "culture day",
    "勤労感謝の日": "labor thanksgiving day",
}

# ---------------------------------------------------------------------------
# Singapore – Ministry of Manpower (MOM) aliases
# ---------------------------------------------------------------------------
_SINGAPORE_ALIASES: dict[str, str] = {
    "hari raya puasa": "eid al fitr",
    "hari raya haji": "eid al adha",
    "deepavali": "diwali",
    "vesak day": "vesak",
    "labour day": "labor day",
    "christmas day": "christmas",
}

# ---------------------------------------------------------------------------
# Malaysia – aliases
# ---------------------------------------------------------------------------
_MALAYSIA_ALIASES: dict[str, str] = {
    "hari raya aidilfitri": "eid al fitr",
    "hari raya aidiladha": "eid al adha",
    "hari raya haji": "eid al adha",
    "hari raya qurban": "eid al adha",
    "maal hijrah": "islamic new year",
    "awal muharam": "islamic new year",
    "maulidur rasul": "prophet s birthday",
    "nuzul al quran": "nuzul al quran",
    "thaipusam": "thaipusam",
    "hari kebangsaan": "national day",
    "hari malaysia": "malaysia day",
    "israk dan mikraj": "isra and mi raj",
    "hari pekerja": "labor day",
    "hari wesak": "vesak",
    "cuti hari wesak": "vesak",
    "tahun baharu cina": "chinese new year",
    "tahun baharu cina hari kedua": "chinese new year second day",
    "hari krismas": "christmas",
}

# ---------------------------------------------------------------------------
# Philippines – aliases
# ---------------------------------------------------------------------------
_PHILIPPINES_ALIASES: dict[str, str] = {
    "araw ng kagitingan": "day of valor",
    "araw ng kasarinlan": "independence day",
    "araw ng mga bayani": "national heroes day",
    "araw ng bonifacio": "bonifacio day",
    "araw ng rizal": "rizal day",
    "eid l fitr": "eid al fitr",
    "eid l adha": "eid al adha",
}

# ---------------------------------------------------------------------------
# Thailand – aliases
# ---------------------------------------------------------------------------
_THAILAND_ALIASES: dict[str, str] = {
    "wan songkran": "songkran",
    "wan chakri": "chakri memorial day",
    "wan visakha bucha": "visakha bucha",
    "wan asarnha bucha": "asalha puja",
    "wan khao phansa": "buddhist lent day",
}

# ---------------------------------------------------------------------------
# South Korea – aliases
# ---------------------------------------------------------------------------
_SOUTH_KOREA_ALIASES: dict[str, str] = {
    "seollal": "korean new year",
    "samiljeol": "independence movement day",
    "eorininal": "children s day",
    "bucheonim osinnal": "birthday of the buddha",
    "hyeonchungil": "memorial day",
    "gwangbokjeol": "national liberation day",
    "chuseok": "chuseok",
    "gaecheonjeol": "national foundation day",
    "hangulnal": "hangul day",
}


# ---------------------------------------------------------------------------
# Master alias dictionary – merge all regional maps
# ---------------------------------------------------------------------------
ALIASES: dict[str, str] = {}
ALIASES.update(_INDIA_MH_ALIASES)
ALIASES.update(_INDIA_BANK_ALIASES)
ALIASES.update(_INDIA_STOCK_ALIASES)
ALIASES.update(_JAPAN_ALIASES)
ALIASES.update(_SINGAPORE_ALIASES)
ALIASES.update(_MALAYSIA_ALIASES)
ALIASES.update(_PHILIPPINES_ALIASES)
ALIASES.update(_THAILAND_ALIASES)
ALIASES.update(_SOUTH_KOREA_ALIASES)


def canonical_name(name: str) -> str:
    """Return the canonical form of a holiday name.

    Normalizes the input and checks the global alias map.
    Falls back to the normalized form when no alias is found.
    """

    normalized = normalize_name(name)

    return ALIASES.get(normalized, normalized)


def register_aliases(mapping: dict[str, str]) -> None:
    """Merge additional aliases into the global map at runtime.

    Keys and values should already be in normalized form.
    """

    ALIASES.update(mapping)