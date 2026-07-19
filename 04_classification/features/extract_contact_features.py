"""Feature extraction for vibration-contact classification.

This module provides functions to extract time-domain and frequency-domain
features from the EKF innovation signal and estimated torque for use in
the rule-based classifier.

Typical usage:
    features = extract_contact_features(innovation_norm, tau_ext_est, dt)
"""

import numpy as np


def extract_contact_features(
    innovation_norm: np.ndarray,
    tau_ext_est: np.ndarray,
    dt: float,
) -> dict[str, float]:
    """Extract features from innovation and torque signals.

    Args:
        innovation_norm: L2 norm of EKF innovation vector over time window.
        tau_ext_est: Estimated external torque over time window [Nm].
        dt: Sampling time [s].

    Returns:
        Dictionary of extracted features:
            - innovation_mean: Mean innovation norm.
            - innovation_std: Standard deviation of innovation norm.
            - innovation_peak: Peak innovation norm.
            - tau_ext_mean: Mean estimated external torque [Nm].
            - tau_ext_std: Standard deviation of estimated torque [Nm].
            - tau_ext_peak: Peak estimated torque [Nm].
            - tau_ext_energy: Energy proxy (sum of squared torque) [Nm^2].
            - zero_crossing_rate: Zero-crossing rate of innovation [Hz].

    Raises:
        ValueError: If input arrays have different lengths or dt <= 0.
    """
    if len(innovation_norm) != len(tau_ext_est):
        raise ValueError(
            f"Innovation and torque arrays must have same length, "
            f"got {len(innovation_norm)} vs {len(tau_ext_est)}"
        )
    if dt <= 0:
        raise ValueError(f"dt must be positive, got {dt}")

    n = len(innovation_norm)

    features: dict[str, float] = {}

    # Time-domain features from innovation
    features["innovation_mean"] = float(np.mean(innovation_norm))
    features["innovation_std"] = float(np.std(innovation_norm))
    features["innovation_peak"] = float(np.max(innovation_norm))

    # Time-domain features from estimated torque
    features["tau_ext_mean"] = float(np.mean(tau_ext_est))
    features["tau_ext_std"] = float(np.std(tau_ext_est))
    features["tau_ext_peak"] = float(np.max(np.abs(tau_ext_est)))
    features["tau_ext_energy"] = float(np.sum(tau_ext_est**2))

    # Zero-crossing rate of innovation
    signs = np.sign(innovation_norm - np.mean(innovation_norm))
    zero_crossings = np.sum(np.abs(np.diff(signs)) > 0)
    features["zero_crossing_rate"] = float(zero_crossings / (n * dt))

    return features
