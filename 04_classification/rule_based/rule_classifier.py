"""Rule-based classifier for normal/vibration/contact discrimination.

This module implements a simple threshold-based classifier that uses
features extracted from the EKF innovation and estimated torque signals
to classify the current joint state into one of three categories:
    - 'normal': Normal operation.
    - 'vibration': Flexible vibration (oscillatory, non-impact).
    - 'contact': External contact/impact.

The classifier uses heuristics only and explicitly does NOT claim
reliable collision detection. It is a baseline for the 72h probe.
"""

from dataclasses import dataclass, field


@dataclass
class ClassifierConfig:
    """Configuration parameters for the rule classifier.

    Attributes:
        innovation_normal_max: Max innovation norm for 'normal' class.
        innovation_vibration_min: Min innovation norm for 'vibration' class.
        tau_ext_impact_min: Min estimated torque for 'contact' class.
        tau_ext_oscillation_min: Min torque std for 'vibration' class.
        zero_crossing_vibration_min: Min zero-crossing rate for 'vibration' [Hz].
    """
    innovation_normal_max: float = 0.5
    innovation_vibration_min: float = 0.3
    tau_ext_impact_min: float = 1.0
    tau_ext_oscillation_min: float = 0.3
    zero_crossing_vibration_min: float = 5.0


@dataclass
class ClassificationResult:
    """Result of a single classification.

    Attributes:
        label: 'normal', 'vibration', or 'contact'.
        contact_score: Contact likelihood score [0, 1] (NOT probability).
        confidence: Confidence in this classification [0, 1].
    """
    label: str
    contact_score: float
    confidence: float


class RuleClassifier:
    """Rule-based classifier for joint state discrimination.

    The classifier uses threshold-based rules on extracted features.
    It is intentionally simple for the 72h probe phase.

    Usage:
        classifier = RuleClassifier()
        result = classifier.classify(features)
    """

    def __init__(self, config: ClassifierConfig | None = None) -> None:
        """Initialize the classifier with optional custom config.

        Args:
            config: Classifier configuration. Uses defaults if None.
        """
        self.config = config or ClassifierConfig()

    def classify(self, features: dict[str, float]) -> ClassificationResult:
        """Classify the current joint state based on extracted features.

        Args:
            features: Dictionary of features from extract_contact_features().

        Returns:
            ClassificationResult with label, contact_score, and confidence.
        """
        innovation_peak = features.get("innovation_peak", 0.0)
        tau_ext_peak = features.get("tau_ext_peak", 0.0)
        tau_ext_std = features.get("tau_ext_std", 0.0)
        zcr = features.get("zero_crossing_rate", 0.0)

        # Default: normal
        label = "normal"
        contact_score = 0.0
        confidence = 0.8

        # Check for impact (high peak torque + high innovation)
        if (
            tau_ext_peak > self.config.tau_ext_impact_min
            and innovation_peak > self.config.innovation_normal_max
        ):
            label = "contact"
            # Contact score proportional to peak torque, capped at 1.0
            contact_score = min(1.0, tau_ext_peak / (2 * self.config.tau_ext_impact_min))
            confidence = 0.7

        # Check for vibration (oscillation pattern)
        elif (
            tau_ext_std > self.config.tau_ext_oscillation_min
            and zcr > self.config.zero_crossing_vibration_min
            and innovation_peak > self.config.innovation_vibration_min
        ):
            label = "vibration"
            contact_score = 0.3  # Low contact score, but not normal
            confidence = 0.6

        # Normal operation
        else:
            if innovation_peak < self.config.innovation_normal_max:
                confidence = 0.9
            else:
                confidence = 0.5

        return ClassificationResult(
            label=label,
            contact_score=contact_score,
            confidence=confidence,
        )
