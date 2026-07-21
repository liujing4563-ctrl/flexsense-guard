# 可信评分设计规范

## 状态

规范状态：`DRAFT`。输入、输出、边界和失效原则已定义；权重、阈值、恢复时间和
性能结论均为 `TBD — requires Plant and P1 evidence`。

## 目标与边界

可信评分回答“当前估计是否足以供下游使用”，不回答“发生接触的概率是多少”。
本模块不读取 Plant 真值，不替代 Observer、分类器或模式管理器。

候选合成结构为：

```text
confidence_score
= w_r * residual_consistency_score
+ w_s * signal_health_score
+ w_p * physical_plausibility_score
+ w_m * model_applicability_score
```

所有分量和最终输出均限制在 `[0,1]`。权重非负且和为 1；最终权重暂不定值。

## 输入与输出

| 类型 | 字段或信息 |
|---|---|
| 输入 | `innovation_norm`、编码器/电流/时间戳有效性、饱和标志、估计状态有限性、参数适用范围 |
| 输出 | `confidence_score`、`valid_flag`、`reason_codes` |
| 禁止输入 | 负载侧真值、真实外扰、评价标签、最终测试集结论 |

## 强制失效规则

- 时间戳乱序或非有限：`valid_flag=false`，记录 `INVALID_TIMESTAMP`；
- 编码器无效：`valid_flag=false`，记录 `INVALID_ENCODER`；
- 电流或测量力矩无效：至少记录 `INVALID_CURRENT` 并进入保守处理；
- 估计或创新出现 NaN/Inf：`valid_flag=false`；
- 未知枚举、未知原因码或越界评分：按低可信处理；
- 信号恢复后不得立即跳回高可信，必须满足滞回和最小恢复窗口。

## 校准与验收

阈值只能使用调试集确定，最终评价集不得用于选权重、阈值或恢复窗口。P3 前需要
覆盖传感器故障、参数失配、饱和、乱序和模型外工况，并报告误判、漏判及恢复
行为。没有有效 P1 证据时，本规范不产生性能声明。
