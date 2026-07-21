# 模式管理规范

## 状态

规范状态：`DRAFT`。模式集合、优先级、默认降级和转换原则已定义；持续时间、
评分阈值和恢复阈值均为 `TBD — requires Plant and P1 evidence`。

## 模式优先级

从高到低：

1. `LOW_CONFIDENCE_DEGRADED`
2. `SAFE_SLOWDOWN`
3. `VIBRATION_SUPPRESSION`
4. `NORMAL_TRACKING`

高优先级条件与低优先级条件同时出现时，高优先级模式获胜。未知输入、未知模式或
规则冲突一律进入 `LOW_CONFIDENCE_DEGRADED`。

## 状态转换

| 当前模式 | 条件 | 下一模式 | 约束 |
|---|---|---|---|
| 任意模式 | `valid_flag=false` 或关键测量失效 | `LOW_CONFIDENCE_DEGRADED` | 立即进入，不等待分类 |
| 任意非低可信模式 | 外部接触证据有效且 P2 已通过 | `SAFE_SLOWDOWN` | 优先于抑振 |
| `NORMAL_TRACKING` | 柔性振动持续且估计可信 | `VIBRATION_SUPPRESSION` | P2 前不得由分类器自动触发 |
| `VIBRATION_SUPPRESSION` | 接触证据有效 | `SAFE_SLOWDOWN` | 高优先级抢占 |
| `SAFE_SLOWDOWN` | 接触解除、估计可信且满足保持窗口 | `NORMAL_TRACKING` | 禁止直接瞬时恢复 |
| `LOW_CONFIDENCE_DEGRADED` | 所有信号恢复并满足滞回与恢复窗口 | `NORMAL_TRACKING` | 重新进入前清除失效原因 |

## 防抖与恢复

- 每种非紧急转换均须满足持续窗口；
- 降级阈值和恢复阈值必须分离形成滞回；
- `SAFE_SLOWDOWN` 和 `LOW_CONFIDENCE_DEGRADED` 设最小保持时间；
- 低可信恢复只能回到 `NORMAL_TRACKING`，不得直接进入高性能模式；
- 具体阈值和时间参数在 P1/P2/P3 有效证据后冻结。

## 输出责任

Mode Manager 只输出 `operation_mode` 及转换原因，不直接计算底层控制力矩。控制
模块根据模式执行相应策略；模式管理不得绕过 Control 直接写入 Plant。
