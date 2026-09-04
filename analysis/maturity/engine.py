"""Maturity engine — color-based classification of fruit crops."""

import cv2
import numpy as np


def _color_percentages(hsv):
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    red1 = (h <= 15) & (s >= 40) & (v >= 50)
    red2 = (h >= 165) & (s >= 40) & (v >= 50)
    red = red1 | red2

    green = (h >= 35) & (h <= 85) & (s >= 30) & (v >= 50)
    yellow = (h >= 15) & (h < 35) & (s >= 40) & (v >= 50)
    white = (s <= 40) & (v >= 150)

    total = max(1, int((v >= 50).sum()))
    return {
        "red": float(red.sum()) / total * 100,
        "green": float(green.sum()) / total * 100,
        "yellow": float(yellow.sum()) / total * 100,
        "white": float(white.sum()) / total * 100,
    }


def _tomato(p):
    red = p["red"]
    if red <= 1:
        return "green", 5
    if red <= 10:
        return "breaker", int(10 + red * 3)
    if red <= 30:
        return "turning", int(30 + (red - 10) * 1.5)
    if red <= 60:
        return "pink", int(50 + (red - 30))
    if red <= 90:
        return "light_red", int(75 + (red - 60) * 0.5)
    return "red", min(100, int(95 + (red - 90) * 0.17))


def _mango(p):
    yellow = p["yellow"]
    green = p["green"]
    if yellow <= 5 and green >= 50:
        return "green", 10
    if yellow <= 25:
        return "breaker", int(15 + yellow * 1.5)
    if yellow <= 75:
        return "turning", int(40 + (yellow - 25) * 1.2)
    return "ripe", min(100, int(90 + (yellow - 75) * 0.4))


def _strawberry(p):
    red = p["red"]
    white = p["white"]
    green = p["green"]
    if green >= 40 and red <= 5:
        return "green", 10
    if white >= 30 and red <= 15:
        return "white", 25
    if red <= 60:
        return "turning", int(40 + red * 0.8)
    return "red", min(100, int(90 + (red - 60) * 0.25))


_CLASSIFIERS = {
    "tomato": _tomato,
    "mango": _mango,
    "strawberry": _strawberry,
}


def predict_maturity(image, crop):
    crop = crop.lower().strip()
    if crop not in _CLASSIFIERS:
        raise ValueError(f"Unknown crop '{crop}'. Use one of: {list(_CLASSIFIERS.keys())}")
    if image is None or image.size == 0:
        raise ValueError("Empty image")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    p = _color_percentages(hsv)
    stage, score = _CLASSIFIERS[crop](p)

    return {
        "stage": stage,
        "score": score,
        "color_stats": {k: round(v, 2) for k, v in p.items()},
    }


if __name__ == "__main__":
    print("Testing maturity engine...")

    red = np.full((100, 100, 3), [0, 0, 255], dtype=np.uint8)
    print("Red -> tomato:", predict_maturity(red, "tomato"))

    green = np.full((100, 100, 3), [0, 255, 0], dtype=np.uint8)
    print("Green -> tomato:", predict_maturity(green, "tomato"))

    yellow = np.full((100, 100, 3), [0, 255, 255], dtype=np.uint8)
    print("Yellow -> mango:", predict_maturity(yellow, "mango"))

    print("Done.")
