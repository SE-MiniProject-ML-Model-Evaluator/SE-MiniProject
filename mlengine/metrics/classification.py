"""FR-12 classification metrics: accuracy, precision, recall, F1 and confusion matrix (US-13)."""
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score


def compute(y_true, y_pred, labels=None):
    """Weighted averages are used so multi-class datasets get one number per metric."""
    labels = list(labels) if labels is not None else sorted(set(y_true) | set(y_pred))
    averaged = {"average": "weighted", "zero_division": 0, "labels": labels}
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, **averaged)), 4),
        "recall": round(float(recall_score(y_true, y_pred, **averaged)), 4),
        "f1": round(float(f1_score(y_true, y_pred, **averaged)), 4),
        "labels": [str(label) for label in labels],
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
    }
