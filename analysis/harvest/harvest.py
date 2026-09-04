"""Harvest prediction — reads rules from crops.yaml."""

import os
import yaml

_CONFIG = None
_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "crops.yaml")


def _load():
    global _CONFIG
    if _CONFIG is None:
        with open(_PATH, "r") as f:
            _CONFIG = yaml.safe_load(f)
    return _CONFIG


def predict_harvest(crop, stage):
    crop = crop.lower().strip()
    config = _load()

    if crop not in config:
        raise ValueError(f"Unknown crop '{crop}'")

    rules = config[crop]["harvest_rules"]
    if stage not in rules:
        raise ValueError(f"Unknown stage '{stage}' for {crop}")

    rule = rules[stage]
    return {
        "readiness": rule["readiness"],
        "estimated_time": rule["time"],
    }


def get_crop_info(crop):
    crop = crop.lower().strip()
    config = _load()
    if crop not in config:
        raise ValueError(f"Unknown crop '{crop}'")
    return config[crop]


if __name__ == "__main__":
    for crop in ["tomato", "mango", "strawberry"]:
        print(f"\n{crop.upper()}")
        info = get_crop_info(crop)
        print(f"  Optimal temp: {info['optimal_temperature']}")
        for stage in info["stages"]:
            r = predict_harvest(crop, stage)
            print(f"  {stage:12s} -> {r['readiness']:6s} | {r['estimated_time']}")
