from django import template

register = template.Library()


@register.filter
def pct(value):
    """0.9532 -> '95.3%'."""
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return "—"


@register.filter
def cm_rows(metrics):
    """Pair each confusion-matrix row with its label and a shading level (0-100) per cell."""
    matrix = (metrics or {}).get("confusion_matrix") or []
    labels = (metrics or {}).get("labels") or [str(i) for i in range(len(matrix))]
    peak = max((max(row) for row in matrix if row), default=0) or 1
    return [(labels[i], [(v, round(100 * v / peak)) for v in row]) for i, row in enumerate(matrix)]
