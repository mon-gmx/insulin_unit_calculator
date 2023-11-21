import json
from typing import Optional

MIDNIGHT = 0
BEDTIME = 20


def get_units_from_tabular(metric: str, value: float) -> Optional[int]:
    try:
        with open(f"./limits/{metric}_limits.json", "r") as f:
            limits = json.load(f)
            for item in limits:
                if value >= item["min"] and value < item["max"]:
                    return item["units"]
    except (IOError, json.JSONDecodeError, ValueError) as error:
        return None


def get_insulin_units(
    carbs: int = 0,
    sugar: int = 0,
    special: Optional[str] = None

) -> Optional[int]:
    units = 0
    if not carbs or not sugar:
        return units
    if special:
        if special.lower() == "midnight":
            return MIDNIGHT
        elif special.lower() == "bedtime":
            return BEDTIME

    for item in ("carbs", "sugar"):
        tabular_units = get_units_from_tabular(metric=item, value=vars().get(item))
        if tabular_units is None:
            return None
        else:
            units += tabular_units
    return units