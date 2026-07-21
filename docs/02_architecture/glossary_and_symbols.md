# 术语与符号表

## 使用规则

本文件是项目术语、符号、力矩所在侧和单位的权威索引。公式定义以
[`system_architecture.md`](system_architecture.md) 为准，公共字段以
[`interface_spec.md`](interface_spec.md) 为准。代码可以使用语言惯用命名，但不得
改变本表语义。

## 机械符号

| 符号 | 公共名称 | 单位 | 定义与正方向 |
|---|---|---:|---|
| `theta_m` | `motor_position_rad` | rad | 电机侧角位置 |
| `omega_m` | `motor_velocity_rad_s` | rad/s | 电机侧角速度 |
| `theta_l` | `load_position_rad` | rad | 负载侧角位置；运行时只允许使用估计值 |
| `omega_l` | `load_velocity_rad_s` | rad/s | 负载侧角速度；运行时只允许使用估计值 |
| `N` | `gear_ratio` | - | 正传动比，理想刚性关系为 `theta_l = theta_m / N` |
| `J_m` | `motor_inertia_kg_m2` | kg·m² | 电机侧等效惯量，必须大于 0 |
| `J_l` | `load_inertia_kg_m2` | kg·m² | 负载侧惯量，必须大于 0 |
| `K_s` | `shaft_stiffness_nm_rad` | N·m/rad | 负载侧定义的传动弹性刚度 |
| `D_s` | `shaft_damping_nms_rad` | N·m·s/rad | 负载侧定义的传动阻尼 |
| `eta` | `transmission_efficiency` | - | 传动效率；当前 P1 暂取 1 |
| `tau_s_load_nm` | 负载侧弹性力矩 | N·m | `K_s(theta_m/N-theta_l)+D_s(omega_m/N-omega_l)` |
| `tau_s_motor_nm` | 电机侧反射弹性力矩 | N·m | `tau_s_load_nm/(eta*N)` |
| `tau_ext_nm` | 外部关节扰动力矩 | N·m | 正值表示沿负载侧正运动方向的阻力矩 |
| `tau_fm_nm` | 电机侧摩擦力矩 | N·m | 与 `omega_m` 方向相反 |
| `tau_fl_nm` | 负载侧摩擦力矩 | N·m | 与 `omega_l` 方向相反 |

## 公共力矩字段

| 字段 | 所在侧 | 含义 | 允许消费者 |
|---|---|---|---|
| `torque_command_nm` | 电机侧 | 饱和和执行器模型之前的控制意图 | 执行器模型、Validation |
| `motor_torque_applied_nm` | 电机侧 | 执行器约束后实际施加给 Plant 的力矩 | Plant、测量模型、Validation |
| `motor_torque_measured_nm` | 电机侧 | Observer 可使用的可追溯测量力矩 | Signal Health、Observer、Validation |

旧字段 `motor_torque_nm` 语义不明确，禁止继续加入新的公共接口。MATLAB 历史代码
中的同名字段必须由 Simulink 同学在 P1 输入一致性任务中迁移。

## 状态与证据术语

| 术语 | 定义 |
|---|---|
| `PASS` | 证据有效、充分、可复现，并满足冻结门禁 |
| `FAIL` | 证据有效，但至少一个强制性能条件未满足 |
| `NOT_VERIFIED` | 缺少证据，或证据无效、不充分、不可复现 |
| `PASSED` / `FAILED` / `NOT RUN` | 单条命令或检查的实际运行状态，不是阶段结论 |
| `MOCK` | 仅用于接口联调的虚构样例，不是仿真或实验结果 |
| `confidence_score` | `[0,1]` 的工程可信评分，不是概率 |
| `contact_score` | `[0,1]` 的接触证据评分，不是概率 |
| `energy_proxy_j` | 机械功率绝对值积分形成的仿真代理指标，不等于驱动器电能 |

## 禁止用语

- 禁止公共字段 `contact_probability`；
- 没有 Jacobian、等效力臂和坐标变换时，不称为“末端力”；
- 不把目录、占位文件、Mock 数据或未运行命令称为已完成功能；
- 不把历史执行 `FAIL` 直接解释为当前技术路线 `FAIL`。
