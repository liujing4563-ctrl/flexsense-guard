# FlexSense-Guard

Flexible-joint virtual sensing and safety-control simulation, using motor-side signals only.

## Current stage

The repository is at the **PR-0 repository-baseline** stage. This stage defines the
project boundary, data contract, collaboration rules, and a small executable Python
contract. It does not claim that the plant, observer, classifier, controller, SIL,
or application has been validated.

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

1. PR-0: repository baseline and executable data contract.
2. PR-1: dual-inertia plant.
3. PR-2: baseline observer.
4. PR-3: confidence and trigger probe.
5. PR-4+: classification, control, SIL, application, and material freeze only after
   the 72-hour probe has a documented decision.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before creating a branch or pull request.
