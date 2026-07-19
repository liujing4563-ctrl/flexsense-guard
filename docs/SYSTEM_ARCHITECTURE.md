# System Architecture

## Overview

FlexSense Guard is organized as a deterministic pipeline:

```text
Scenario config -> Plant simulator -> Signal conditioning -> Force estimator
                                      -> Safety controller -> Actuator command
                         \\-> Telemetry, metrics, and reproducibility record
```

## Components

### Scenario and configuration

Owns robot parameters, controller limits, disturbance profiles, sample time, and random seed. Configuration is immutable during a run.

### Plant simulator

Models joint kinematics, flexible-joint dynamics, actuator behavior, friction, sensor noise, and external disturbances. It exposes measured signals and ground-truth force only for evaluation.

### Signal conditioning

Applies unit normalization, timestamp validation, filtering, and missing-data checks. It must not silently repair invalid samples.

### Force estimator

Consumes conditioned actuator-side and motion signals and returns an estimated external force with uncertainty and status metadata. Ground-truth force is unavailable to this component during normal execution.

### Safety controller

Combines the estimate, uncertainty, joint state, and configured limits to produce a bounded command. It enters a conservative safe state when inputs are stale, invalid, or outside the validated operating envelope.

### Telemetry and evaluation

Records inputs, outputs, timing, configuration hash, seed, estimator error, constraint violations, and termination reason. Evaluation code is separate from runtime control code.

## Boundary rules

- Runtime modules communicate through typed records defined in `API_SPEC.md`.
- Time is monotonic and represented in seconds.
- Angles use radians, angular velocity uses radians per second, torque uses newton-metres, and force uses newtons.
- The runtime never uses evaluation-only ground truth.
- Safety limits are centralized and applied at the final command boundary.
