# 72-Hour Technical Probe

## Hypothesis

For a single flexible joint under bounded disturbances, actuator-side torque and motion signals can provide a useful external-force estimate while the safety controller remains within configured position, velocity, torque, and force limits.

## Scope

- One simulated flexible joint.
- Fixed sample time of 1 ms.
- Deterministic seeds plus a small noise sweep.
- Step, impulse, sinusoidal, and contact-like disturbances.
- No hardware claims.

## Schedule

### Hours 0-12: baseline

- Implement the plant and typed records.
- Verify units, timestamps, limits, and deterministic replay.
- Exit: two identical seeded runs produce identical telemetry hashes.

### Hours 12-36: estimator

- Implement a baseline model-based estimator.
- Measure force error, latency, and sensitivity to noise and parameter mismatch.
- Exit: estimator produces finite outputs and explicit invalid/stale statuses.

### Hours 36-60: safety loop

- Integrate estimator and safety controller.
- Inject stale data, saturation, out-of-range state, and estimator spikes.
- Exit: no command exceeds configured limits; all injected faults reach a safe mode.

### Hours 60-72: evaluation package

- Run the scenario matrix across seeds.
- Export metrics and failure traces.
- Document unresolved risks and next experiments.
- Exit: reproducible report with pass/fail evidence and known limitations.

## Metrics

- Force MAE and 95th-percentile absolute error.
- End-to-end loop latency and deadline misses.
- Maximum position, velocity, torque, and estimated force.
- Safe-stop detection latency.
- Deterministic replay success rate.

## Stop conditions

Stop the probe and record a failure if any command violates a configured limit, if timestamps move backward, if non-finite values reach the controller, or if replay diverges without a documented nondeterministic source.
