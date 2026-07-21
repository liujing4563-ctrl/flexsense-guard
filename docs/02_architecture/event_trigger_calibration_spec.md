# 事件触发校准规范

规范状态和实现状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。目标规范尚未
实现；现有 `calibration_trigger.m` 和 `update_gate.m` 是
`OUTDATED / NON-COMPLIANT IMPLEMENTATION`，本规范不修改其源码。

## 配置边界

Calibration 只能读取当前 `NominalParameterVersion` 并生成
`CalibrationCandidate`。它禁止读取或修改 `ImmutablePlantTrueConfig`。

Acceptance 只能将决定应用于 `VersionedNominalParameterStore`：

- `UPDATE`：原子写入已验收候选，并保留旧版本；
- `HOLD`：保持当前名义版本不变；
- `ROLLBACK`：恢复 `rollback_target_version` 指向的上一有效版本。

回滚不是把参数或状态清零。没有有效备份版本时禁止执行 `ROLLBACK`。

## 允许提出候选的条件

- 受控启动校准阶段或计划维护窗口；
- 工具、负载或已登记运行配置变化；
- 归一化创新持续偏大，且信号仍有效；
- 存在 `MODEL_MISMATCH_SUSPECTED`，且没有硬失效或接触危险；
- 当前参数在独立运行时监测窗口持续不满足已批准适用性条件。

触发条件只允许提出候选，不代表允许执行或更新。

## 禁止条件

- `contact_hazard_latched=true`；
- `EXTERNAL_CONTACT`、`SAFE_SLOWDOWN` 或 `LOW_CONFIDENCE_DEGRADED`；
- 编码器、时间戳或转矩反馈无效；
- 数据陈旧、Observer 发散或输出非有限；
- 执行器持续饱和；
- 没有经过校验的上一有效名义参数版本；
- 上一事件仍在执行、验收、冷却或回滚；
- 候选参数越过批准的物理边界；
- 使用最终评价集或负载侧真值选择候选。

只有明确属于可校准模型失配、且信号有效时，才允许进入候选生成。单纯低评分、
外部动态嫌疑或真实接触不构成校准许可。

## `CalibrationCandidate`

候选必须包含：

```text
candidate_id
base_parameter_version
candidate_parameter_version
parameter_values
generation_reason
acceptance_window_id
```

`base_parameter_version` 必须与生成候选时的当前批准版本一致。参数值需要物理边界、
变化率和所属模块说明；候选不能包含 Plant 真参数。

## 在线和离线验收隔离

在线 Acceptance 只能使用运行时可得代理指标，例如归一化残差、有限性、信号健康、
控制约束和模式行为。离线 Validation 可以使用负载侧真值评价候选质量，但不能控制
同一次在线 `UPDATE/HOLD/ROLLBACK`。

候选生成窗口和验收窗口必须隔离，最终评价集不得用于选择参数、窗口或门限。

## UPDATE、HOLD、ROLLBACK

- `UPDATE`：候选满足全部强制门禁、证据有效且优于当前名义版本时原子应用；
- `HOLD`：证据不足、改善不显著、处于冷却或检查失败时保持当前版本；
- `ROLLBACK`：已应用候选导致退化、失稳、非有限或模式异常时恢复上一有效版本。

每个决定保存 candidate、base、target、验收窗口、原因码、证据和参数校验值。失败
证据不得删除。

## 冷却、间隔和执行窗口

冷却时间、最小事件间隔、激励幅值、持续时间、参数集合、步长和验收阈值尚未确定，
需要有效 Plant、P1 和后续校准实验。执行窗口必须可中止；硬失效、饱和、危险锁存
或安全模式抢占时立即停止并作 `HOLD` 或有效 `ROLLBACK`。

## 记录要求

每次事件记录事件 ID、触发/禁止条件、模式、危险锁存、原因码、输入窗口、当前版本、
候选版本、备份校验、验收窗口、决定、失败原因、提交和实际运行状态。未运行检查
写 `NOT_RUN`。
