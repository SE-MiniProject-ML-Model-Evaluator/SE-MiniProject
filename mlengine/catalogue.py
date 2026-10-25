"""C6 Model Selector: fixed catalogue of scikit-learn models (FR-09) and their editable hyperparameters."""
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


def _int(default, lo, hi, allow_none=False):
    return {"type": "int", "default": default, "min": lo, "max": hi, "allow_none": allow_none}


def _float(default, lo, hi):
    return {"type": "float", "default": default, "min": lo, "max": hi}


def _choice(default, options):
    return {"type": "choice", "default": default, "options": options}


CATALOGUE = {
    # ---- classification ----
    "logistic_regression": {
        "label": "Logistic Regression", "task": "classification", "estimator": LogisticRegression, "scale": True,
        "fixed": {"max_iter": 1000},
        "params": {"C": _float(1.0, 0.0001, 1000.0), "max_iter": _int(1000, 50, 10000)},
    },
    "decision_tree": {
        "label": "Decision Tree", "task": "classification", "estimator": DecisionTreeClassifier, "seeded": True,
        "params": {"max_depth": _int(None, 1, 100, allow_none=True), "min_samples_split": _int(2, 2, 100),
                   "criterion": _choice("gini", ["gini", "entropy"])},
    },
    "random_forest": {
        "label": "Random Forest", "task": "classification", "estimator": RandomForestClassifier, "seeded": True,
        "params": {"n_estimators": _int(100, 10, 1000), "max_depth": _int(None, 1, 100, allow_none=True)},
    },
    "knn": {
        "label": "k-Nearest Neighbours", "task": "classification", "estimator": KNeighborsClassifier, "scale": True,
        "params": {"n_neighbors": _int(5, 1, 100), "weights": _choice("uniform", ["uniform", "distance"])},
    },
    "svm": {
        "label": "Support Vector Machine", "task": "classification", "estimator": SVC, "scale": True,
        "params": {"C": _float(1.0, 0.0001, 1000.0), "kernel": _choice("rbf", ["rbf", "linear", "poly"])},
    },
    # ---- regression ----
    "linear_regression": {
        "label": "Linear Regression", "task": "regression", "estimator": LinearRegression,
        "params": {"fit_intercept": _choice(True, [True, False])},
    },
    "decision_tree_regressor": {
        "label": "Decision Tree Regressor", "task": "regression", "estimator": DecisionTreeRegressor, "seeded": True,
        "params": {"max_depth": _int(None, 1, 100, allow_none=True), "min_samples_split": _int(2, 2, 100)},
    },
    "random_forest_regressor": {
        "label": "Random Forest Regressor", "task": "regression", "estimator": RandomForestRegressor, "seeded": True,
        "params": {"n_estimators": _int(100, 10, 1000), "max_depth": _int(None, 1, 100, allow_none=True)},
    },
}


class InvalidModelConfig(ValueError):
    pass


def models_for(task_type):
    return {key: spec for key, spec in CATALOGUE.items() if spec["task"] == task_type}


def public_catalogue():
    """Serializable catalogue for GET /api/models."""
    return [{"key": key, "label": spec["label"], "task": spec["task"],
             "hyperparameters": {name: {k: v for k, v in p.items()} for name, p in spec["params"].items()}}
            for key, spec in CATALOGUE.items()]


def resolve_params(model_key, given=None):
    """Merge user values with defaults and check type/range; unknown names are rejected."""
    if model_key not in CATALOGUE:
        raise InvalidModelConfig(f"Unknown model '{model_key}'.")
    spec, given = CATALOGUE[model_key], dict(given or {})
    unknown = set(given) - set(spec["params"])
    if unknown:
        raise InvalidModelConfig(f"Unsupported hyperparameter(s): {', '.join(sorted(unknown))}.")
    resolved = {}
    for name, rule in spec["params"].items():
        value = given.get(name, rule["default"])
        if value in ("", None) and rule.get("allow_none"):
            resolved[name] = None
            continue
        try:
            if rule["type"] == "int":
                value = int(value)
            elif rule["type"] == "float":
                value = float(value)
        except (TypeError, ValueError):
            raise InvalidModelConfig(f"{name} must be a {rule['type']}.")
        if rule["type"] in ("int", "float") and not rule["min"] <= value <= rule["max"]:
            raise InvalidModelConfig(f"{name} must be between {rule['min']} and {rule['max']}.")
        if rule["type"] == "choice" and value not in rule["options"]:
            raise InvalidModelConfig(f"{name} must be one of {rule['options']}.")
        resolved[name] = value
    return resolved


def build_model(model_key, params, random_seed=42):
    spec = CATALOGUE[model_key]
    kwargs = {**spec.get("fixed", {}), **params}
    if spec.get("seeded"):
        kwargs["random_state"] = random_seed
    estimator = spec["estimator"](**kwargs)
    return make_pipeline(StandardScaler(), estimator) if spec.get("scale") else estimator
