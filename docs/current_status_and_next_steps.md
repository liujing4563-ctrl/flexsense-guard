# 当前状态与下一步

本文件是项目当前阶段状态的唯一权威来源。其他文档定义规则、模型和长期路线，
不得重复维护详细当前状态。快照日期：2026-07-24。

## 状态体系

三类状态必须分开使用：

| 层级 | 允许值 | 含义 |
|---|---|---|
| Specification Status | `DRAFT`、`REVIEWED`、`APPROVED`、`FROZEN` | 规范从草案、审查、批准到正式冻结的治理状态 |
| Implementation Status | `MISSING`、`PLACEHOLDER`、`PARTIAL`、`IMPLEMENTED`、`INVALID` | 代码或跨语言映射的实际落地状态 |
| Verification Status | `NOT_RUN`、`NOT_VERIFIED`、`PASS`、`FAIL` | 实际执行和证据结论 |

`PROVISIONAL` 只修饰尚待依据确认的工程门限，不表示规范、实现或验证状态。
未确定的数值写“尚未确定，需要有效实验或应用需求依据”，不把 `TBD` 当作状态。

## 当前权威状态

| 工作部分 | 状态层级 | 当前状态 | 说明 |
|---|---|---|---|
| Project scope specification | Specification | `APPROVED` | 单关节范围、非目标和分阶段路线已经批准 |
| Mathematical semantics specification | Specification | `REVIEWED` | 理想齿轮、负载侧弹性力矩和能量关系已审查；仍等待 Simulink 同学共同确认及实现验证 |
| Cross-language interface specification | Specification | `REVIEWED` | DTO、字段、单位、失效规则和 v1→v2 迁移表已审查；仍待跨语言模块负责人批准 |
| Python/Schema contract implementation | Implementation | `IMPLEMENTED` | 当前分支契约测试已通过；不代表算法实现或跨语言迁移完成 |
| Cross-language implementation | Implementation | `PARTIAL` | MATLAB 为 `INVALID`，C 和 App 为 `MISSING` |
| MATLAB Plant/EKF implementation | Implementation | `INVALID` | 仍使用旧力矩反射和旧输入链，等待 Simulink 同学修复 |
| Confidence target implementation | Implementation | `INVALID` | 仓库存在旧实现，但不符合当前规范 |
| Calibration target implementation | Implementation | `INVALID` | 仓库存在旧实现，但不符合当前规范 |
| Mode Manager target implementation | Implementation | `INVALID` | 仓库存在旧实现，但不符合当前规范 |
| Historical P1 execution result | Verification | `FAIL` | 旧脚本曾运行失败 |
| Historical P1 evidence validity | Verification | `INVALID / INSUFFICIENT` | 模型、输入和实验覆盖存在确定性缺陷 |
| Current P1 feasibility decision | Verification | `NOT_VERIFIED` | P1-V 和 P1-A 均未形成有效证据 |
| P2 | Verification | `BLOCKED` | P1-V 尚未通过 |
| P3 | Verification | `BLOCKED` | P1-V 尚未通过；涉及接触的部分还依赖 P2-CONTACT |

不得把数学规范写成 `VERIFIED`，不得把 Python/Schema 契约测试解释为 MATLAB、
Observer、Confidence、Calibration 或 Mode Manager 已经实现。

## 当前能力声明边界

- 当前不存在经过验证的 Python/MATLAB 端到端闭环；
- 当前不存在经过验证的安全控制结论；
- 当前没有开始正式 P2/P3 实验；
- 团队并行准备框架已形成部分文档交付，状态为 `PARTIAL`，仍待真人审查和各模块
  第一阶段交付，不能解释为任何主体模块已实现。

## 阶段门结构

| 阶段门 | 回答的问题 | 当前状态 |
|---|---|---|
| P1-V | 仅使用合法 Observer 输入时，负载侧位置和速度是否达到基本可用性 | `NOT_VERIFIED` |
| P1-A | Observer 相对电机侧直接映射是否具有稳定且有工程意义的优势 | `NOT_VERIFIED` |
| P2-VIB | 柔性振动是否可稳定辨识 | `BLOCKED` |
| P2-CONTACT | 外部接触是否可与正常动态和摩擦变化区分 | `BLOCKED` |
| P3-DEGRADE | 故障发生时可信评分和有效性是否正确下降 | `BLOCKED` |
| P3-ACTION | 低可信和接触危险是否触发正确的保守动作 | `BLOCKED` |
| P3-RECOVERY | 故障解除后是否按滞回和保持规则恢复 | `BLOCKED` |

P1 中可以记录外部扰动力矩误差作为诊断指标，但它不是 P1-V 或 P1-A 的强制门禁。
外部扰动和接触的可分辨性属于 P2。

## 路线状态

- A 路线要求 P1-V、P1-A、P2-VIB、P2-CONTACT 和三个 P3 子门全部通过。
- B 路线用于 P1-V 通过、但 P1-A、P2 或 P3 至少一项未通过的缩减交付；只保留
  已通过对应门禁的能力。
- `P1_REFRAME_REVIEW` 表示 P1-V 通过但 P1-A 未建立优势，只能选择
  `CONTINUE_TO_ROUTE_B`、一次 `ONE_BOUNDED_REPAIR` 或 `ENTER_ROUTE_C`。
- C 路线可由有效 P1-V 失败触发，也可由 `P1_REFRAME_REVIEW` 通过 Decision ID
  主动选择；后一种情况不能改写 P1-V 的真实结果。

## 下一项目动作

Draft PR #16 的修改范围现已收口，独立人工审查尚未完成，因此规范仍为 `REVIEWED`，
不得称为 `APPROVED` 或 `FROZEN`。从现在起该 PR 只接受审查意见修订、测试修复和
事实性纠错，不再新增 Schema、模式或规范主题。

非作者 Review 请求和角色化检查清单已经发出。当前首要动作是等待并处理 Simulink
同学对数学和 MATLAB 可实现性的审查，以及计算机软件或嵌入式 Linux 同学对跨语言
契约可实现性的审查。PR #16 获得对应批准并合并后，Simulink 同学再基于更新后的
`main` 同步 PR #15，确认数学模型并修复 MATLAB Plant、Observer 和 P1 输入链。

等待人工审查期间，全队可以按
[`team_parallel_preparation_plan.md`](04_collaboration/team_parallel_preparation_plan.md)
并行完成场景、字段映射、工具链、测试计划和交接清单。该工作只形成准备材料，不
启动主体算法，不改变 P1/P2/P3 状态。

P1 形成有效 `PASS` 证据前，其他同学只能进行接口审查和交付计划，不启动 P2/P3、
完整 App、C/SIL 或 Test Agent 主体开发。

## 每位同学当前任务

| 同学 | 主责路径 | 当前任务 | 禁止事项 |
|---|---|---|---|
| 项目负责人同学 | `docs/**`、`common/schemas/**`、`python/**` 及责任矩阵指定路径 | 处理 PR #16 Review；维护并行工作包、依赖、Issue 和审查矩阵 | 不修改 Plant、EKF、runner、分类器、App 或 C/SIL 主体 |
| Simulink 同学 | `01_plant/**`、`02_observer/**`、P1 runner、`results/p1/**` | 审查 PR #16；准备 MATLAB 文件影响清单和 P1 测试计划 | 准备任务中不改算法、Q/R/P 或 runner |
| 深度学习通感算同学 | `04_classification/**`、`09_test_agent/**` 及 P2 验证路径 | 准备 P2 场景、标签、信号需求、数据隔离和事件级评价 | P1-V 通过前不训练分类器或运行正式 P2/P3 |
| 计算机软件同学 | `configs/**`、报告和 `07_app/**` | 准备 Mock 驱动的只读页面、字段映射和无效状态方案 | 不把 Mock 当实验结果，不开发完整 App |
| 嵌入式 Linux 同学 | `08_sil/**` | 准备工具链、DTO 到 C 映射、回放和一致性测试方案 | 不添加 C/C++ 主体，不移植当前旧 Observer |

完整路径归属见
[`team_responsibilities.md`](04_collaboration/team_responsibilities.md)。

## PR #15 与 PR #16 协作结论

- 完整的 PR #15 独有、PR #16 独有和七个重叠文件清单见
  [`pr15_pr16_overlap_analysis.md`](04_collaboration/pr15_pr16_overlap_analysis.md)。
- PR #16 包含更新后的 DTO、阶段门和状态定义，应先完成审查并合并。
- PR #15 随后必须基于更新后的 `main` rebase 或等价同步，再人工解决文档冲突。
- 未同步就合并 PR #15 可能恢复旧字段、旧状态词或旧 P1 门禁，存在状态回退风险。
- 不自动关闭或合并任一 PR。

## 治理例外

PR #14 在非作者审查规则完全执行前已经合并，GitHub 未记录非作者 review：

```text
Governance exception: merged before review policy was fully enforced.
```

该记录只保存事实，不补造 review，也不构成后续 PR 的豁免。PR #16 至少需要
Simulink 同学和一位非作者审查后才可进入合并流程。
