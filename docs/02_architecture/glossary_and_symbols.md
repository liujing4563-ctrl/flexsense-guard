# 术语与符号表

## 使用规则

本文件是术语、符号、力矩所在侧和单位的权威索引。公式以
[`system_architecture.md`](system_architecture.md) 为准，公共字段以
[`interface_spec.md`](interface_spec.md) 为准，当前状态以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。

## 领域术语

| 术语 | 本项目定义 |
|---|---|
| Plant | 被仿真的双惯量柔性关节真实对象，持有仿真真值和不可变真实参数 |
| Observer | 只使用 `ObserverInput` 估计不可测负载状态和外扰的观测器 |
| Controller | 根据参考值、估计和模式产生 `ControlCommand` 的模块 |
| Signal Health | 检查时间戳、编码器、电流、转矩反馈和数据新鲜度的模块 |
| Confidence | 根据归一化残差、信号健康、物理合理性和模型适用性产生工程评分的机制 |
| Classification | 根据允许的估计与特征输出分类状态和接触证据评分的模块 |
| Mode Manager | 产生运行模式、危险锁存和最小安全动作级别的模块 |
| Calibration | 生成候选名义参数的受控过程，不直接更新 Plant 或当前名义版本 |
| Acceptance | 对候选名义参数作 `UPDATE`、`HOLD` 或 `ROLLBACK` 决定的过程 |
| Offline Validation | 唯一允许使用仿真真值计算指标和阶段结论的离线过程 |
| Runtime Data | 允许运行时模块读取的专用 DTO 数据 |
| Ground Truth | Plant 真实状态、真实外扰和真实参数，只能进入 Plant 或离线评价 |
| Nominal Parameter | Observer 或 Controller 使用的版本化名义参数 |
| External Joint Torque | 作用在负载关节坐标中的带符号外部广义力矩，不是末端力 |
| Contact Score | `[0,1]` 的接触证据评分，不是概率 |
| Confidence Score | `[0,1]` 的工程可信评分，不是概率 |
| Contact Hazard Latch | 已确认接触危险的独立记忆，不因 operation mode 改变而自动清除 |
| Safety Action Level | Controller 必须满足的最小保守动作包络 |

## 机械符号

| 符号 | 公共名称 | 单位 | 定义与正方向 |
|---|---|---:|---|
| `theta_m` | `motor_position_rad` | rad | 电机侧角位置 |
| `omega_m` | `motor_velocity_rad_s` | rad/s | 电机侧角速度 |
| `theta_g` | 齿轮输出侧角位置 | rad | 柔性元件之前的坐标，`theta_m/N` |
| `omega_g` | 齿轮输出侧角速度 | rad/s | 柔性元件之前的坐标，`omega_m/N` |
| `theta_l` | `load_position_rad` | rad | 负载侧角位置；运行时只能使用估计值 |
| `omega_l` | `load_velocity_rad_s` | rad/s | 负载侧角速度；运行时只能使用估计值 |
| `N` | `gear_ratio` | - | 电机侧与齿轮输出侧运动量之比，`theta_g=theta_m/N` |
| `J_m` | `motor_inertia_kg_m2` | kg·m² | 电机侧等效惯量，必须大于 0 |
| `J_l` | `load_inertia_kg_m2` | kg·m² | 负载侧惯量，必须大于 0 |
| `K_s` | `shaft_stiffness_nm_rad` | N·m/rad | 按负载侧扭转坐标定义的刚度 |
| `D_s` | `shaft_damping_nms_rad` | N·m·s/rad | 按负载侧相对角速度定义的阻尼 |
| `q` | `torsion_rad` | rad | `theta_g-theta_l=theta_m/N-theta_l` |
| `tau_s_load_nm` | 负载侧弹性力矩 | N·m | `K_s*q+D_s*q_dot` |
| `tau_s_motor_nm` | 电机侧反射弹性力矩 | N·m | 本阶段理想齿轮下为 `tau_s_load_nm/N` |
| `tau_ext_nm` | 外部关节广义力矩 | N·m | 正值沿负载坐标正方向，负值沿负方向 |
| `tau_fl_nm` | 负载侧摩擦广义力矩 | N·m | 实际广义力矩，正常情况下与 `omega_l` 方向相反 |
| `tau_fm_resist_nm` | 电机侧阻力项 | N·m | `b_m*omega_m+tau_c_m*sign(omega_m)`，在电机方程中减去 |

本阶段固定 `eta=1`，不冻结一般双向齿轮效率公式。效率、回程差和非理想传动需要
独立模型、接口变更和新的功率/能量推导。

## 运行时 DTO

| DTO | 关键内容 | 允许消费者 |
|---|---|---|
| `ActuatorCommand` | 执行器前力矩指令 | Actuator、Validation |
| `PlantInputTrace` | 实际施加力矩、饱和和限制 | Plant、Validation；禁止 Observer |
| `RawMotorMeasurement` | 电机位置、速度、电流和原始有效标志 | Torque Feedback、Signal Health |
| `TorqueFeedback` | Observer 可见转矩反馈、来源、有效性和标准差 | Signal Health、ObserverInput |
| `SignalHealthStatus` | 健康标志、陈旧、饱和和原因码 | ObserverInput、Confidence、Mode |
| `ObserverInput` | 合法电机侧状态和转矩反馈 | Observer |
| `ObserverEstimate` | 负载状态、外扰估计和归一化残差 | Confidence、Classification、Validation |
| `ConfidenceOutput` | `valid_flag`、工程评分和原因码 | Classification、Mode、Validation |
| `ClassificationOutput` | 分类和接触证据评分 | Mode、Validation |
| `ModeDecision` | 运行模式、危险锁存和安全动作级别 | Controller、Validation |
| `SystemStateSnapshot` | 上述输出的只读时间对齐快照 | App、报告、Validation |

`motor_torque_applied_nm` 是仿真 Plant 输入追踪值。Observer 只允许读取
`motor_torque_feedback_nm`。旧公共字段 `motor_torque_nm` 和
`motor_torque_measured_nm` 不再作为 v2 当前权威字段。

## 状态与证据术语

| 术语 | 定义 |
|---|---|
| `PASS` | 证据有效、充分、可复现，并满足批准门禁 |
| `FAIL` | 证据有效，但至少一个强制门禁未满足 |
| `NOT_VERIFIED` | 证据无效、不充分、不可复现或没有运行 |
| `NOT_RUN` | 命令或环境没有实际执行 |
| `PROVISIONAL` | 有待应用需求或有效实验确认的工程门限 |
| `MOCK` | 仅用于契约联调的样例，不是算法证据 |
| `energy_proxy_j` | 机械功率绝对值积分代理，不等于驱动器电能 |

## 禁止用语

- 禁止公共字段 `contact_probability`；
- 没有 Jacobian、等效力臂和坐标变换时不称为末端力；
- 不把目录、Mock、占位代码或未运行命令称为已完成功能；
- 不把历史执行 `FAIL` 直接解释为当前技术路线 `FAIL`；
- 不把 `REVIEWED` 的规范描述为实现或实验已经验证。
