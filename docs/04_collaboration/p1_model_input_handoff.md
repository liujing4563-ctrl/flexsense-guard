# P1 双惯量模型与 Plant/Observer 输入一致性修复交接单

## 1. 任务目标

修复 MATLAB 双惯量 Plant、EKF 和 P1 输入链的物理一致性，使后续 P1 复验具备
有效基础。本任务不负责证明 P1 已通过，也不通过调整算法参数获得性能结论。

## 2. 当前问题

1. 负载侧弹性力矩与电机侧反射力矩此前未明确区分；
2. Plant 内部使用饱和后的实际力矩；
3. Observer 使用饱和前的 `torque_command_nm`；
4. Plant 和 Observer 当前使用的物理输入不一致；
5. EKF 状态方程和雅可比仍对应旧力矩模型；
6. `seed=0` 不能保证复现；
7. 当前 P1 runner 只有单负载、单场景和单 seed；
8. 当前 runner 使用评价真值选择 Q；
9. 当前 P1 结果证据无效或不足；
10. MATLAB 尚未完成新公共输入接口迁移。

历史 P1 执行结果必须保留为 `FAIL`，但上述问题意味着它不能证明 EKF 路线或
负载侧状态估计不可行。当前 P1 可行性结论只能为 `NOT_VERIFIED`。

```text
Historical P1 execution result: FAIL
Evidence validity: INVALID / INSUFFICIENT
Current P1 feasibility decision: NOT_VERIFIED
P2: BLOCKED
P3: BLOCKED
```

## 3. 冻结的数学语义

电机侧状态为 `theta_m`、`omega_m`，负载侧状态为 `theta_l`、`omega_l`。传动比
`N` 的方向冻结为 motor-side motion / load-side motion，即理想刚性关系为
`theta_l = theta_m / N`。

负载侧弹性力矩定义为：

```text
tau_s_load_nm
= K_s * (theta_m / N - theta_l)
+ D_s * (omega_m / N - omega_l)
```

P1 基线暂定理想齿轮效率 `eta = 1`，电机侧反射弹性力矩为：

```text
tau_s_motor_nm = tau_s_load_nm / N
```

电机侧与负载侧动力学分别为：

```text
J_m * theta_m_ddot
= motor_torque_applied_nm - tau_s_load_nm / N - tau_fm

J_l * theta_l_ddot
= tau_s_load_nm - tau_ext_nm - tau_fl
```

`tau_s_load_nm` 始终表示负载侧弹性力矩，不得继续使用含义不清的 `tau_s` 作为
跨模块公共字段。若后续加入效率 `eta`，必须先独立冻结效率方向、功率关系和方程，
不得只在代码中临时插入效率项。

## 4. 三类力矩字段

| 字段 | 冻结含义 | 生产者 | 消费者 |
|---|---|---|---|
| `torque_command_nm` | 控制器或场景产生的期望电机侧力矩指令 | Control / Scenario | 执行器模型、Validation |
| `motor_torque_applied_nm` | 饱和、限制和执行器模型后实际作用于 Plant 的电机侧力矩 | 执行器模型 | Plant、测量模型、Validation |
| `motor_torque_measured_nm` | Observer 可获得的电机侧力矩测量或估计值 | 测量模型 / 电流换算 | Observer、Signal Health、Validation |

数据流冻结为：

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

Observer 禁止直接把 `torque_command_nm` 当作实际施加力矩。没有独立转矩传感器
模型时，可明确采用 `motor_torque_measured_nm = motor_torque_applied_nm + noise`，
但噪声模型、随机种子和单位必须可追溯。

## 5. 真值边界

以下真值只能进入 Validation 和离线评价：

- `true_load_position_rad`；
- `true_load_velocity_rad_s`；
- `true_external_torque_nm`；
- Plant 真实参数。

它们禁止进入 Observer、Confidence、Classification、Mode Manager 和 Control。
Plant 真实参数与 Observer 名义参数必须使用独立结构，并记录失配比例。

## 6. Simulink 同学需要完成的工作

| 编号 | 工作 | 本任务关系 |
|---|---|---|
| `P1-RECOVERY-01` | 修改 MATLAB Plant 的齿轮力矩反射 | 当前修复 |
| `P1-RECOVERY-02` | 输出 `motor_torque_applied_nm` | 当前修复 |
| `P1-RECOVERY-03` | 建立 `motor_torque_measured_nm` 测量模型 | 当前修复 |
| `P1-RECOVERY-04` | 使 Observer 只使用 `motor_torque_measured_nm` | 当前修复 |
| `P1-RECOVERY-05` | 同步修正 EKF 状态方程和雅可比 | 当前修复 |
| `P1-RECOVERY-06` | 修复 `seed=0` 复现问题 | 当前修复 |
| `P1-RECOVERY-07` | 增加无耗散能量一致性测试 | 当前修复 |
| `P1-RECOVERY-08` | 增加输入一致性测试 | 当前修复 |
| `P1-RECOVERY-09` | 重建三负载、10 seed P1 runner | 后续任务，本轮不实现 |

仓库 Issue 可用 `P1-RECOVERY-01` 作为本轮恢复工作的总任务编号；上表其余编号是
同一交付链中的可验收子任务，后续可按 PR 规模拆分。

## 7. 验收标准

- [ ] `tau_s_load_nm` 的定义在文档、Plant 和 EKF 中一致
- [ ] 电机侧方程使用 `tau_s_load_nm / N`
- [ ] 负载侧方程使用 `tau_s_load_nm`
- [ ] Plant 输入为 `motor_torque_applied_nm`
- [ ] Observer 输入为 `motor_torque_measured_nm`
- [ ] Observer 不直接使用 `torque_command_nm`
- [ ] Plant 输出实际施加力矩
- [ ] Observer 不读取负载侧真值
- [ ] Plant 真实参数和 Observer 名义参数分离
- [ ] EKF 雅可比与修正后的状态方程一致
- [ ] `seed=0` 可以复现
- [ ] 运行结果无 NaN 和 Inf
- [ ] 无耗散、无外力条件下能量变化符合数值误差预期
- [ ] 有耗散条件下机械能不出现无解释的持续增长
- [ ] MATLAB 测试实际运行
- [ ] 未运行内容明确写为 `NOT RUN`

## 8. 非目标

- 不调 Q、R、P 来追求 `PASS`；
- 不降低 P1 门禁；
- 不启动 P2 或 P3；
- 不开发 Confidence、Classification、App、C/SIL 或 Test Agent；
- 不修改历史 P1 数据；
- 不声称 P1 已经通过。

## 9. 交付物

Simulink 同学最终交付修改后的 Plant、EKF 和雅可比，完成三类力矩字段迁移，提供
能量一致性、输入一致性和随机种子复现测试，并附 MATLAB 运行日志、文件变更清单、
风险说明和 Draft PR。任何没有实际运行的检查必须明确标记 `NOT RUN`。

## 10. 分支和 PR

- 建议分支：`fix/p1-model-input-consistency`
- 建议标题：`fix: align P1 dual-inertia model and torque input semantics`
- 主责：Simulink 同学
- 审查：项目负责人同学和至少一位非作者
- 合并：禁止自动合并
- 声明：不得在该 PR 中顺带调参、降低门禁或启动 P2/P3
