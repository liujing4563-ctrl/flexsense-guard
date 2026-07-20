# 接口规范

## 电机侧输入 `MotorSideMeasurement`

| 字段 | 单位 | 说明 |
|---|---:|---|
| `timestamp_s` | s | 仿真时间戳 |
| `motor_position_rad` | rad | 电机侧位置 |
| `motor_velocity_rad_s` | rad/s | 电机侧速度 |
| `motor_current_a` | A | 电机电流 |
| `motor_torque_nm` | Nm | 电机侧力矩估计或测量 |
| `torque_command_nm` | Nm | 力矩指令 |
| `encoder_valid` / `current_valid` / `timestamp_valid` | - | 信号有效性 |
| `saturation_flag` | - | 执行器饱和标志 |

## 虚拟感知输出 `VirtualSensingEstimate`

| 字段 | 单位 | 说明 |
|---|---:|---|
| `estimated_load_position_rad` | rad | 负载侧位置估计 |
| `estimated_load_velocity_rad_s` | rad/s | 负载侧速度估计 |
| `estimated_torsion_rad` | rad | 扭转角估计 |
| `estimated_external_torque_nm` | Nm | 外部扰动力矩估计 |
| `innovation_norm` | - | 创新残差范数 |
| `confidence_score` | [0,1] | 工程可信评分，不是概率 |
| `contact_score` | [0,1] | 接触证据评分，不是概率 |
| `operation_mode` | - | `normal`、`vibration_suppression`、`safe_slowdown` 或 `degraded` |
| `valid_flag` / `reason_codes` | - | 有效性和可追溯原因 |

## 不变量

- 不定义终端力输出；若未来需要力，必须显式声明 Jacobian 或力臂和变换模型。
- 禁止 `contact_probability` 字段。
- 负载侧位置、速度和外扰真值只用于离线评估。
