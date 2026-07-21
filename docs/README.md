# 文档索引

本目录是 FlexSense-Guard 的规范来源。`00_docs/` 仅保留历史追溯价值。

## 快速入口

- [`current_status_and_next_steps.md`](current_status_and_next_steps.md)：当前完成情况、下一动作和每位同学的立即任务

## `01_project`：项目定义与治理

- [`project_charter.md`](01_project/project_charter.md)：目标、阶段门与声明边界
- [`scope_and_non_goals.md`](01_project/scope_and_non_goals.md)：范围与明确排除项
- [`risk_register.md`](01_project/risk_register.md)：项目风险、触发信号与降级条件

## `02_architecture`：架构与公共契约

- [`system_architecture.md`](02_architecture/system_architecture.md)：模块边界和数据流
- [`interface_spec.md`](02_architecture/interface_spec.md)：输入输出契约、枚举和单位
- [`glossary_and_symbols.md`](02_architecture/glossary_and_symbols.md)：术语、符号、所在侧和单位
- [`cross_language_contract.md`](02_architecture/cross_language_contract.md)：文档、JSON、Python、MATLAB、C 和 App 迁移状态
- [`confidence_design_spec.md`](02_architecture/confidence_design_spec.md)：可信评分结构和待实验参数
- [`event_trigger_calibration_spec.md`](02_architecture/event_trigger_calibration_spec.md)：事件触发、验收和回退规则
- [`mode_manager_spec.md`](02_architecture/mode_manager_spec.md)：模式优先级、转换和恢复规则

## `03_validation`：探针与实验验证

- [`feasibility_probe_72h.md`](03_validation/feasibility_probe_72h.md)：探针、阶段门与降级决策
- [`experiment_protocol.md`](03_validation/experiment_protocol.md)：可复现实验规则
- [`acceptance_matrix.md`](03_validation/acceptance_matrix.md)：P1/P2/P3 和集成验收矩阵
- [`metric_definitions.md`](03_validation/metric_definitions.md)：指标公式、单位和聚合规则
- [`evidence_management.md`](03_validation/evidence_management.md)：结果目录、元数据和证据有效性
- [`probe_results.md`](03_validation/probe_results.md)：技术探针执行记录

## `04_collaboration`：职责与协作交付

- [`team_responsibilities.md`](04_collaboration/team_responsibilities.md)：同学间职责边界
- [`issue_backlog.md`](04_collaboration/issue_backlog.md)：阶段任务映射
- [`p1_model_input_handoff.md`](04_collaboration/p1_model_input_handoff.md)：P1 模型和输入一致性修复交接单
- [`repository_cleanup_log.md`](04_collaboration/repository_cleanup_log.md)：旧 PR、stash 和分支迁移风险
- [`git_workflow.md`](04_collaboration/git_workflow.md)：分支与 PR 工作流

## 跨类别治理记录

- [`decision_log.md`](decision_log.md)：影响范围、路线、契约、门禁和职责的重大决策

所有当前规范使用简体中文。路径、命令、代码标识、枚举和标准技术名称保持原样，
避免翻译造成跨语言接口歧义。
