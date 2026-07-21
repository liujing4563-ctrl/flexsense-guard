# 可信评分设计规范

## 1. 规范状态

设计状态：`SPECIFIED`，算法状态：未实现。输入、输出、失效原则、优先级和下游
关系已经规定；最终权重、阈值、时间窗口和性能结论尚未冻结。

## 2. 设计目标

可信评分回答“当前估计是否足以供下游使用”，在信号异常、Observer 失配或物理
不合理时主动降低可用性，并给出可追溯原因。

## 3. 非目标

- 不估计负载侧状态或外部关节扰动力矩；
- 不输出接触概率，也不替代 Classification；
- 不读取 Plant 真值、评价标签或最终评价集结论；
- 不直接产生控制力矩或在线修改参数；
- 当前规范不构成 P3 已通过的证据。

## 4. 输入

| 输入类别 | 候选信息 | 约束 |
|---|---|---|
| 残差一致性 | `innovation_norm`、残差有限性和持续性 | 阈值待 P1/P3 证据确定 |
| 信号健康 | 编码器、电流、测量力矩、时间戳、数据新鲜度 | 任一硬失效优先于连续评分 |
| 物理合理性 | 状态有限性、参数边界、能量与变化率检查 | 不使用负载侧真值在线判定 |
| 模型适用性 | 饱和、参数失配迹象、模型外工况 | 只输出适用性证据，不在线辨识真参数 |

## 5. 输出

- `confidence_score`：限制在 `[0,1]` 的工程评分，不是统计概率；
- `valid_flag`：当前估计是否允许下游正常使用；
- `reason_codes`：无效、低可信或模型不适用的原因数组。

## 6. 评分组成

候选设计框架为：

```text
confidence_score
= w_residual * residual_consistency
+ w_signal * signal_health
+ w_physics * physical_plausibility
+ w_model * model_compatibility
```

该公式只是设计框架。各分量定义、权重和归一化方法均未确定；权重不得使用最终
评价集选择，最终值必须基于有效 P1 和 P3 证据确定。硬失效条件可以直接令
`valid_flag=false`，不受加权平均结果覆盖。

## 7. 无效条件

以下情况至少令 `valid_flag=false`：时间戳无效或倒退、编码器无效、关键输入非
有限、Observer 发散、状态出现 NaN/Inf、未知枚举、评分越界或数据超过新鲜度
要求。电流无效、执行器持续饱和、参数失配迹象和物理边界异常进入低可信还是直接
无效，必须由后续故障矩阵验证。

## 8. 候选原因码

以下是设计候选项，不代表 Schema、Python 或 MATLAB 已完成迁移：

```text
ENCODER_INVALID
CURRENT_INVALID
TIMESTAMP_INVALID
ACTUATOR_SATURATED
INNOVATION_EXCESSIVE
PHYSICAL_LIMIT_VIOLATION
PARAMETER_MISMATCH_SUSPECTED
OBSERVER_DIVERGENCE
DATA_STALE
UNKNOWN_REASON
```

原因码必须是稳定字符串、允许多个同时出现，并保留首次触发和恢复时间。候选值
进入公共枚举前必须走独立契约变更 PR。

## 9. 低可信进入条件

- 硬失效立即进入低可信，不等待连续评分窗口；
- 残差、模型失配或持续饱和等软条件必须满足持续窗口；
- 多个软异常同时出现时按故障优先级合并原因；
- 进入阈值、持续窗口和组合规则均为 TBD。

## 10. 恢复条件

恢复前必须满足：硬失效已解除、数据重新连续有效、Observer 输出有限、残差回到
恢复区间、所有强制原因码已清除，并持续满足恢复窗口。恢复不能删除历史原因和
时间记录。

## 11. 滞回原则

低可信进入阈值与恢复阈值必须分离，进入窗口与恢复窗口可以不同。禁止在阈值附近
逐样本往返切换，也禁止用单个正常样本清除持续故障。

## 12. 最小保持时间原则

硬失效解除后仍应保持低可信至少一个冻结恢复窗口。具体保持时间不得凭经验写死，
必须由采样率、Observer 动态和 P3 故障实验共同确定。

## 13. 与 Classification 的关系

Classification 消费 `valid_flag`、`confidence_score` 和原因码。低可信或无效时应
输出 `LOW_CONFIDENCE`，不得把异常残差解释为外部接触，也不得把
`contact_score` 解释为概率。

## 14. 与 Mode Manager 的关系

`valid_flag=false` 或低可信条件满足时，Mode Manager 优先进入
`LOW_CONFIDENCE_DEGRADED`。Mode Manager 负责模式转换，Confidence 不直接写入
Plant 或底层控制器。

## 15. 与 Event-trigger Calibration 的关系

可信下降可以提出校准候选事件，但无效输入、Observer 发散、持续饱和或没有可信
参数备份时必须禁止校准。校准结果不能反向改写历史可信证据。

## 16. 故障优先级

架构优先级从高到低为：时间戳/编码器等关键输入失效、Observer 发散、非有限或
物理越界、数据陈旧、持续执行器饱和、创新异常、参数失配迹象。具体冲突映射仍需
P3 验证，未知故障按 `UNKNOWN_REASON` 和低可信处理。

## 17. 待实验确定参数

以下内容统一为 `TBD — requires validated Plant and P1 evidence`：评分分量算法、
权重、归一化范围、进入/恢复阈值、持续窗口、最小保持时间和原因码升级规则。
P3 还必须验证可信评分与真实估计误差的相关性，才能允许其驱动安全模式。
