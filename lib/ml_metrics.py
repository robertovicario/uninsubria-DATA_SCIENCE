# =========================
# Dependencies
# =========================

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay,
    mean_absolute_error, root_mean_squared_error, r2_score
)
from typing import Literal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =========================
# Methods
# =========================

def compute_metrics_clf(
    metrics_out: dict,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    set: str = 'test'
) -> None:

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    metrics_out[set] = [
        int(len(y_true)), float(acc), float(prec), float(rec), float(f1)
    ]

def compute_metrics_reg(
    metrics_out: dict,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    set: str = 'test'
) -> None:

	mae = mean_absolute_error(y_true, y_pred)
	rmse = root_mean_squared_error(y_true, y_pred)
	r2 = r2_score(y_true, y_pred)
	metrics_out[set] = [
        int(len(y_true)), float(mae), float(rmse), float(r2)
    ]

	# -------------------------

	return None

def out_metrics(
	metrics_out: dict,
	ml_task: Literal['classification', 'regression']
) -> pd.DataFrame:
    
	# Classification
	if ml_task == 'classification':
		return pd.DataFrame(
            metrics_out,
            index=['Size', 'Accuracy', 'Precision', 'Recall', 'F1']
        ).T

	# Regression
	elif ml_task == 'regression':
		return pd.DataFrame(
            metrics_out,
            index=['Size', 'MAE', 'RMSE', 'R2']
        ).T

def out_cm(
	y_true: np.ndarray,
	y_pred: np.ndarray,
	model_classes: list,
	display_labels: list
) -> None:

    # Confusion Matrix
    cm = confusion_matrix(
		y_true, y_pred,
		labels=model_classes
	)
    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=display_labels
    )
    display.plot(cmap='Blues', values_format='d')
    plt.title('Confusion Matrix')
    plt.show()

# -------------------------
