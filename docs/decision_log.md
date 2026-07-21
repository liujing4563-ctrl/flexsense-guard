# 决策日志

本文件记录影响项目范围、路线、公共契约、阶段门或职责边界的重大决定。算法内部
实现选择由对应模块文档记录。

## 记录模板

```text
Decision ID:
Date:
Problem:
Options:
Decision:
Evidence:
Owner:
Affected files:
Reversal condition:
```

## DEC-001：修正 P1 当前技术状态

- **Date**：2026-07-21
- **Problem**：历史 P1 运行失败能否直接作为当前路线失败结论。
- **Options**：保持 `FAIL`；或拆分历史执行结果、证据有效性和当前技术结论。
- **Decision**：历史执行结果保留 `FAIL`；证据有效性为
  `INVALID / INSUFFICIENT`；当前 P1 可行性结论改为 `NOT_VERIFIED`。
- **Evidence**：旧实验存在力矩侧未冻结、Plant/Observer 输入不一致、单负载、
  单场景、单 seed 和调参与评价未隔离问题。
- **Owner**：项目负责人同学。
- **Affected files**：项目、架构、验证和当前状态文档。
- **Reversal condition**：模型和输入契约修复后，新的有效、充分且可复现实验形成
  `PASS` 或 `FAIL` 证据。

## DEC-002：冻结负载侧弹性力矩语义

- **Date**：2026-07-21
- **Problem**：`tau_s` 所在侧和齿轮反射关系不明确。
- **Decision**：使用 `tau_s_load_nm` 表示负载侧弹性力矩；理想效率下反射到电机
  侧的力矩为 `tau_s_load_nm / N`。
- **Evidence**：统一动力学定义和无耗散能量一致性要求。
- **Owner**：项目负责人同学；Simulink 同学共同确认实现。
- **Affected files**：`docs/02_architecture/**`、后续 Plant/Observer 实现。
- **Reversal condition**：引入经过审查的效率、回差或其他传动模型，并完成新的
  能量推导和接口变更。

## DEC-003：拆分三类电机力矩字段

- **Date**：2026-07-21
- **Problem**：Plant 使用饱和后力矩而 Observer 使用原始指令，导致实验无效。
- **Decision**：公共输入区分 `torque_command_nm`、
  `motor_torque_applied_nm` 和 `motor_torque_measured_nm`；禁止 Observer 直接使用
  原始指令。
- **Evidence**：Plant 与 Observer 输入必须可追溯且物理一致。
- **Owner**：项目负责人同学维护契约；Simulink 同学迁移 MATLAB 实现。
- **Affected files**：公共文档、Schema、Python 类型和后续 MATLAB 信号结构。
- **Reversal condition**：无；只能通过版本化接口变更进一步细化，不能重新合并为
  含糊字段。

## DEC-004：按模块路径归属 Codex 产出

- **Date**：2026-07-21
- **Problem**：由项目负责人提交提示词是否意味着生成代码均属于负责人工作。
- **Decision**：代码责任按照所在模块和责任矩阵确定，不按提示词发起人确定。
- **Evidence**：模块负责同学必须解释实现、复现实验并承担交付质量。
- **Owner**：项目负责人同学。
- **Affected files**：职责、Issue、PR 和贡献规范。
- **Reversal condition**：团队正式调整人员或目录归属并更新责任矩阵。
