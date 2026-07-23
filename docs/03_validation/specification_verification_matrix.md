# 规范验证矩阵

本矩阵记录规范是否获得对应真人审查，不记录算法性能结论。当前状态的唯一权威
来源仍是
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md)。

截至 2026-07-24，PR #16 没有已提交的真人 Review。Codex 检查、Python 测试和
Schema 校验均不能替代模块负责人批准，因此下表保持 `HUMAN REVIEW PENDING`。

| ID | 审查项 | 规范文件 | 审查人 | 审查方法 | 所需证据 | 当前状态 | 阻塞项 |
|---|---|---|---|---|---|---|---|
| SV-01 | 数学模型语义 | `system_architecture.md`、`glossary_and_symbols.md` | Simulink 同学 | 独立推导并逐项标记 | 带符号方程、状态定义和 Review 评论 | `HUMAN REVIEW PENDING` | 尚无 Simulink 真人意见 |
| SV-02 | 齿轮比和力矩反射 | `system_architecture.md`、`interface_spec.md` | Simulink 同学 | 虚功、功率和无耗散能量复核 | 两侧力矩推导及能量测试计划 | `HUMAN REVIEW PENDING` | 尚无独立推导和测试方案 |
| SV-03 | `ObserverInput` 边界 | `interface_spec.md`、`cross_language_contract.md` | Simulink 同学 | DTO 字段逐项审查和真值泄漏检查 | MATLAB 映射建议、禁止字段清单 | `HUMAN REVIEW PENDING` | MATLAB 输入链仍为 `INVALID` |
| SV-04 | P1-V 设计 | `feasibility_probe_72h.md`、`acceptance_matrix.md` | Simulink 同学、项目负责人同学 | 审查输入、负载、seed、门限预注册和证据 | P1-V 测试计划及待确认门限 | `HUMAN REVIEW PENDING` | 速度和部分绝对门限尚未批准 |
| SV-05 | P1-A 设计 | `feasibility_probe_72h.md`、`experiment_protocol.md` | Simulink 同学、项目负责人同学 | 审查 baseline、公平比较和评价隔离 | P1-A 测试计划、数据划分和退出条件 | `HUMAN REVIEW PENDING` | MATLAB runner 尚未迁移 |
| SV-06 | P2 场景和标签 | `acceptance_matrix.md`、`metric_definitions.md`、并行准备计划 | 通感算同学、项目负责人同学 | 场景表、标签和事件级指标审查 | 数据需求、混淆场景和阻塞项 | `HUMAN REVIEW PENDING` | P2 正式开发被 P1-V 阻断 |
| SV-07 | App 字段映射 | `interface_spec.md`、`evidence_management.md`、并行准备计划 | 软件同学 | Mock 回放、字段与无效状态逐项映射 | 页面映射表和 Mock 标识规则 | `HUMAN REVIEW PENDING` | App 映射为 `MISSING` |
| SV-08 | C/SIL 字段映射 | `cross_language_contract.md`、`interface_spec.md`、并行准备计划 | Linux 同学 | DTO 到 C 类型、版本和异常策略审查 | C 映射表、回放和测试计划 | `HUMAN REVIEW PENDING` | C 映射为 `MISSING`，无有效 MATLAB 参考 |
| SV-09 | Validation Schema | `evidence_management.md`、`validation_report.schema.json` | 软件或 Linux 同学 | 跨语言解析、阶段 payload 和 N/A 省略检查 | 映射意见、示例校验和不兼容策略 | `HUMAN REVIEW PENDING` | 尚无非作者跨语言审查 |
| SV-10 | Mode 与危险锁存 | `mode_manager_spec.md`、`interface_spec.md` | 项目负责人同学及非作者模块同学 | 单写者、清除权限和保守恢复场景审查 | 状态转换表、异常场景意见 | `HUMAN REVIEW PENDING` | Safety Supervisor 尚无主体实现 |
| SV-11 | 当前状态与 A/B/C 路线 | `current_status_and_next_steps.md`、`project_charter.md` | 项目负责人同学，至少一位非作者模块同学复核 | 检查历史证据、当前决定、子门阻断和路线退出条件 | 项目负责人状态审查记录及非作者 Review | `HUMAN REVIEW PENDING` | 尚无非作者对最终状态和路线的复核 |

审查结果只允许：

```text
APPROVE
NEEDS_REVISION
NOT_SURE
```

只有真实审查人提交意见后，才可把对应行更新为上述结果。不得由 Codex 代填人工
批准，也不得把 `HUMAN REVIEW PENDING` 解释为规范失败。
