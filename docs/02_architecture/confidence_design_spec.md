# 可信评分设计规范

规范状态和实现状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。目标规范尚未
实现；仓库旧 `confidence_score.m` 和 `signal_health_check.m` 属于
`OUTDATED / NON-COMPLIANT IMPLEMENTATION`，本规范不修改其源码。

## 目标与非目标

Confidence 回答“当前估计是否允许下游正常使用”，输出工程评分、硬有效标志和可
追溯原因。它不估计负载状态、不输出概率、不分类接触、不修改参数、不产生控制力矩，
也不读取 Plant 真值或最终评价标签。

## 输入依赖

Confidence 只读取：

- `ObserverEstimate`；
- `SignalHealthStatus`；
- 已批准的物理边界和数据新鲜度规则；
- 可观测的执行器饱和和模型适用性证据。

Confidence 禁止读取 `ClassificationOutput`，避免形成
Confidence -> Classification -> Confidence 循环。Classifier 可以读取
`ConfidenceOutput`。

## 输出语义

| 输出 | 含义 |
|---|---|
| `valid_flag` | 硬门控结果，决定当前估计能否用于正常下游逻辑 |
| `confidence_score` | `[0,1]` 的软工程评分，不是统计概率 |
| `confidence_state` | `VALID`、`SOFT_DEGRADED` 或 `HARD_INVALID` |
| `reason_codes` | 当前硬失效、软退化和模型外动态原因 |

`valid_flag=false` 时评分不能把估计重新变为有效。评分较低也不自动等于硬失效。

## 残差规范

禁止把位置残差 rad 与速度残差 rad/s 直接组成原始 L2 范数并声明无量纲。允许的
候选方法为：

1. Normalized Innovation Squared（NIS）；
2. 白化残差；
3. 使用预注册尺度逐通道归一化后再组合。

具体方法由 Observer 接口和有效 P1 证据确认。在此之前，权重、阈值、窗口、恢复
时间和残差组合方式均不作数值承诺。

## 硬失效

以下条件至少使 `valid_flag=false` 且状态为 `HARD_INVALID`：

- `ENCODER_INVALID`；
- `TIMESTAMP_INVALID`；
- `DATA_STALE`；
- `OBSERVER_DIVERGENCE`；
- 关键输入或状态出现 NaN/Inf；
- 未知契约版本或未知关键枚举。

硬失效立即生效，不等待软评分窗口。

## 软退化

以下证据默认降低 `confidence_score`，但不自动使估计无效：

- 短时执行器饱和；
- 归一化创新持续偏大；
- 参数失配迹象；
- 物理边界接近；
- 模型外动态迹象。

软退化达到硬失效的升级条件必须由 P3 故障矩阵单独批准，不能凭经验写死。

## 残差原因区分

大残差至少区分：

```text
SIGNAL_FAILURE
MODEL_MISMATCH_SUSPECTED
EXTERNAL_DYNAMIC_SUSPECTED
```

真实接触可能导致残差增大，因此 `INNOVATION_EXCESSIVE` 不能自动解释为 Observer
无效，也不能自动压制接触候选。只有信号失效、发散或明确物理不可能条件才能直接
触发硬无效；外部动态嫌疑交给 Classification 结合其他证据判断。

## 评分框架

候选框架可以组合残差一致性、信号健康、物理合理性和模型适用性，但所有分量必须
先归一化。最终权重不得使用最终评价集选择，也不得把加权分数解释为概率。

## 恢复与滞回

恢复要求硬原因解除、数据连续有效、Observer 输出有限、归一化残差回到恢复区间，
并持续满足恢复窗口。进入阈值与恢复阈值必须分离；单个正常样本不能清除持续故障。
具体阈值、窗口和最小保持时间需要 P3-DEGRADE/P3-RECOVERY 证据。

## 与其他模块关系

- Classification 可以读取 Confidence；低可信时必须保留原因，不把评分称为概率；
- Mode Manager 使用硬有效性和软评分，但负责最终模式和安全动作；
- Confidence 下降只能提出校准候选，不能批准校准；
- 接触危险锁存、低可信降级或硬失效时禁止校准；
- P3 通过前，Confidence 只能用于诊断和展示，不能驱动安全模式。
