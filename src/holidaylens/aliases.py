from holidaylens.normalization import normalize_name


ALIASES = {
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
}


def canonical_name(name: str) -> str:
    """Return the canonical form of a holiday name."""

    normalized = normalize_name(name)

    return ALIASES.get(normalized, normalized)