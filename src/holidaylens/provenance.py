from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    authority: str


def validate_source(source: Source) -> None:
    """Validate a reference source."""

    if not source.name.strip():
        raise ValueError("Source name is required")

    if not source.url.strip():
        raise ValueError("Source URL is required")

    if not source.authority.strip():
        raise ValueError("Source authority is required")