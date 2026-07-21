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
- **Evidence**：旧实验存在力矩侧未明确、Plant/Observer 输入不一致、单负载、
  单场景、单 seed 和调参与评价未隔离问题；当前环境也无法执行 MATLAB 复验。
- **Owner**：项目负责人同学。
- **Affected files**：项目、架构、验证和当前状态文档。
- **Reversal condition**：模型和输入契约修复后，新的有效、充分且可复现实验形成
  `PASS` 或 `FAIL` 证据。

## DEC-002：规定负载侧弹性力矩候选语义

- **Date**：2026-07-21
- **Problem**：`tau_s` 所在侧和齿轮反射关系不明确。
- **Decision**：使用 `tau_s_load_nm` 表示负载侧弹性力矩；理想效率下反射到电机
  侧的力矩为 `tau_s_load_nm / N`。
- **Evidence**：统一动力学定义和无耗散能量一致性要求。
- **Owner**：项目负责人同学；Simulink 同学共同确认实现。
- **Affected files**：`docs/02_architecture/**`、后续 Plant/Observer 实现。
- **Reversal condition**：引入经过审查的效率、回差或其他传动模型，并完成新的
  能量推导和接口变更。

## DEC-003：拆分命令、Plant 追踪和 Observer 反馈契约

- **Date**：2026-07-21
- **Problem**：Plant 使用饱和后力矩而 Observer 使用原始指令，导致实验无效。
- **Decision**：v2 契约拆为 `ActuatorCommand`、`PlantInputTrace`、
  `RawMotorMeasurement`、`TorqueFeedback`、`SignalHealthStatus` 和 `ObserverInput`。
  Observer 只能读取 `motor_torque_feedback_nm`，不得读取命令或
  `motor_torque_applied_nm`。
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

## DEC-005：设计规范与算法实现分层

- **Date**：2026-07-21
- **Problem**：完整设计文档是否可以被解释为 Confidence、Calibration、Mode
  Manager 或验证系统已经实现。
- **Decision**：规范、实现和验证分别使用各自状态词；权重、阈值、窗口和保持时间
  在有效证据形成前保持 `TBD` 或明确标记为 `PROVISIONAL`。
- **Evidence**：当前仓库只有文档、Schema、Python 契约、Mock 和部分旧实现，尚无
  经过 P1/P2/P3 验证的端到端链路。
- **Owner**：项目负责人同学维护规范；对应模块同学负责实现和实验。
- **Affected files**：架构规范、跨语言矩阵、验收矩阵、当前状态和 PR 声明。
- **Reversal condition**：对应实现完成、测试实际运行并通过已批准阶段门后，单独更新
  实现状态和性能结论。

## DEC-006：拆分 P1 子门并闭合路线

- **Date**：2026-07-21
- **Problem**：状态基本可用性、Observer 相对 baseline 的优势和外扰可分辨性被混在
  一个 P1 结论中。
- **Decision**：P1 拆为 P1-V 与 P1-A；外扰力矩只作 P1 诊断，P2 拆为 P2-VIB 与
  P2-CONTACT，P3 拆为 DEGRADE、ACTION 与 RECOVERY。P1-V 通过而 P1-A 失败时进入
  `P1_REFRAME_REVIEW`，不能直接认定状态不可估计。
- **Evidence**：绝对可用性与相对优势回答不同问题，且振动/接触可分辨性属于 P2。
- **Owner**：项目负责人同学。
- **Affected files**：项目章程、阶段门、实验协议、报告 Schema 和 Issue。
- **Reversal condition**：只有新的有效证据或范围变更经审查后才能调整子门关系。

### P1_REFRAME_REVIEW 约束补充

该状态只能输出 `CONTINUE_TO_ROUTE_B`、`ONE_BOUNDED_REPAIR` 或 `ENTER_ROUTE_C`。
每个 P1 评价活动最多一次有限修复；门限只能在评价集解封前修改并记录 Decision ID。
修复后使用新的独立评价配置。若 P1-V 已通过后主动进入 C，记录为范围决定，不把
P1-V 改写为失败。

## DEC-007：隔离真值配置与名义参数

- **Date**：2026-07-21
- **Problem**：校准若可修改 Plant 真值配置，会污染实验对象和评价结论。
- **Decision**：`ImmutablePlantTrueConfig` 在单次实验中不可修改；校准只生成候选，
  验收决定只能原子更新或回滚 `VersionedNominalParameterStore`。在线决定不得读取真值。
- **Evidence**：被评价对象和算法名义参数必须独立、可追溯。
- **Owner**：项目负责人同学维护契约，相关模块同学审查实现。
- **Affected files**：架构、校准规范、公共 DTO、Schema 和实验协议。
- **Reversal condition**：无；配置字段可版本化扩展，但隔离原则不得取消。

## DEC-008：采用 v2 DTO 和阶段化证据报告

- **Date**：2026-07-21
- **Problem**：单体输入和全阶段指标报告造成越权读取及用 `0.0` 表示不适用指标。
- **Decision**：公共运行时契约升级至 `2.0.0`；系统输出拆分后由
  `SystemStateSnapshot` 只读聚合。验证报告采用公共 Envelope 加 stage 专用 Payload，
  不适用字段必须省略。
- **Evidence**：DTO 单一职责、运行时真值隔离和证据语义清晰性。
- **Owner**：项目负责人同学维护候选契约；各语言负责同学完成迁移。
- **Affected files**：接口文档、Schema、Python 类型、Mock 和契约测试。
- **Reversal condition**：后续破坏性变更必须提升主版本并提供迁移记录。

## DEC-009：记录 PR #14 治理例外

- **Date**：2026-07-21
- **Problem**：PR #14 在审查策略完全执行前合并，且没有非作者审查记录。
- **Decision**：`Governance exception: merged before review policy was fully enforced.`
  不补造 review；此后公共契约 PR 至少需要模块负责同学和一位非作者审查。
- **Evidence**：现有 PR 历史记录。
- **Owner**：项目负责人同学。
- **Affected files**：协作记录和 PR 声明。
- **Reversal condition**：历史事实不可反转，只能追加后续治理改进记录。

## DEC-010：PR #15 与 PR #16 的处理顺序

- **Date**：2026-07-21
- **Problem**：两个 Draft PR 同时修改状态入口和部分架构、验证文档，存在旧定义覆盖
  v2 规范的风险。
- **Decision**：PR #16 包含更新的 DTO、子门、路线、配置隔离和状态分类定义，应先
  完成审查；随后将 PR #15 rebase 或同步到更新后的 `main`，逐文件解决冲突。不得自动
  合并、关闭 PR #15 或回退当前状态。
- **Evidence**：本地 `origin/main...` 分支文件差异清单。
- **Owner**：项目负责人同学。
- **Affected files**：两个 PR 的重叠文档及 PR 正文。
- **Reversal condition**：若维护者决定先合并 PR #15，PR #16 必须先 rebase 并证明
  没有状态、接口或路线回退。
