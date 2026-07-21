# 模式管理规范

## 1. 规范状态

设计状态：`SPECIFIED`，算法状态：未实现。模式、分类、优先级、冲突处理和恢复
原则已经规定；阈值、持续窗口和最小保持时间仍需 P2/P3 验证。

## 2. 模式与分类集合

运行模式只能使用：

```text
NORMAL_TRACKING
VIBRATION_SUPPRESSION
SAFE_SLOWDOWN
LOW_CONFIDENCE_DEGRADED
```

分类状态只能使用：

```text
NORMAL
FLEXIBLE_VIBRATION
EXTERNAL_CONTACT
LOW_CONFIDENCE
```

未知分类或未知模式按无效输入处理，不能静默保持高性能模式。

## 3. 架构优先级

```text
LOW_CONFIDENCE_DEGRADED
> SAFE_SLOWDOWN
> VIBRATION_SUPPRESSION
> NORMAL_TRACKING
```

这是安全冲突时的架构优先级，不是性能结论。高优先级条件与低优先级条件同时成立
时，高优先级模式获胜；具体阈值和保持时间尚未冻结，需要 P2/P3 验证。

## 4. 状态转移表

| 当前模式 | 条件 | 下一模式 | 约束 |
|---|---|---|---|
| 任意模式 | `valid_flag=false`、关键输入无效或未知枚举 | `LOW_CONFIDENCE_DEGRADED` | 立即抢占，不等待分类 |
| 任意非低可信模式 | 有效 `EXTERNAL_CONTACT` 且 P2 已通过 | `SAFE_SLOWDOWN` | 优先于抑振和正常跟踪 |
| `NORMAL_TRACKING` | 有效 `FLEXIBLE_VIBRATION` 持续成立 | `VIBRATION_SUPPRESSION` | P2 前不得由分类器自动触发 |
| `VIBRATION_SUPPRESSION` | 有效外部接触条件成立 | `SAFE_SLOWDOWN` | 高优先级抢占 |
| `VIBRATION_SUPPRESSION` | 振动条件解除且恢复窗口满足 | `NORMAL_TRACKING` | 需要滞回和最小保持时间 |
| `SAFE_SLOWDOWN` | 接触解除、输入有效且恢复窗口满足 | `NORMAL_TRACKING` | 禁止瞬时恢复 |
| `LOW_CONFIDENCE_DEGRADED` | 全部硬失效解除并满足恢复门禁 | `NORMAL_TRACKING` | 只回到安全基线模式 |

## 5. 冲突处理

先处理输入有效性，再处理接触证据、振动证据和正常状态。同级规则冲突、原因码
无法解释或分类与可信状态矛盾时，进入 `LOW_CONFIDENCE_DEGRADED` 并保留冲突
原因，不选择更激进模式。

## 6. 输入无效处理

时间戳、编码器、关键力矩输入、枚举或数值非有限时立即输出
`LOW_CONFIDENCE_DEGRADED`。无效输入不得用于更新模式恢复计时器、Calibration
候选或正常控制参数。

## 7. 滞回原则

进入阈值和恢复阈值必须分离，进入窗口与恢复窗口允许不同。模式转换基于持续事件，
不能依据单个边界样本往返切换。紧急降级不等待滞回，恢复必须等待滞回。

## 8. 最小保持时间原则

`SAFE_SLOWDOWN` 和 `LOW_CONFIDENCE_DEGRADED` 必须设置最小保持时间；
`VIBRATION_SUPPRESSION` 也应防止频繁切换。具体时间为
`TBD — requires validated Plant and P1 evidence`，并需 P2/P3 验证。

## 9. 恢复条件

恢复要求触发原因解除、关键输入连续有效、Confidence 满足恢复门禁、分类状态稳定、
最小保持时间结束且没有更高优先级事件。恢复只进入 `NORMAL_TRACKING`，再由正常
转移规则决定是否进入其他模式。

## 10. 安全默认模式

启动时契约未验证、状态未知、规则冲突或恢复条件不完整时，安全默认模式为
`LOW_CONFIDENCE_DEGRADED`。这不等于底层控制动作已实现。

## 11. 与 Confidence 的关系

Mode Manager 消费 `valid_flag`、`confidence_score` 和 `reason_codes`。硬失效优先于
连续评分；Confidence 不直接写模式，Mode Manager 也不重新计算可信评分。

## 12. 与 Classification 的关系

Mode Manager 消费 `classification_state` 和 `contact_score`，但只有在对应阶段门
通过且 Confidence 有效时才允许分类驱动模式。P2 前不得宣称可靠接触模式切换。

## 13. 与 Calibration 的关系

进入 `SAFE_SLOWDOWN` 或 `LOW_CONFIDENCE_DEGRADED` 时必须中止校准。Calibration
只能提交候选事件与决定，不能绕过 Mode Manager 修改模式。

## 14. 尚未冻结阈值

所有评分阈值、接触/振动持续时间、最小保持时间、恢复窗口和抢占后的冷却时间均为
`TBD — requires validated Plant and P1 evidence`。模式规范不代表模式算法、控制律
或 P2/P3 已经实现。
