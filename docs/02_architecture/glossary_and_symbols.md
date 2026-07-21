# 术语与符号表

## 使用规则

本文件是项目术语、符号、力矩所在侧和单位的权威索引。公式定义以
[`system_architecture.md`](system_architecture.md) 为准，公共字段以
[`interface_spec.md`](interface_spec.md) 为准。代码可以使用语言惯用命名，但不得
改变本表语义。

## 领域术语

| 术语 | 本项目定义 |
|---|---|
| Plant | 被仿真的双惯量柔性关节真实对象，持有仿真真值和真实参数 |
| Observer | 只使用允许运行时输入估计不可测负载侧状态和外扰的观测器 |
| Controller | 根据参考值、估计状态和运行模式产生 `torque_command_nm` 的模块 |
| Signal Health | 检查时间戳、编码器、电流、力矩和数据新鲜度，不估计负载状态的模块 |
| Confidence | 根据残差、信号健康、物理合理性和模型适用性给出工程可信评分的机制 |
| Classification | 根据允许的估计与特征输出分类状态和接触证据评分的模块 |
| Validation | 使用冻结协议和仿真真值计算指标、保存证据的离线评价过程 |
| Acceptance | 根据证据有效性和冻结门禁作出 `PASS`、`FAIL` 或 `NOT_VERIFIED` 决定的过程 |
| Calibration | 在受控条件下提出、评价、更新或回滚候选参数的过程 |
| Identification | 从允许数据估计模型参数的过程；不等同于在线校准或状态估计 |
| Runtime Data | 可在运行链中流向 Observer、Confidence、Classification、Mode Manager 和 Control 的数据 |
| Ground Truth | Plant 真实状态、真实外扰和真实参数，只能进入离线 Validation |
| Nominal Parameter | Observer 或控制器实际使用的名义参数，必须与 Plant 真实参数分离 |
| True Parameter | Plant 用于生成仿真真值的参数，禁止作为运行时算法输入 |
| External Joint Torque | 作用在负载侧关节坐标中的外部扰动力矩，不是未经映射的末端力 |
| Contact Score | `[0,1]` 的接触证据评分，不是碰撞概率或统计概率 |
| Confidence Score | `[0,1]` 的工程可信评分，不是统计概率 |
| Operation Mode | Mode Manager 输出的离散运行模式，不直接等同于底层控制律 |
| Reason Code | 解释无效、低可信、降级或回退原因的稳定字符串标识 |

## 机械符号

| 符号 | 公共名称 | 单位 | 定义与正方向 |
|---|---|---:|---|
| `theta_m` | `motor_position_rad` | rad | 电机侧角位置 |
| `omega_m` | `motor_velocity_rad_s` | rad/s | 电机侧角速度 |
| `theta_l` | `load_position_rad` | rad | 负载侧角位置；运行时只允许使用估计值 |
| `omega_l` | `load_velocity_rad_s` | rad/s | 负载侧角速度；运行时只允许使用估计值 |
| `N` | `gear_ratio` | - | 电机侧运动量与负载侧运动量之比；理想刚性关系为 `theta_l = theta_m / N` |
| `J_m` | `motor_inertia_kg_m2` | kg·m² | 电机侧等效惯量，必须大于 0 |
| `J_l` | `load_inertia_kg_m2` | kg·m² | 负载侧惯量，必须大于 0 |
| `K_s` | `shaft_stiffness_nm_rad` | N·m/rad | 负载侧定义的传动弹性刚度 |
| `D_s` | `shaft_damping_nms_rad` | N·m·s/rad | 负载侧定义的传动阻尼 |
| `eta` | `transmission_efficiency` | - | 传动效率；当前 P1 暂取 1 |
| `tau_s_load_nm` | 负载侧弹性力矩 | N·m | `K_s(theta_m/N-theta_l)+D_s(omega_m/N-omega_l)` |
| `tau_s_motor_nm` | 电机侧反射弹性力矩 | N·m | 当前 `eta=1` 时为 `tau_s_load_nm/N`；一般形式为 `tau_s_load_nm/(eta*N)` |
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
