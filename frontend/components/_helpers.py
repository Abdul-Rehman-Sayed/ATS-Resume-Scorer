from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    if score >= 80:
        return "#2e7d32", "#e8f5e9"
    if score >= 60:
        return "#f57c00", "#fff3e0"
    return "#c62828", "#ffebee"


def get_severity_style(severity: str) -> Tuple[str, str]:
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "#c62828", "#ffebee"
    if level in ("medium", "moderate"):
        return "#f57c00", "#fff3e0"
    return "#2e7d32", "#e8f5e9"
