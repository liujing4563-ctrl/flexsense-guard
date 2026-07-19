# Initial API Specification

The bootstrap API is language-neutral and can be implemented in Python first.

## `SimulationConfig`

```yaml
sample_time_s: 0.001
duration_s: 10.0
random_seed: 42
joint:
  inertia_kg_m2: 0.01
  stiffness_nm_per_rad: 2.0
  damping_nm_s_per_rad: 0.02
safety:
  max_abs_position_rad: 1.57
  max_abs_velocity_rad_s: 4.0
  max_abs_torque_nm: 1.5
  max_force_n: 20.0
```

## `MeasurementFrame`

```yaml
timestamp_s: 0.0
position_rad: 0.0
velocity_rad_s: 0.0
torque_nm: 0.0
sequence: 0
valid: true
```

## `ForceEstimate`

```yaml
timestamp_s: 0.0
force_n: 0.0
uncertainty_n: 0.0
status: "ok" # ok | stale | invalid | out_of_range
```

## `SafetyCommand`

```yaml
timestamp_s: 0.0
torque_nm: 0.0
mode: "normal" # normal | limited | safe_stop
reason: null
```

## Contract requirements

- Timestamps must be finite and strictly non-decreasing per stream.
- A stale measurement must not produce a normal command.
- Commands must satisfy configured absolute limits after all controller logic.
- Invalid numeric values must result in `safe_stop`.
- Each response carries the input timestamp or an explicit failure reason.
