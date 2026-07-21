# PR #15 与 PR #16 重叠分析

检查日期：2026-07-21。由于本地 `gh` 不可用，本记录以 `origin/main`、
`chore/p1-simulink-handoff`、`feat/project-lead-control-specs` 及 PR #16 当前工作树候选
差异计算。它只分析，不合并、不关闭任何 PR。

## PR #15 独有文件

```text
.github/PULL_REQUEST_TEMPLATE.md
01_plant/simulink/README.md
docs/04_collaboration/p1_model_input_handoff.md
docs/04_collaboration/repository_cleanup_log.md
```

## PR #16 独有文件

```text
AGENTS.md
CONTRIBUTING.md
README.md
common/schemas/actuator_command.schema.json
common/schemas/artifact_index_entry.schema.json
common/schemas/calibration_candidate.schema.json
common/schemas/calibration_decision.schema.json
common/schemas/classification_output.schema.json
common/schemas/confidence_output.schema.json
common/schemas/contract_common.schema.json
common/schemas/control_command.schema.json
common/schemas/immutable_plant_true_config.schema.json
common/schemas/integration_validation_result.schema.json
common/schemas/mode_decision.schema.json
common/schemas/motor_side_measurement.schema.json
common/schemas/nominal_parameter_version.schema.json
common/schemas/observer_estimate.schema.json
common/schemas/observer_input.schema.json
common/schemas/p1_validation_result.schema.json
common/schemas/p2_validation_result.schema.json
common/schemas/p3_validation_result.schema.json
common/schemas/plant_input_trace.schema.json
common/schemas/raw_motor_measurement.schema.json
common/schemas/scenario_config.schema.json
common/schemas/signal_health_status.schema.json
common/schemas/sil_validation_result.schema.json
common/schemas/system_state.schema.json
common/schemas/system_state_snapshot.schema.json
common/schemas/torque_feedback.schema.json
common/schemas/validation_report.schema.json
common/schemas/validation_report_envelope.schema.json
configs/README.md
configs/mock/README.md
configs/mock/actuator_command_example.json
configs/mock/artifact_index_entry_example.json
configs/mock/calibration_candidate_example.json
configs/mock/calibration_decision_example.json
configs/mock/control_command_example.json
configs/mock/motor_side_measurement_example.json
configs/mock/nominal_parameter_version_example.json
configs/mock/observer_input_example.json
configs/mock/plant_input_trace_example.json
configs/mock/raw_motor_measurement_example.json
configs/mock/signal_health_status_example.json
configs/mock/system_state_contact.json
configs/mock/system_state_low_confidence.json
configs/mock/system_state_normal.json
configs/mock/system_state_vibration.json
configs/mock/torque_feedback_example.json
configs/mock/validation_report_example.json
docs/01_project/project_charter.md
docs/01_project/risk_register.md
docs/01_project/scope_and_non_goals.md
docs/02_architecture/confidence_design_spec.md
docs/02_architecture/cross_language_contract.md
docs/02_architecture/event_trigger_calibration_spec.md
docs/02_architecture/glossary_and_symbols.md
docs/02_architecture/mode_manager_spec.md
docs/03_validation/acceptance_matrix.md
docs/03_validation/evidence_management.md
docs/03_validation/metric_definitions.md
docs/03_validation/probe_results.md
docs/04_collaboration/git_workflow.md
docs/04_collaboration/team_responsibilities.md
docs/decision_log.md
python/flexsense_guard/__init__.py
python/flexsense_guard/types.py
python/tests/conftest.py
python/tests/test_contract_schema.py
python/tests/test_dto_boundaries.py
python/tests/test_enum_consistency.py
python/tests/test_forbidden_fields.py
python/tests/test_import.py
python/tests/test_mock_schema.py
python/tests/test_public_contract.py
python/tests/test_schema_examples.py
python/tests/test_validation_report_contract.py
```

其中旧 `motor_side_measurement`、旧 `system_state` Schema 和旧 Mock 在 PR #16 中是
删除项，不是继续保留的当前接口。

## 重叠文件

```text
docs/02_architecture/interface_spec.md
docs/02_architecture/system_architecture.md
docs/03_validation/experiment_protocol.md
docs/03_validation/feasibility_probe_72h.md
docs/04_collaboration/issue_backlog.md
docs/README.md
docs/current_status_and_next_steps.md
```

## 定义新旧判断

PR #16 包含更新定义：三层状态体系、v2 DTO、真值配置隔离、P1-V/P1-A、P2/P3
子门、`P1_REFRAME_REVIEW`、危险锁存、阶段化报告和不适用字段省略规则。PR #15 的
价值主要是 Simulink 交接单、仓库清理记录和模型实现接手说明。

## 推荐顺序与风险

1. 先完成 PR #16 的 Simulink 同学及至少一位非作者审查；
2. PR #16 审查通过后再按治理流程合并；
3. 将 PR #15 rebase 或等价同步到更新后的 `main`；
4. 对七个重叠文件逐项确认没有恢复旧 DTO、旧状态表或未拆分 P1 门禁；
5. 保留 PR #15，不自动关闭或合并。

若 PR #15 未同步就后合并，存在状态回退、旧契约复活和 P1/P2 边界再次混淆的风险。
若团队决定先处理 PR #15，则 PR #16 必须 rebase 并重新执行全部契约与链接检查。
