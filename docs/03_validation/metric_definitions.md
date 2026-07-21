# 指标定义

## 通用规则

所有指标必须记录单位、评价窗口、采样时间、聚合方式和异常案例处理。单次运行先
计算案例指标，再按负载和场景报告全部 seed 的中位数、分位数及成功 seed 数；
不得只报告最好结果。

## 状态估计指标

| 指标 | 定义 | 单位 |
|---|---|---:|
| `load_position_rmse_rad` | `sqrt(mean((estimated_load_position_rad-true_load_position_rad)^2))` | rad |
| `load_velocity_rmse_rad_s` | `sqrt(mean((estimated_load_velocity_rad_s-true_load_velocity_rad_s)^2))` | rad/s |
| `external_torque_rmse_nm` | `sqrt(mean((estimated_external_torque_nm-true_external_torque_nm)^2))` | N·m |
| `vibration_velocity_rms_rad_s` | 指定无接触窗口内负载侧振动速度的 RMS | rad/s |

真值只允许在离线评价中使用。

## 分类与安全指标

| 指标 | 定义 | 单位 |
|---|---|---:|
| `false_alarm_count` | 正常/振动窗口被判为接触的事件数 | count |
| `missed_detection_count` | 接触事件未在冻结窗口内检出的数量 | count |
| `detection_delay_s` | 接触开始到首次有效检出的时间 | s |
| `post_contact_travel_rad` | 有效检出后到停止或窗口结束的负载侧角位移绝对值 | rad |
| `stopping_time_s` | 有效检出到满足冻结停止判据的时间 | s |

事件合并窗口、停止速度阈值和最大检测窗口均为阶段配置，不得在查看最终评价结果
后调整。

## 能量与资源指标

能量代理定义为：

```text
energy_proxy_j = integral(abs(motor_torque_applied_nm * motor_velocity_rad_s), dt)
```

`energy_proxy_j` 是仿真机械能流代理，不等同于真实驱动器电能消耗。若使用其他
代理公式，必须改用不同字段名并说明原因。

资源指标至少包括单步执行时间的中位数、95 分位数和最大值，以及峰值内存。仅在
目标平台真实运行后才能作实时性声明。

## 非有限值和失败

出现 NaN、Inf、发散、提前终止或缺失样本时，该案例不能从统计中静默删除。必须
标记失败分类并计入成功 seed 数；若指标无法计算，阶段证据有效性由验收矩阵决定。
