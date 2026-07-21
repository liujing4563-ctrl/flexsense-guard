# 公共接口规范

## 适用范围

本规范是 MATLAB、Python、C/C++、App 和测试工具之间的公共契约。字段名、单位、
枚举和无效数据处理一旦变更，必须同步修改文档、JSON Schema、Python 类型、
MATLAB 结构体定义和 C 头文件，并由受影响的模块负责同学审查。

## 分类状态

公共分类状态只能使用：

| 枚举值 | 含义 | 允许使用条件 |
|---|---|---|
| `NORMAL` | 正常运动 | 估计有效且没有持续振动或接触证据 |
| `FLEXIBLE_VIBRATION` | 柔性振动 | P2 证据支持后使用 |
| `EXTERNAL_CONTACT` | 外部接触 | P2 证据支持后使用 |
| `LOW_CONFIDENCE` | 估计低可信 | 信号、模型或物理检查不满足要求 |

## 运行模式

公共运行模式只能使用：

| 枚举值 | 含义 | 默认控制原则 |
|---|---|---|
| `NORMAL_TRACKING` | 正常跟踪 | 使用名义跟踪策略 |
| `VIBRATION_SUPPRESSION` | 振动抑制 | 降低振动并限制激励 |
| `SAFE_SLOWDOWN` | 安全减速 | 限速、减速并保留可追溯原因 |
| `LOW_CONFIDENCE_DEGRADED` | 低可信降级 | 使用保守参数和最小能力集 |

## 电机侧输入 `MotorSideMeasurement`

| 字段 | 类型 | 单位 | 合法范围 | 生产模块 | 消费模块 | 无效数据处理 |
|---|---|---:|---|---|---|---|
| `timestamp_s` | number | s | 有限且不小于 0，运行中单调不减 | Plant / 数据回放 | 全部运行时模块 | 标记时间戳无效，不更新 Observer |
| `motor_position_rad` | number | rad | 有限值 | Plant / 编码器接口 | Signal Health、Observer | 标记编码器无效，保持或降级 |
| `motor_velocity_rad_s` | number | rad/s | 有限值 | Plant / 速度估计 | Signal Health、Observer | 标记编码器无效，保持或降级 |
| `motor_current_a` | number | A | 有限值 | Plant / 电流接口 | Signal Health、力矩换算 | 标记电流无效，不使用该值校准 |
| `torque_command_nm` | number | Nm | 有限值 | Control / 场景发生器 | 执行器模型、Validation | 标记指令无效并进入保守模式；禁止直接输入 Observer |
| `motor_torque_applied_nm` | number | Nm | 有限值 | 执行器模型 | Plant、转矩测量模型、Validation | 必须反映饱和和执行器约束；无效时停止案例 |
| `motor_torque_measured_nm` | number | Nm | 有限值 | 转矩测量模型 / 电流换算 | Signal Health、Observer、Validation | 无效时不执行 Observer 更新 |
| `encoder_valid` | boolean | - | `true` 或 `false` | Signal Health | Observer、Confidence | `false` 时禁止正常更新 |
| `current_valid` | boolean | - | `true` 或 `false` | Signal Health | Observer、Confidence | `false` 时降低可信评分 |
| `timestamp_valid` | boolean | - | `true` 或 `false` | Signal Health | 全部运行时模块 | `false` 时拒绝乱序样本 |
| `saturation_flag` | boolean | - | `true` 或 `false` | Plant / 执行器接口 | Confidence、Control、Validation | `true` 时记录原因并限制控制 |

### 力矩字段不变量

```text
torque_command_nm
-> saturation / actuator model
-> motor_torque_applied_nm
-> Plant

motor_torque_applied_nm
-> torque measurement model
-> motor_torque_measured_nm
-> Observer
```

- `torque_command_nm` 是控制意图，不代表 Plant 实际收到的力矩。
- `motor_torque_applied_nm` 是饱和和执行器模型之后实际施加到 Plant 的电机侧力矩。
- `motor_torque_measured_nm` 是 Observer 可消费的电机侧测量力矩。
- 没有独立测量模型时，可以暂定
  `motor_torque_measured_nm = motor_torque_applied_nm + measurement_noise_nm`。
- Observer 禁止直接消费 `torque_command_nm`。
- 旧字段 `motor_torque_nm` 自本版本起为禁止字段。JSON Schema 和 Python 类型已
  完成迁移；MATLAB 历史结构由 Simulink 同学在 P1 输入一致性任务中迁移。

## 虚拟感知输出 `VirtualSensingEstimate`

| 字段 | 类型 | 单位 | 合法范围 | 生产模块 | 消费模块 | 无效数据处理 |
|---|---|---:|---|---|---|---|
| `timestamp_s` | number | s | 有限且不小于 0 | Observer | 下游全部模块 | 与输入时间戳不一致时判无效 |
| `estimated_load_position_rad` | number | rad | 有限值 | Observer | Classification、Control、Validation | `valid_flag=false` 时不得用于正常控制 |
| `estimated_load_velocity_rad_s` | number | rad/s | 有限值 | Observer | Classification、Control、Validation | `valid_flag=false` 时不得用于正常控制 |
| `estimated_torsion_rad` | number | rad | 有限值 | Observer | Confidence、Classification、Validation | 超物理范围时进入低可信 |
| `estimated_external_torque_nm` | number | Nm | 有限值 | Observer | Confidence、Classification、Validation | 无效时不得解释为接触 |
| `innovation_norm` | number | - | 有限且不小于 0 | Observer | Confidence、Validation | 非有限值时立即判无效 |
| `confidence_score` | number | - | `[0,1]` | Confidence | Classification、Mode Manager、Validation | 超范围时判无效并降级 |
| `contact_score` | number | - | `[0,1]` | Classification | Mode Manager、Validation | P2 前只作诊断，不驱动接触模式 |
| `classification_state` | string | - | 四种分类状态之一 | Classification / Confidence | Mode Manager、Validation、App | 未知值按 `LOW_CONFIDENCE` 处理 |
| `operation_mode` | string | - | 四种运行模式之一 | Mode Manager | Control、Validation、App | 未知值按 `LOW_CONFIDENCE_DEGRADED` 处理 |
| `valid_flag` | boolean | - | `true` 或 `false` | Observer / Confidence | 下游全部模块 | `false` 时禁止正常控制 |
| `reason_codes` | array[string] | - | 已登记原因码的数组 | Signal Health / Confidence | Validation、App | 未知原因码保留原文并进入低可信 |

## 原因码

当前基础原因码为：

```text
NONE
INVALID_TIMESTAMP
INVALID_ENCODER
INVALID_CURRENT
TORQUE_SATURATED
LOW_CONFIDENCE
```

新增原因码必须保持可追溯、单一含义，并同步公共契约。

## 仿真真值

以下字段只允许出现在仿真结果和评价接口中：

```text
true_load_position
true_load_velocity
true_external_torque
```

Observer、Confidence、Classification、Mode Manager 和 Control 的输入结构中禁止
出现这些字段。测试必须检查该不变量。

## 参数边界

- Plant 使用真实仿真参数；Observer 使用独立的名义参数。
- 两组参数不得引用同一可变对象。
- Observer 名义参数必须记录与 Plant 参数的失配。
- 参数值必须检查有限性、惯量和传动比为正、阻尼和摩擦非负。
- 传动比方向统一为理想刚性关系 `theta_l = theta_m / N`。
- `tau_s_load_nm` 统一表示负载侧弹性力矩；电机侧反射力矩在理想效率下为
  `tau_s_load_nm / N`。

## 术语约束

- `confidence_score` 是工程可信评分，不是统计概率。
- `contact_score` 是接触证据评分，不是概率。
- 禁止字段 `contact_probability`。
- 核心外扰输出统一使用 `estimated_external_torque_nm`。
- 当前输出是外部关节扰动力矩。未给出 Jacobian、等效力臂和坐标变换时，不得
  称为末端力。

## 版本与兼容

公共接口变更必须：

1. 在独立 PR 中说明兼容性影响；
2. 同步文档、Schema 和语言类型；
3. 增加或修改一致性测试；
4. 获得受影响模块负责同学确认；
5. 不在同一 PR 中顺带修改主体算法。

当前字段语义、JSON Schema 和 Python 参考类型已经同步。MATLAB 输入结构、C/C++
头文件和 App 映射尚未迁移，端到端契约状态为 `NOT_VERIFIED`。各语言状态见
[`cross_language_contract.md`](cross_language_contract.md)。
