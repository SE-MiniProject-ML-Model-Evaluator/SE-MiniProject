"""C7 ML Engine metrics, dispatched by task type."""
from . import classification, regression


def compute(task_type, y_true, y_pred, labels=None):
    if task_type == "classification":
        return classification.compute(y_true, y_pred, labels)
    return regression.compute(y_true, y_pred)
