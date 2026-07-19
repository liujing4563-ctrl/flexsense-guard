# FlexSense-Guard engineering guardrails

## Scope and sequencing

- Work on one dominant flexible joint only.
- Complete and review one phase per branch and pull request.
- Do not start classification, control, SIL, UI, or test-agent work until the
  72-hour feasibility probe records a decision.
- Do not add patent, competition-confidential, or personal data while the repository
  is public.

## Data-contract rules

- Use `estimated_external_torque_nm`; do not infer or expose terminal force without
  a declared Jacobian or moment arm.
- `confidence_score` is an engineering score, not a statistical probability.
- `contact_score` is an evidence score, not a contact probability. Do not introduce
  `contact_probability`.
- Plant truth is evaluation-only and must never be provided to an observer input.
- Keep plant parameters and observer nominal parameters separate.

## Engineering rules

- Keep Python code typed and covered by focused pytest tests.
- State whether MATLAB/Octave and C/SIL checks were run; never imply unrun checks
  passed.
- Use Chinese documentation and refer to contributors as “同学”.
- Preserve generated outputs outside source control unless an explicit `.gitkeep` is
  needed.
