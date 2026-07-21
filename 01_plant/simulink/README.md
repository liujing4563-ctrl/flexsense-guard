# Simulink 模型交付接口约定

## 目的

本目录预留给 Simulink 同学后续人工建立 `.slx` 模型。当前尚未实现正式 `.slx`，
本文只冻结未来模型的端口、力矩语义、真值边界和交付要求，不代表模型已经完成。

```text
Historical P1 execution result: FAIL
Evidence validity: INVALID / INSUFFICIENT
Current P1 feasibility decision: NOT_VERIFIED
P2: BLOCKED
P3: BLOCKED
```

## 冻结的力矩语义

```text
torque_command_nm
-> actuator saturation/model
-> motor_torque_applied_nm
-> Plant

motor_torque_applied_nm
-> measurement/noise model
-> motor_torque_measured_nm
-> Observer
```

- `torque_command_nm`：期望的电机侧力矩指令；
- `motor_torque_applied_nm`：执行器约束后实际施加到 Plant 的电机侧力矩；
- `motor_torque_measured_nm`：Observer 可获得的电机侧测量或估计力矩；
- `tau_s_load_nm`：负载侧弹性力矩；
- `tau_s_motor_nm = tau_s_load_nm / N`：理想效率下反射到电机侧的弹性力矩。

不得把含义不清的 `tau_m` 或 `tau_s` 作为跨模块公共端口。Observer 禁止直接把
`torque_command_nm` 当作实际施加力矩。

## 未来端口约定

### Plant 模型（Simulink）

| 端口 | 方向 | 信号 | 单位 | 说明 |
|---|---|---|---|---|
| 1 | 输入 | `motor_torque_applied_nm` | Nm | 实际电机侧输入 |
| 2 | 输入 | `true_external_torque_nm` | Nm | 仿真场景真值，不得传入 Observer |
| 3 | 输出 | `motor_position_rad` | rad | 电机侧测量 |
| 4 | 输出 | `motor_velocity_rad_s` | rad/s | 电机侧测量 |
| 5 | 输出 | `motor_torque_applied_nm` | Nm | 逐样本回传实际施加力矩 |
| 6 | 输出 | `true_load_position_rad` | rad | 仅供 Validation |
| 7 | 输出 | `true_load_velocity_rad_s` | rad/s | 仅供 Validation |
| 8 | 输出 | `tau_s_load_nm` | Nm | 负载侧弹性力矩真值，仅供评价 |

### 执行器与测量模型

执行器子系统接收 `torque_command_nm`，输出 `motor_torque_applied_nm` 和饱和标志。
测量子系统接收实际施加力矩，输出 `motor_torque_measured_nm`。Observer 只接收后者。

### 真值边界

`true_load_position_rad`、`true_load_velocity_rad_s`、
`true_external_torque_nm` 和 Plant 真实参数只能进入 Validation。Observer、
Confidence、Classification、Mode Manager 和 Control 均不得读取这些真值。

### 采样时间

- 基础采样时间：1 ms（1000 Hz）
- 控制频率：与采样时间一致

### 文件命名

- `flex_joint_plant.slx`：主 Plant 模型
- `flex_joint_observer.slx`：Observer 子系统
- `probe_runner.slx`：探针运行框架

### 实现与版本控制要求

1. Plant 真实参数和 Observer 名义参数使用独立结构；
2. 记录三类力矩、有效性标志、仿真真值和评价窗口；
3. 正式 `.slx` 可以提交 Git，但必须由 Simulink 同学实际建立和验证；
4. `slprj/`、`*.slxc`、代码生成缓存和临时日志不得提交；
5. MATLAB 测试未实际运行时必须明确写 `NOT RUN`；
6. 详细修复和验收要求见
   [`p1_model_input_handoff.md`](../../docs/04_collaboration/p1_model_input_handoff.md)。
