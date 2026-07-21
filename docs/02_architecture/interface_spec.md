# 公共接口规范

本文件定义 v2 公共数据契约。当前规范、实现和验证状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。

## 版本和破坏性变更

v2 将原 `MotorSideMeasurement` 和扁平 `VirtualSensingEstimate/SystemState` 拆分为
专用 DTO。旧字段 `motor_torque_nm`、`motor_torque_measured_nm` 以及旧聚合结构不再
是当前权威接口，不保留静默兼容别名。

所有 v2 JSON DTO 使用 `schema_version="2.0.0"`。接口变更必须在独立 PR 中同步
本文档、JSON Schema、Python 类型、Mock、契约测试和受影响语言映射，并获得模块
负责同学确认。

## 公共枚举

### `ClassificationState`

```text
NORMAL
FLEXIBLE_VIBRATION
EXTERNAL_CONTACT
LOW_CONFIDENCE
```

### `OperationMode`

```text
NORMAL_TRACKING
VIBRATION_SUPPRESSION
SAFE_SLOWDOWN
LOW_CONFIDENCE_DEGRADED
```

### `TorqueSource`

```text
CURRENT_ESTIMATE
TORQUE_SENSOR
ACTUATOR_MODEL
UNKNOWN
```

### `SafetyActionLevel`

```text
NONE
LIMITED
SLOWDOWN
STOP_REQUEST
```

### `ReasonCode`

```text
NONE
ENCODER_INVALID
CURRENT_INVALID
TIMESTAMP_INVALID
TORQUE_INVALID
DATA_STALE
ACTUATOR_SATURATED
INNOVATION_EXCESSIVE
MODEL_MISMATCH_SUSPECTED
EXTERNAL_DYNAMIC_SUSPECTED
PHYSICAL_LIMIT_VIOLATION
OBSERVER_DIVERGENCE
LOW_CONFIDENCE
CONTACT_HAZARD_LATCHED
UNKNOWN_REASON
```

`NONE` 只能单独出现；存在任何异常原因时不得同时包含 `NONE`。未知输入枚举必须
映射为无效并保留 `UNKNOWN_REASON`，不能静默继续正常模式。

## 运行时输入契约

### `ActuatorCommand`

| 字段 | 类型 | 单位 | 生产者 | 消费者 | 无效处理 |
|---|---|---:|---|---|---|
| `schema_version` | string | - | Controller | Actuator | 非 `2.0.0` 拒绝 |
| `timestamp_s` | number | s | Controller | Actuator | 非有限、负值或乱序时拒绝 |
| `torque_command_nm` | number | N·m | Controller | Actuator | 非有限时进入保守动作 |

### `PlantInputTrace`

| 字段 | 类型 | 单位 | 生产者 | 消费者 | 无效处理 |
|---|---|---:|---|---|---|
| `schema_version` | string | - | Actuator | Plant、Validation | 版本错误时停止案例 |
| `timestamp_s` | number | s | Actuator | Plant、Validation | 非法时停止案例 |
| `motor_torque_applied_nm` | number | N·m | Actuator | Plant、Validation | 非有限时停止案例 |
| `saturation_active` | boolean | - | Actuator | Plant、Validation | 必须记录 |
| `actuator_limit_nm` | number | N·m | Actuator | Validation | 必须为正且有限 |

`PlantInputTrace` 属于仿真和离线追踪数据。Observer、Confidence、Classification、
Mode Manager、Calibration 和 Controller 禁止读取 `motor_torque_applied_nm`。

### `RawMotorMeasurement`

| 字段 | 类型 | 单位 | 生产者 | 消费者 | 无效处理 |
|---|---|---:|---|---|---|
| `schema_version` | string | - | Plant/硬件适配器 | Feedback、Health | 版本错误时拒绝 |
| `timestamp_s` | number | s | Plant/时钟 | Feedback、Health | 乱序或非有限时无效 |
| `motor_position_rad` | number | rad | 编码器 | Health、ObserverInput builder | 无效时不更新 Observer |
| `motor_velocity_rad_s` | number | rad/s | 速度估计 | Health、ObserverInput builder | 无效时不更新 Observer |
| `motor_current_a` | number | A | 电流接口 | Torque Feedback、Health | 无效时禁止电流换算 |
| `encoder_valid` | boolean | - | 原始采集层 | Health | `false` 为硬失效 |
| `current_valid` | boolean | - | 原始采集层 | Feedback、Health | `false` 时电流来源无效 |
| `timestamp_valid` | boolean | - | 原始采集层 | Health | `false` 为硬失效 |

### `TorqueFeedback`

| 字段 | 类型 | 单位 | 生产者 | 消费者 | 无效处理 |
|---|---|---:|---|---|---|
| `schema_version` | string | - | 转矩换算/传感器适配器 | Health、ObserverInput builder | 版本错误时拒绝 |
| `timestamp_s` | number | s | Feedback | Health、ObserverInput builder | 与原始测量不同步时无效 |
| `motor_torque_feedback_nm` | number | N·m | Feedback | Observer | 无效时不得用于预测输入 |
| `torque_source` | enum | - | Feedback | Observer、Validation | `UNKNOWN` 时默认低可信 |
| `torque_valid` | boolean | - | Feedback | Health、Observer | `false` 时禁止正常更新 |
| `torque_std_nm` | number | N·m | Feedback | Observer、Confidence | 非负；未知时不得填零冒充确定值 |

`motor_torque_feedback_nm` 可以来自电流换算、独立传感器或受控执行器模型估计，
不保证来自独立力矩传感器，也不等同于实际施加力矩。

来源语义固定如下，但具体估计器实现不在本规范中固定：

- `CURRENT_ESTIMATE`：由电流和版本化转矩常数换算到电机轴侧；必须记录常数版本、
  有效性和所在侧，不能把负载侧力矩直接当成电机轴侧力矩；
- `TORQUE_SENSOR`：独立转矩传感器经单位和所在侧换算后的电机轴侧反馈；
- `ACTUATOR_MODEL`：运行时执行器模型的估计输出，不等于、不得复制仿真真值
  `motor_torque_applied_nm`；
- `UNKNOWN`：来源不可确认，默认不得用于正常 Observer 更新。

`torque_std_nm` 表示同一电机轴侧反馈的不确定度标准差，不是噪声为零的占位值。
`torque_valid=false` 时 Observer 禁止执行正常测量更新；采用预测保持、降级或拒绝
样本由 Observer 规范在 P1 前批准，本接口不预先固定算法策略。App 对
`CURRENT_ESTIMATE` 或 `ACTUATOR_MODEL` 应显示“电机转矩反馈估计”，只有
`TORQUE_SENSOR` 才能显示为传感器测量。

### `SignalHealthStatus`

包含 `timestamp_s`、`encoder_valid`、`current_valid`、`timestamp_valid`、
`torque_valid`、`data_stale`、`saturation_active` 和 `reason_codes`。Signal Health 是
这些状态的唯一生产者；原始测量对象不承载派生健康结论。

### `ObserverInput`

只允许包含：

```text
schema_version
timestamp_s
motor_position_rad
motor_velocity_rad_s
motor_torque_feedback_nm
encoder_valid
current_valid
timestamp_valid
torque_valid
torque_std_nm
```

明确禁止：

```text
torque_command_nm
motor_torque_applied_nm
true_load_position_rad
true_load_velocity_rad_s
true_external_torque_nm
Plant 真实参数
```

## 模块输出契约

### `ObserverEstimate`

包含负载位置、负载速度、扭转量和外部关节力矩估计。残差必须使用
`normalized_innovation_squared`，或在后续版本中引入明确的逐通道归一化结构；不得
把 rad 与 rad/s 原始残差直接求 L2 范数后声明为无量纲量。

### `ConfidenceOutput`

包含 `confidence_score`、`valid_flag`、`confidence_state` 和 `reason_codes`。
`valid_flag` 是硬门控结果，`confidence_score` 是软评分，两者不可互相替代。

### `ClassificationOutput`

包含 `classification_state`、`contact_score` 和 `valid_flag`。`contact_score` 是工程
证据评分，不是概率；P2-CONTACT 通过前不得驱动接触安全动作。

### `ModeDecision`

包含：

```text
operation_mode
contact_hazard_latched
safety_action_required
safety_action_level
reason_codes
```

`operation_mode` 表示运行策略，危险锁存表示危险记忆，安全动作级别表示 Controller
必须执行的最小保守包络。`ModeDecision` 由 Safety Supervisor 统一产生：Mode Manager
只提供运行模式候选，Classification/Contact Logic 只提供危险证据，二者均无权设置
或清除锁存。低可信模式不得清除危险锁存或减弱安全动作。

### `SystemStateSnapshot`

只读聚合：`ObserverEstimate`、`ConfidenceOutput`、`ClassificationOutput` 和
`ModeDecision` 的同时间戳快照。它用于 App、报告和离线 Validation，不由单个算法
模块写入，也不得反向输入 Observer、Confidence 或 Classification。

### `ControlCommand`

| 字段 | 类型 | 单位 | 生产者 | 消费者 | 无效处理 |
|---|---|---:|---|---|---|
| `schema_version` | string | - | Controller | Actuator、Validation | 版本不匹配时拒绝 |
| `timestamp_s` | number | s | Controller | Actuator、Validation | 非法或乱序时拒绝 |
| `requested_torque_nm` | number | N·m | Controller | Validation | 非有限时请求失效 |
| `limited_torque_nm` | number | N·m | Controller | Actuator、Validation | 非有限时进入保守动作 |
| `safety_action_level` | enum | - | Controller | Actuator、Validation | 未知值按最保守边界处理并拒绝正常执行 |
| `operation_mode` | enum | - | Controller | App、Validation | 未知值进入低可信处理 |
| `valid_until_s` | number | s | Controller | Actuator | 早于当前时间即过期拒绝 |
| `reason_codes` | array | - | Controller | App、Validation | 缺失或冲突时对象无效 |

控制限制必须满足 `ModeDecision.safety_action_level`，具体转矩、速度和停止门限尚未
确定，需要 P3 和控制实验批准。

## 配置与校准契约

### `ImmutablePlantTrueConfig`

单次实验开始后不可修改，只供 Scenario、Plant 和 Offline Validation 使用。当前
场景 Schema 是该配置的入口之一；真实参数不得复制到运行时 DTO。

### `NominalParameterVersion`

由 `VersionedNominalParameterStore` 产生，Observer、Confidence、Calibration 和
Controller 只读消费。它记录 `parameter_version`、`base_parameter_version`、
`parameter_values`、`created_reason` 和 `checksum_sha256`。版本、校验或数值无效时
拒绝加载并保持上一有效版本；不得回退到默认零值。

### `CalibrationCandidate`

由 Calibration 产生、Acceptance 消费，包含 `candidate_id`、
`base_parameter_version`、`candidate_parameter_version`、`parameter_values`、
`generation_reason` 和 `acceptance_window_id`。候选版本与 base 相同、base 不是当前
批准版本、字段非有限、越界或包含真值来源时拒绝，不进入更新流程。

### `CalibrationDecision`

由 Acceptance 产生，名义参数库和证据记录消费。它包含 `candidate_id`、`decision`、
`decision_reason_codes` 和 `rollback_target_version`。`decision` 只能是 `UPDATE`、
`HOLD` 或 `ROLLBACK`。未知决定、缺少原因或候选不匹配时按 `HOLD` 拒绝执行；
`ROLLBACK` 必须指向已存在的上一有效版本，不能把参数或状态清零。

### `ArtifactIndexEntry`

由阶段 runner 或报告工具产生，Validation、审查者和报告系统消费。字段包括
`artifact_id`、`artifact_type`、`uri`、`checksum_sha256`、`size_bytes`、`owner` 和
`available`。URI 不可访问、SHA-256 不匹配、大小不一致或保管人缺失时，artifact
无效；必需 artifact 无效时阶段报告不得 `PASS`。索引只描述证据，不填虚构性能值。

## 仿真真值边界

以下字段只允许出现在 Plant 内部或离线评价数据中：

```text
true_load_position_rad
true_load_velocity_rad_s
true_external_torque_nm
motor_torque_applied_nm
```

契约测试必须证明 `ObserverInput`、`ObserverEstimate`、`ConfidenceOutput`、
`ClassificationOutput`、`ModeDecision` 和 `ControlCommand` 不含这些字段。

## 验证报告

验证报告采用公共 evidence envelope 加阶段 payload。P1、P2、P3、SIL 和 Integration
只要求各自适用指标；不适用指标必须省略，不得使用 `0.0` 表示 N/A。完整定义见
[`evidence_management.md`](../03_validation/evidence_management.md) 和
`common/schemas/validation_report.schema.json`。

公共 envelope 只强制跨阶段可追溯字段。`algorithm_version`、`random_seed`、
`software_environment` 和 `runtime_ms` 按实验适用性填写；多模块 Integration 使用
`result.component_versions` 记录组件版本，不用空字符串或零值补齐不适用字段。

## 失效和兼容规则

- 数值必须有限；时间戳非负且运行时单调不减；
- 评分限制在 `[0,1]`，标准差和误差指标非负；
- 未知枚举、版本不匹配或必需字段缺失时拒绝对象；
- `valid_flag=false` 的估计不得用于正常控制；
- v1 到 v2 是破坏性迁移，旧数据只能在明确的离线转换边界处理；
- 禁止在当前 DTO 中保留含糊旧字段作为兼容别名。
