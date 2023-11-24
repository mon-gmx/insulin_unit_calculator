import json
from typing import Optional

from config import (bedtime_units,
                    default_carbs_ratio,
                    midnight_units)
from logger import get_logger

log = get_logger(__name__)


def get_units_from_ratio(value: int, ratio: int, limit: int = 20) -> int:
    for i in range(1, limit):
        if value >= (i * ratio) and value < ((i + 1) * ratio):
            return i
    return limit


def get_units_from_tabular(metric: str, value: float) -> Optional[int]:
    try:
        with open(f"./limits/{metric}_limits.json", "r") as f:
            limits = json.load(f)
            for item in limits:
                if value >= item["min"] and value < item["max"]:
                    return item["units"]
    except (IOError, json.JSONDecodeError, ValueError) as error:
        log.error(f"Read of limits failed: {error}")
        return None


def get_insulin_units(
    carbs: int = 0,
    sugar: int = 0,
    carbs_ratio: int = default_carbs_ratio,
    special: Optional[str] = None
) -> Optional[int]:
    units = 0
    if not carbs and not sugar:
        return units
    log.info(f"Special is: {special}")
    if special:
        if "midnight" in special.lower():
            return midnight_units
        elif "bedtime" in special.lower():
            return bedtime_units

    units += get_units_from_ratio(carbs, carbs_ratio)
    log.info(units)
    sugar_tabular_units = get_units_from_tabular(metric="sugar", value=sugar)
    if sugar_tabular_units is None:
        log.warning("Tabular units did not load")
        return None
    else:
        units += sugar_tabular_units
    return units
