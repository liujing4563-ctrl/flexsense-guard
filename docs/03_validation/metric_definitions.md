# 指标定义

## 通用计算规则

每个案例先在预先登记的有效评价窗口中计算指标，再按负载、场景和算法报告全部
seed。连续指标至少报告中位数、第一四分位数、第三四分位数和失败案例数；计数
指标同时报告总数与逐案例分布。不得只报告最好 seed。

NaN、Inf、发散、提前终止或缺失必需样本不能静默删除。无法计算的指标不写 0 或
NaN 到 JSON，而是令案例 `valid_flag=false`，记录失败原因并计入失败数。

## 状态估计指标

| 指标 | 数学定义 | 单位 | 统计窗口 | 无效数据处理 | 多 seed 聚合 | 阶段 | 生产模块 | 消费模块 |
|---|---|---:|---|---|---|---|---|---|
| `load_position_rmse_rad` | `sqrt(mean((estimated_load_position_rad-true_load_position_rad)^2))` | rad | 冻结 P1 评价窗口 | 缺真值、非有限或样本不足时案例无效 | 中位数、Q1、Q3、失败数、优于 baseline 数 | P1 | Validation | Acceptance、报告 |
| `load_velocity_rmse_rad_s` | `sqrt(mean((estimated_load_velocity_rad_s-true_load_velocity_rad_s)^2))` | rad/s | 冻结 P1 评价窗口 | 同上 | 中位数、Q1、Q3、失败数 | P1 | Validation | Acceptance、报告 |
| `external_torque_rmse_nm` | `sqrt(mean((estimated_external_torque_nm-true_external_torque_nm)^2))` | N·m | 预注册外扰评价窗口 | 无外扰真值、非有限或样本不足时省略并标原因 | 中位数、Q1、Q3、失败数 | P1 可选诊断/P2 | Validation | Classification 评价、报告 |
| `maximum_absolute_error` | `max(abs(estimate-reference))`，必须同时记录被测字段 | 与被测字段一致 | 与对应 RMSE 相同 | 不用有限子集掩盖非有限样本 | 中位数、Q1、Q3、全局最大值、失败数 | P1/P2/P3 | Validation | Acceptance、风险审查 |

真值只允许由离线 Validation 使用，不能回流 Observer、Confidence、
Classification、Mode Manager 或 Control。

## 振动与事件指标

| 指标 | 数学定义 | 单位 | 统计窗口 | 无效数据处理 | 多 seed 聚合 | 阶段 | 生产模块 | 消费模块 |
|---|---|---:|---|---|---|---|---|---|
| `vibration_rms` | `sqrt(mean((x-mean(x))^2))`，并记录 `x` 的字段和滤波定义 | 与 `x` 一致 | 冻结无接触振动窗口 | 窗口、信号或滤波定义缺失时无效 | 中位数、Q1、Q3、失败数 | P2/控制验收 | Validation | Classification、Control、报告 |
| `false_alarm_count` | 无真实接触事件被判为接触的合并事件数量 | count | 完整案例及预注册事件合并窗口 | 缺标签或合并规则时无效 | 总数、中位数、Q1、Q3、失败数 | P2/P3 | Validation | Acceptance、报告 |
| `missed_detection_count` | 真实接触未在预注册检测窗口内形成有效检出的事件数量 | count | 每个真实接触事件的检测窗口 | 缺标签或窗口时无效 | 总数和逐案例分布 | P2/P3 | Validation | Acceptance、报告 |
| `detection_delay_s` | `t_first_valid_detection-t_contact_start` | s | 每个被成功检出的接触事件 | 漏检不写 0；计入漏检并标记该延迟不可用 | 成功事件中位数、Q1、Q3、最大值及漏检数 | P2/P3 | Validation | Control、Acceptance、报告 |
| `stopping_time_s` | `t_stop_criterion-t_first_valid_detection` | s | 检出后至冻结停止判据或案例结束 | 未停止时记录失败，不用案例结束时间冒充停止 | 成功事件分位数、最大值、未停止数 | P3/集成 | Validation | Control、Acceptance、报告 |
| `post_contact_travel_rad` | 检出后至停止或窗口结束的负载侧累计角位移绝对值 | rad | 有效检出后冻结窗口 | 无有效检出时标不可用并关联漏检 | 中位数、Q1、Q3、最大值、失败数 | P3/集成 | Validation | Control、Acceptance、报告 |

事件必须先按预注册合并窗口形成事件级记录，不能按采样点重复累计误报或漏报。

## 能量与资源指标

| 指标 | 数学定义 | 单位 | 统计窗口 | 无效数据处理 | 多 seed 聚合 | 阶段 | 生产模块 | 消费模块 |
|---|---|---:|---|---|---|---|---|---|
| `energy_proxy_j` | `integral(abs(motor_torque_applied_nm*motor_velocity_rad_s), dt)` | J | 完整案例或冻结动作窗口 | 时间戳、力矩或速度无效时案例无效 | 中位数、Q1、Q3、最大值、失败数 | P1/控制验收 | Validation | Acceptance、报告 |
| `runtime_ms` | 被测步骤的墙钟时间或目标平台单调时钟差，必须说明计时边界 | ms | 预热后全部被测调用 | 环境、计时器或样本数缺失时不作实时性结论 | 中位数、P95、最大值、失败数 | P1/SIL/集成 | 运行器/SIL | Acceptance、报告 |
| `memory_bytes` | 被测进程或算法实例的峰值已用内存 | byte | 初始化后至案例结束 | 平台或测量工具未记录时写 `NOT RUN` | 中位数、P95、最大值、失败数 | SIL/集成 | SIL/运行器 | Acceptance、报告 |

`energy_proxy_j` 是仿真机械能量代理，不等同于真实驱动器电能消耗、热损耗或电池
能耗。`runtime_ms` 和 `memory_bytes` 只有在声明的目标平台实际测量后才能支持实时性
或资源声明。
