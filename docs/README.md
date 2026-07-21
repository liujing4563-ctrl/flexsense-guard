# 文档索引

本目录是 FlexSense-Guard 的规范来源。`00_docs/` 仅保留历史追溯价值。

规范成熟度、实现完整度和验证结论是三套独立状态。当前阶段状态只以
[`current_status_and_next_steps.md`](current_status_and_next_steps.md) 为准；其他文档
说明规则或历史证据，不重复维护当前状态表。

## 快速入口

- [`current_status_and_next_steps.md`](current_status_and_next_steps.md)：当前完成情况、下一动作和每位同学的立即任务

## `01_project`：项目定义与治理

- [`project_charter.md`](01_project/project_charter.md)：目标、阶段门与声明边界
- [`scope_and_non_goals.md`](01_project/scope_and_non_goals.md)：范围与明确排除项
- [`risk_register.md`](01_project/risk_register.md)：项目风险、触发信号与降级条件

## `02_architecture`：架构与公共契约

- [`system_architecture.md`](02_architecture/system_architecture.md)：模块边界和数据流
- [`interface_spec.md`](02_architecture/interface_spec.md)：v2 DTO、输入输出契约、枚举和单位
- [`glossary_and_symbols.md`](02_architecture/glossary_and_symbols.md)：术语、符号、所在侧和单位
- [`cross_language_contract.md`](02_architecture/cross_language_contract.md)：文档、JSON、Python、MATLAB、C 和 App 迁移状态
- [`confidence_design_spec.md`](02_architecture/confidence_design_spec.md)：可信评分结构和待实验参数
- [`event_trigger_calibration_spec.md`](02_architecture/event_trigger_calibration_spec.md)：事件触发、验收和回退规则
- [`mode_manager_spec.md`](02_architecture/mode_manager_spec.md)：模式优先级、转换和恢复规则

## `03_validation`：探针与实验验证

- [`feasibility_probe_72h.md`](03_validation/feasibility_probe_72h.md)：探针、阶段门与降级决策
- [`experiment_protocol.md`](03_validation/experiment_protocol.md)：可复现实验规则
- [`acceptance_matrix.md`](03_validation/acceptance_matrix.md)：P1/P2/P3 子门和集成验收矩阵
- [`metric_definitions.md`](03_validation/metric_definitions.md)：指标公式、单位和聚合规则
- [`evidence_management.md`](03_validation/evidence_management.md)：阶段化报告、结果目录和证据有效性
- [`probe_results.md`](03_validation/probe_results.md)：技术探针执行记录

## `04_collaboration`：职责与协作交付

- [`team_responsibilities.md`](04_collaboration/team_responsibilities.md)：同学间职责边界
- [`issue_backlog.md`](04_collaboration/issue_backlog.md)：阶段任务映射
- [`git_workflow.md`](04_collaboration/git_workflow.md)：分支与 PR 工作流
- [`pr15_pr16_overlap_analysis.md`](04_collaboration/pr15_pr16_overlap_analysis.md)：两个 Draft PR 的文件重叠、顺序和回退风险

## 跨类别治理记录

- [`decision_log.md`](decision_log.md)：影响范围、路线、契约、门禁和职责的重大决策

所有当前规范使用简体中文。路径、命令、代码标识、枚举和标准技术名称保持原样，
避免翻译造成跨语言接口歧义。
