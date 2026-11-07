"""C9 Reporting service: comparison data (FR-14) and report files (FR-15)."""
import csv
import io

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

CLASSIFICATION_METRICS = [("accuracy", "Accuracy"), ("precision", "Precision"), ("recall", "Recall"),
                          ("f1", "F1-score")]
REGRESSION_METRICS = [("mae", "MAE"), ("mse", "MSE"), ("rmse", "RMSE"), ("r2", "R²")]


def metric_columns(task_type):
    return CLASSIFICATION_METRICS if task_type == "classification" else REGRESSION_METRICS


class CompareError(ValueError):
    pass


def comparison(evaluations):
    """Validate a set of evaluations for comparison and build table/chart data."""
    if len(evaluations) < 2:
        raise CompareError("Select at least two evaluations to compare.")
    if any(e.status != "completed" for e in evaluations):
        raise CompareError("Only completed evaluations can be compared.")
    tasks = {e.task_type for e in evaluations}
    if len(tasks) > 1:
        raise CompareError("Classification and regression results cannot be compared together.")
    task = tasks.pop()
    columns = metric_columns(task)
    rows = [{"id": e.id, "model": e.model_label, "dataset": e.dataset.original_name,
             "hyperparameters": e.hyperparameters,
             "metrics": {key: e.metrics.get(key) for key, _ in columns}} for e in evaluations]
    best = {}
    for key, _ in columns:
        values = [(r["metrics"][key], r["id"]) for r in rows if r["metrics"][key] is not None]
        if values:
            lower_is_better = key in ("mae", "mse", "rmse")
            best[key] = (min(values) if lower_is_better else max(values))[1]
    return {"task_type": task, "columns": [{"key": k, "label": label} for k, label in columns],
            "rows": rows, "best": best}


def _summary_rows(evaluation):
    config = getattr(evaluation.dataset, "config", None)
    rows = [
        ("Dataset", evaluation.dataset.original_name),
        ("Model", evaluation.model_label),
        ("Task", evaluation.task_type),
        ("Status", evaluation.status),
        ("Trained", timezone.localtime(evaluation.created_at).strftime("%d %b %Y %H:%M")),
    ]
    if config:
        rows += [("Target", config.target_column), ("Features", ", ".join(config.feature_columns)),
                 ("Missing values", config.get_missing_strategy_display()),
                 ("Test size", f"{round(config.test_size * 100)}%"), ("Random seed", str(config.random_seed))]
    rows += [("Train / test rows", f"{evaluation.train_rows} / {evaluation.test_rows}")]
    params = ", ".join(f"{k}={v}" for k, v in evaluation.hyperparameters.items()) or "defaults"
    rows.append(("Hyperparameters", params))
    return rows


def report_csv(evaluation):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["field", "value"])
    for key, value in _summary_rows(evaluation):
        writer.writerow([key, value])
    metrics = evaluation.metrics or {}
    for key, label in metric_columns(evaluation.task_type):
        writer.writerow([label, metrics.get(key, "")])
    if metrics.get("confusion_matrix"):
        writer.writerow([])
        writer.writerow(["confusion matrix (rows = actual, columns = predicted)"] + metrics.get("labels", []))
        for label, row in zip(metrics.get("labels", []), metrics["confusion_matrix"]):
            writer.writerow([label] + row)
    return buffer.getvalue().encode("utf-8-sig")    # BOM so Excel opens it with the right encoding


def _table(data, widths, header=True):
    table = Table(data, colWidths=widths)
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C8CDD3")),
             ("FONTSIZE", (0, 0), (-1, -1), 9), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F2F6"))]
    if header:
        style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C8CDD3")),
                 ("FONTSIZE", (0, 0), (-1, -1), 9),
                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                 ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    table.setStyle(TableStyle(style))
    return table


def report_pdf(evaluation):
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    buffer = io.BytesIO()
    story = [Paragraph("ML Model Evaluation Report", styles["Title"]),
             Paragraph(f"{evaluation.model_label} on {evaluation.dataset.original_name}", styles["Heading2"]),
             Spacer(1, 6)]
    story.append(_table([[k, Paragraph(str(v), body)] for k, v in _summary_rows(evaluation)],
                        [45 * mm, 125 * mm], header=False))
    story += [Spacer(1, 10), Paragraph("Metrics (test split)", styles["Heading3"])]
    metrics = evaluation.metrics or {}
    rows = [["Metric", "Value"]] + [[label.replace("²", "2"), f"{metrics.get(key, 0):.4f}"]
                                    for key, label in metric_columns(evaluation.task_type) if key in metrics]
    story.append(_table(rows, [60 * mm, 40 * mm]))
    if metrics.get("confusion_matrix"):
        labels = metrics.get("labels", [])
        story += [Spacer(1, 10), Paragraph("Confusion matrix (rows = actual, columns = predicted)", styles["Heading3"])]
        data = [["Actual \\ Predicted"] + labels] + [[lab] + [str(v) for v in row]
                                                     for lab, row in zip(labels, metrics["confusion_matrix"])]
        width = min(30 * mm, 130 * mm / max(1, len(labels)))
        story.append(_table(data, [40 * mm] + [width] * len(labels)))
    story += [Spacer(1, 14), Paragraph(f"Generated {timezone.localtime():%d %b %Y %H:%M} by the "
                                       "Web Based ML Model Evaluator.", styles["Italic"])]
    SimpleDocTemplate(buffer, pagesize=A4, title="ML Model Evaluation Report",
                      leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm).build(story)
    return buffer.getvalue()
