"""FR-13 regression metrics: MAE, MSE and R² (US-14)."""
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute(y_true, y_pred):
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "mse": round(mse, 4),
        "rmse": round(mse ** 0.5, 4),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
    }
