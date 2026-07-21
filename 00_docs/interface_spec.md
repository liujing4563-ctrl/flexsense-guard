# 历史接口规范

> 本文件仅用于历史追溯。当前规范以 [`docs/02_architecture/interface_spec.md`](../docs/02_architecture/interface_spec.md) 为准。

## 概述

本文档定义 FlexSense-Guard 项目中核心模块间的数据交换接口。所有接口优先使用 JSON Schema 进行定义，模块间通过标准化数据结构体通信。

---

## 1. 场景配置 `ScenarioConfig`

文件：`common/schemas/scenario_config.schema.json`

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| schema_version | string | - | Schema 版本号（语义化版本） |
| scenario_id | string | - | 场景唯一标识符 |
| payload_level | string | - | 载荷等级：light / medium / heavy |
| sample_time_s | number | s | 仿真采样时间 |
| duration_s | number | s | 仿真总时长 |
| collision_time_s | number | s | 外部接触注入时刻（无接触则 -1） |
| encoder_dropout_rate | number | - | 编码器丢包率 [0, 1] |
| current_noise_std | number | A | 电流测量噪声标准差 |
| torque_constant_error | number | - | 力矩常数偏差比例 |
| observer_parameter_mismatch | number | - | Observer 参数失配比例 |
| random_seed | integer | - | 随机种子（0 表示不固定） |

---

## 2. 系统状态 `SystemState`

文件：`common/schemas/system_state.schema.json`

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| timestamp_s | number | s | 当前时间戳 |
| estimated_load_position_rad | number | rad | 负载侧位置估计值 |
| estimated_load_velocity_rad_s | number | rad/s | 负载侧速度估计值 |
| estimated_torsion_rad | number | rad | 扭转角估计值（θm/N − θl） |
| estimated_external_torque_nm | number | Nm | 外部扰动力矩估计值 |
| innovation_norm | number | - | 创新残差 L2 范数 |
| confidence_score | number | - | 可信评分 [0, 1]，越高越可信 |
| contact_score | number | - | 接触程度评分 [0, 1]（非概率） |
| operation_mode | string | - | 当前操作模式：normal / vibration_suppression / safe_slowdown / degraded |
| valid_flag | boolean | - | 状态数据是否有效 |

---

## 3. 验证报告 `ValidationReport`

文件：`common/schemas/validation_report.schema.json`

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| schema_version | string | - | Schema 版本号 |
| algorithm_version | string | - | 算法版本标识符 |
| git_commit | string | - | 本次运行的 Git commit hash |
| random_seed | integer | - | 使用的随机种子 |
| decision | string | - | 总体判定：pass / fail / inconclusive |
| load_position_rmse | number | rad | 负载侧位置 RMSE |
| load_velocity_rmse | number | rad/s | 负载侧速度 RMSE |
| external_torque_rmse | number | Nm | 外部力矩估计 RMSE |
| false_alarm_count | integer | - | 误报次数（正常被判定为接触） |
| missed_detection_count | integer | - | 漏检次数（接触未被检测） |
| detection_delay_s | number | s | 检测延迟时间 |
| stopping_time_s | number | s | 从检测到完全停止的时间 |
| post_contact_travel_rad | number | rad | 检测后继续运动的弧长 |
| vibration_rms | number | rad/s | 振动速度 RMS |
| energy_proxy | number | - | 能耗代理指标（力矩平方积分） |
| runtime_ms | number | ms | 算法单步执行时间 |
| valid_flag | boolean | - | 报告是否有效 |

---

## 4. Plant-Observer 接口

### Plant 输出（Observer 输入）

```
y_measure = [θm, ωm]       % 电机侧可测量
u_input   = τm              % 电机力矩指令
```

### Observer 内部状态

```
x = [θm, ωm, θl, ωl, τext]ᵀ
```

### Observer 输出

```
y_estimate = [θl_est, ωl_est, τext_est, torsion_est]
confidence  = [innovation_norm, signal_health, confidence_score]
```

### 关键约束

```
Plant真实参数 ≠ Observer名义参数
仿真真值 θl, ωl, τext 禁止传入 Observer
```

---

## 5. 模式管理接口

```
输入:  confidence_score, contact_score, classification_result
输出:  operation_mode: normal | vibration_suppression | safe_slowdown | degraded
       control_command: 根据模式调整后的控制信号
```

## 6. 事件触发校准接口

```
触发条件: confidence_score < threshold_trigger
        且自上次校准以来超过冷却时间

校准动作: 注入低幅探针信号（幅度 < 名义力矩的 5%）
        持续时间: 3~5 个采样步

更新门控: accept: 新估计结果与校准后一致
         hold:  保持当前估计不变
         rollback: 回退到上一个可信状态
```
