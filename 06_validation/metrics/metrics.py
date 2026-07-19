"""Metrics computation for FlexSense-Guard validation.

This module provides Python implementations of standard evaluation metrics
used for the 72h feasibility probes.
"""

import numpy as np


def compute_rmse(true: np.ndarray, estimated: np.ndarray) -> float:
    """Compute Root Mean Square Error between true and estimated signals.

    Args:
        true: Ground truth signal array.
        estimated: Estimated signal array.

    Returns:
        RMSE value.

    Raises:
        ValueError: If arrays have different lengths.
    """
    if len(true) != len(estimated):
        raise ValueError(
            f"Arrays must have same length, got {len(true)} vs {len(estimated)}"
        )
    return float(np.sqrt(np.mean((true - estimated) ** 2)))


def compute_detection_metrics(
    detections: np.ndarray,
    ground_truth: np.ndarray,
) -> dict[str, int | float]:
    """Compute detection performance metrics.

    Args:
        detections: Binary detection signal (1 = detected, 0 = not detected).
        ground_truth: Binary ground truth contact signal (1 = contact, 0 = none).

    Returns:
        Dictionary with:
            - false_alarm_count: Number of false alarms.
            - missed_detection_count: Number of missed detections.
            - true_positive_count: Number of true positives.
            - true_negative_count: Number of true negatives.
            - false_positive_rate: False positive rate (if TN+FP > 0).
            - false_negative_rate: False negative rate (if TP+FN > 0).

    Raises:
        ValueError: If arrays have different lengths.
    """
    if len(detections) != len(ground_truth):
        raise ValueError(
            f"Arrays must have same length, got {len(detections)} vs {len(ground_truth)}"
        )

    detections = detections.astype(bool)
    ground_truth = ground_truth.astype(bool)

    tp = int(np.sum(detections & ground_truth))
    fp = int(np.sum(detections & ~ground_truth))
    fn = int(np.sum(~detections & ground_truth))
    tn = int(np.sum(~detections & ~ground_truth))

    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        "false_alarm_count": fp,
        "missed_detection_count": fn,
        "true_positive_count": tp,
        "true_negative_count": tn,
        "false_positive_rate": float(fpr),
        "false_negative_rate": float(fnr),
    }
