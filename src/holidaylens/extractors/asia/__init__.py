"""Asia region extractor package.

Automatically registers all Asian holiday extractors when imported.
"""

from holidaylens.extractors.asia import (
    india_gov,
    india_nse,
    india_rbi,
    japan_cao,
    malaysia_gov,
    philippines_gov,
    singapore_mom,
    south_korea_gov,
    thailand_gov,
)

__all__ = [
    "india_gov",
    "india_nse",
    "india_rbi",
    "japan_cao",
    "malaysia_gov",
    "philippines_gov",
    "singapore_mom",
    "south_korea_gov",
    "thailand_gov",
]
