# FlexSense Guard Project Charter

## Mission

Build a reproducible simulation platform for virtual force sensing and safety control of flexible robot joints without load-side force sensors.

## Initial objectives

1. Define a deterministic joint and contact simulation baseline.
2. Estimate external interaction force from motion and actuator-side signals.
3. Enforce safety constraints through a clearly testable control loop.
4. Produce traceable experiments, metrics, and failure reports.

## Non-goals for the bootstrap phase

- Hardware deployment or claims of production safety certification.
- Support for every robot morphology or simulator.
- Online learning in the first prototype.

## Success criteria

- A new contributor can run the baseline simulation from a clean checkout.
- Every experiment records configuration, seed, software version, and metrics.
- The estimator and safety controller have unit and scenario-level tests.
- Unsafe or invalid input is rejected at the interface boundary.

## Working principles

- Reproducibility over opaque performance claims.
- Explicit units, coordinate frames, assumptions, and limits.
- Simulation evidence before hardware-facing recommendations.
- Small, reviewable changes with one purpose per pull request.

## Bootstrap deliverables

- System architecture and module boundaries.
- Versioned API and data contracts.
- A 72-hour technical probe with measurable exit criteria.
- Initial issue backlog covering simulation, estimation, safety, validation, and documentation.
