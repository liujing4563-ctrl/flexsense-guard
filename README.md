# FlexSense-Guard

Flexible-joint virtual sensing and safety-control simulation, using motor-side signals only.

## Current stage

PR-0 repository baseline has been merged. The first P1 feasibility probe has now
returned `fail`; the recorded evidence is in [`docs/probe_results.md`](docs/probe_results.md).
The project is therefore downscoped to motor-side control simulation. It does not
claim that virtual sensing, classification, controller logic, SIL, or an application
has been validated.

Some numbered directories were imported before this baseline was established. Treat
them as exploratory material only; later PRs must validate each module separately.

## Scope

- One dominant flexible joint with a dual-inertia digital plant.
- Motor-side position, velocity, current, and torque as observer inputs.
- Estimated load-side state and external disturbance **torque** as outputs.
- Normal tracking, vibration suppression, safe slowdown, and degraded modes.

The project excludes load-side sensor inputs, multi-robot systems, Kuramoto
synchronization, reinforcement learning, ROS/Gazebo/Isaac integration, hardware
claims, and industrial safety certification. This public repository contains no
patent-related material.

## Canonical documentation

The current documentation lives in [`docs/`](docs/). The historical `00_docs/`
directory is retained for traceability and is superseded by the corresponding files
under `docs/`.

Key documents:

- [`docs/project_charter.md`](docs/project_charter.md)
- [`docs/system_architecture.md`](docs/system_architecture.md)
- [`docs/interface_spec.md`](docs/interface_spec.md)
- [`docs/feasibility_probe_72h.md`](docs/feasibility_probe_72h.md)
- [`docs/scope_and_non_goals.md`](docs/scope_and_non_goals.md)

## Python smoke check

```bash
python -m pip install -e ".[dev]"
python -m pytest python/tests -q
```

MATLAB/Octave and C/SIL checks are intentionally not run or claimed by PR-0.

## Delivery sequence

1. PR-0: repository baseline and executable data contract — complete.
2. P1 feasibility probe: load-side estimation — failed; see the recorded result.
3. Further virtual-sensing development is blocked pending a separately reviewed
   restart decision. Classification, control, SIL, application, and test-agent work
   are not authorized by the failed probe.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before creating a branch or pull request.
