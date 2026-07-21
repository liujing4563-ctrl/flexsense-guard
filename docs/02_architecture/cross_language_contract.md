# 跨语言契约矩阵

当前状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。本矩阵记录
v2 候选契约在各语言中的实际落地，不把规范审查解释为实现完成。

## 状态规则

本表的 Specification 使用 `DRAFT/REVIEWED/APPROVED/FROZEN`；实现使用
`MISSING/PLACEHOLDER/PARTIAL/IMPLEMENTED/INVALID`。验证结果另行记录，不在本表
混用。

## DTO 矩阵

| DTO | Specification | Python | Schema | MATLAB | C | App |
|---|---|---|---|---|---|---|
| `ActuatorCommand` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `PlantInputTrace` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `RawMotorMeasurement` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `TorqueFeedback` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `SignalHealthStatus` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `ObserverInput` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `ObserverEstimate` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `ConfidenceOutput` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `ClassificationOutput` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `ModeDecision` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `SystemStateSnapshot` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| `ControlCommand` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| `ImmutablePlantTrueConfig` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `INVALID` | `MISSING` | `MISSING` |
| `NominalParameterVersion` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| `CalibrationCandidate` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| `CalibrationDecision` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| `ArtifactIndexEntry` | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |
| Stage Validation Report | `REVIEWED` | `IMPLEMENTED` | `IMPLEMENTED` | `MISSING` | `MISSING` | `MISSING` |

MATLAB 标记为 `INVALID` 表示仓库已有旧实现，但字段、方程或输入边界不符合 v2；
`MISSING` 表示尚不存在相应映射。Python/Schema 的 `IMPLEMENTED` 只表示契约结构和
测试存在，不代表主体算法实现。

## 关键字段边界

| 字段 | 所属 DTO | Observer 可见 | 说明 |
|---|---|---|---|
| `torque_command_nm` | `ActuatorCommand` | 否 | 控制意图 |
| `motor_torque_applied_nm` | `PlantInputTrace` | 否 | 仿真 Plant 实际输入追踪值 |
| `motor_torque_feedback_nm` | `TorqueFeedback`、`ObserverInput` | 是 | 带来源、有效性和标准差的反馈 |
| `normalized_innovation_squared` | `ObserverEstimate` | 输出 | 不混合原始 rad/rad/s L2 范数 |
| `contact_hazard_latched` | `ModeDecision` | N/A | Safety Supervisor 独占写入和清除的危险记忆 |
| `safety_action_level` | `ModeDecision`、`ControlCommand` | N/A | 最小安全动作包络 |

## 破坏性迁移

v1 的 `MotorSideMeasurement`、`motor_torque_measured_nm` 和扁平 `SystemState` 被 v2
专用 DTO 替代。旧数据只能由明确的离线迁移器转换，不在当前类型中保留兼容别名。

| v1 结构或字段 | v2 结构或字段 | 迁移处理 |
|---|---|---|
| `MotorSideMeasurement` | `RawMotorMeasurement`、`TorqueFeedback`、`SignalHealthStatus`、`ObserverInput` | 按生产者和消费者拆分，不复制整个旧对象 |
| `torque_command_nm` | `ActuatorCommand.torque_command_nm` | 只进入 Actuator，不进入 Observer |
| `motor_torque_applied_nm` | `PlantInputTrace.motor_torque_applied_nm` | 只供 Plant 和离线 Validation，禁止进入 Observer |
| `motor_torque_measured_nm` | `TorqueFeedback.motor_torque_feedback_nm` | 重命名并新增来源、有效性和标准差；不保证来自转矩传感器 |
| 旧扁平 `SystemState` | `SystemStateSnapshot` | 改为多模块输出的只读时间对齐快照 |
| `innovation_norm` | `ObserverEstimate.normalized_innovation_squared` | 原始混合单位 L2 值不可直接迁移，必须重新计算 |

迁移检查：所有当前 v2 DTO 使用 `schema_version="2.0.0"`；Mock 只引用 v2 Schema；
契约测试必须拒绝旧字段；当前状态入口只保留
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md)。离线迁移器尚未
实现，需要迁移历史数据时由数据所有者单独提交，不在运行时保留双版本权威字段。

## 权威来源

| 内容 | 权威来源 |
|---|---|
| 当前阶段状态 | [`current_status_and_next_steps.md`](../current_status_and_next_steps.md) |
| 字段、单位和失效规则 | [`interface_spec.md`](interface_spec.md) |
| 数学符号 | [`glossary_and_symbols.md`](glossary_and_symbols.md) |
| JSON 结构 | `common/schemas/*.schema.json` |
| Python 类型 | `python/flexsense_guard/types.py` |
| MATLAB 映射 | Simulink 同学负责的 Plant、Observer 和 runner |
| C/C++ 类型 | 嵌入式 Linux 同学在 `08_sil/include/**` 实现 |
| App 映射 | 软件同学在 `07_app/**` 实现 |

## 迁移规则

1. 模块负责同学只能在自己的主责路径实现语言映射；
2. 不保留含糊旧字段或自动回退别名；
3. 公共字段变更同步文档、Schema、Python、Mock 和测试；
4. MATLAB、C 和 App 未共同回放前，跨语言实现保持 `PARTIAL`；
5. 端到端状态只能由真实生产者、消费者和证据决定。
