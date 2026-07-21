# 模式管理与危险锁存规范

规范状态和实现状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。目标规范尚未
实现；现有 `mode_manager.m` 是 `OUTDATED / NON-COMPLIANT IMPLEMENTATION`，本规范
不修改其源码。

## 三个正交输出

Mode Manager 必须分开输出：

1. `operation_mode`：当前运行策略；
2. `contact_hazard_latched`：已确认接触危险的记忆；
3. `safety_action_level`：Controller 必须满足的最小安全动作包络。

`safety_action_required` 表示当前动作级别是否高于 `NONE`。

## 运行模式

```text
NORMAL_TRACKING
VIBRATION_SUPPRESSION
SAFE_SLOWDOWN
LOW_CONFIDENCE_DEGRADED
```

运行模式不等同于底层控制律，也不单独决定是否清除危险。

## 安全动作级别

```text
NONE
LIMITED
SLOWDOWN
STOP_REQUEST
```

级别从上到下逐渐保守。具体转矩、速度、停止和保持门限尚未确定，必须由 P3-ACTION
和控制实验批准。本规范不是工业安全认证逻辑。

## 危险锁存

- 有效 P2-CONTACT 证据触发后，设置 `contact_hazard_latched=true`；
- 低可信、模式切换或单个无接触样本不得清除锁存；
- 清除必须满足接触解除证据、信号连续有效、最小保持时间和恢复窗口；
- P2-CONTACT 通过前，Mock 中的危险锁存只用于契约联调，不能驱动真实安全声明。

## 冲突处理

`LOW_CONFIDENCE_DEGRADED > SAFE_SLOWDOWN` 不再作为唯一安全优先级。模式策略可以
进入低可信降级，但最终控制动作必须取当前模式要求和危险锁存要求中更保守者：

```text
effective_safety_action
= max(mode_required_action, latched_hazard_required_action)
```

如果 `contact_hazard_latched=true`，安全动作至少为 `SLOWDOWN`，必要时为
`STOP_REQUEST`。低可信模式不得清除危险，也不得把动作降到 `NONE` 或 `LIMITED`。

## 状态转移原则

| 条件 | operation_mode | 危险与动作约束 |
|---|---|---|
| 关键输入无效、未知枚举、Observer 发散 | `LOW_CONFIDENCE_DEGRADED` | 保留已有危险锁存；动作取更保守值 |
| 有效接触且 P2-CONTACT 已通过 | `SAFE_SLOWDOWN` 或更保守策略 | 锁存危险，至少 `SLOWDOWN` |
| 有效柔性振动且 P2-VIB 已通过 | `VIBRATION_SUPPRESSION` | 不自动设置接触危险 |
| 条件正常且无锁存危险 | `NORMAL_TRACKING` | 可以为 `NONE` |

同级规则冲突、来源不可解释或数据不同步时进入低可信降级，并保留所有危险原因。

## 滞回、保持和恢复

- 紧急降级和危险锁存不等待滞回；
- 恢复阈值与进入阈值分离；
- `SAFE_SLOWDOWN`、`LOW_CONFIDENCE_DEGRADED` 和危险锁存均有最小保持时间；
- 恢复只先进入 `NORMAL_TRACKING`，再由正常规则重新评价其他模式；
- 具体窗口和保持时间需要 P3-ACTION/P3-RECOVERY 证据。

## 与其他模块关系

- Confidence 不直接写模式；
- Classification 提供分类和接触证据，但只有通过对应 P2 子门后才能驱动模式；
- Calibration 在危险锁存、`SAFE_SLOWDOWN` 或 `LOW_CONFIDENCE_DEGRADED` 时必须中止；
- Controller 必须执行不弱于 `safety_action_level` 的控制限制；
- P3-ACTION 通过前，ModeDecision 只能用于契约联调和诊断。
