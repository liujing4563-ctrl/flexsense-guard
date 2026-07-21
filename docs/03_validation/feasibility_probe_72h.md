# 72 小时技术探针与阶段门

当前阶段状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。本文件定义
探针问题、证据条件和门禁结构，不重复维护当前结论。

## 通用证据要求

- 使用版本化场景配置、固定随机种子和干净工作区；
- 数学模型、力矩所在侧、齿轮方向和符号已经共同确认；
- Plant 真实参数与 Observer 名义参数完全分离；
- 保存 `ActuatorCommand`、`PlantInputTrace`、`TorqueFeedback` 和 `ObserverInput`；
- 证明 Observer 没有读取 `motor_torque_applied_nm` 或任何 Plant 真值；
- 同一比较使用相同输入、场景和评价窗口；
- 调参集与最终评价集预先分离；
- 保存有限性、发散、错误、运行状态和失败案例；
- 未运行环境明确写 `NOT_RUN`；
- 单负载、单 seed 或单张曲线不能作阶段结论。

## P1：负载侧状态估计

P1 只回答负载侧位置和速度的可行性及 Observer 优势，不承担外部扰动力矩可分辨性
的强制门禁。`external_torque_rmse_nm` 可以记录为诊断指标，外部扰动与接触的
可分辨性属于 P2。

### P1 共同实验条件

- 负载：light、medium、heavy；
- 随机种子：至少 0 到 9；
- 工况：名义、轻度/中度参数失配、测量噪声和初始状态失配；
- 失配覆盖负载惯量、刚度、阻尼和摩擦；
- Observer 参数不得与 Plant 真参数完全相同；
- baseline 与 Observer 使用同一合法 `ObserverInput`、场景和窗口；
- 最终评价数据不得用于选择 Q、R、P、阈值或候选算法。

### P1 证据有效性前置条件

1. 理想齿轮和力矩侧定义经过项目负责人、Simulink 同学共同确认；
2. 无耗散模型通过能量一致性检查；
3. Plant 使用 `motor_torque_applied_nm`，Observer 只读取
   `motor_torque_feedback_nm`；
4. ObserverInput 不含 Plant 真值、真实参数或实际施加力矩；
5. Plant 与 Observer 参数对象独立并记录失配；
6. 调试集和评价集分离；
7. 三负载、seed 0 到 9 全部实际运行；
8. 配置、提交、环境、命令、日志和失败证据可追溯。

任一前置条件不满足时，P1-V 和 P1-A 都只能是 `NOT_VERIFIED`。

## P1-V：Load-State Viability Gate

### 问题

仅使用合法 `ObserverInput`，负载侧位置和速度是否达到基本可用水平？

### 强制指标

- `load_position_rmse_rad`；
- `load_velocity_rmse_rad_s`；
- 两者最大绝对误差；
- 有限性和发散标志；
- light、medium、heavy 的逐 seed 结果及分位数；
- 运行时间和失败案例数。

### 工程门限状态

- 仓库现有位置 RMSE 门限 `0.05 rad` 暂保留为
  `PROVISIONAL ENGINEERING GATE`；
- 速度 RMSE 的绝对应用门限尚未确定，必须在运行 P1 前依据任务轨迹、采样率和应用
  需求预注册；
- `0.05 rad` 不是工业标准或统计定理，审查通过前不能作为最终性能承诺；
- 速度门限没有批准前，P1-V 不得判为 `PASS`。

P1-V 通过要求证据有效、无 NaN/Inf、无发散，并且位置和速度均满足运行前批准的
绝对应用门限。它不要求 Observer 必须优于 baseline。

## P1-A：Observer Advantage Gate

### 问题

Observer 相对电机侧直接映射 baseline 是否具有稳定且有工程意义的优势？

baseline 定义为：

```text
load_position_baseline = motor_position / gear_ratio
load_velocity_baseline = motor_velocity / gear_ratio
```

### 公平性要求

- baseline 与 Observer 使用相同合法输入、场景、窗口和真值评价；
- 多负载、多 seed 汇总；
- 调参集与最终评价集分离；
- 不使用评价真值选择 Q/R/P 或最佳候选；
- 报告中位数、Q1、Q3、胜出 seed 数和失败案例。

### 工程门限状态

仓库现有“位置 RMSE 中位数相对 baseline 改善至少 30%，每个负载至少 8/10 seed
胜出”暂保留为 `PROVISIONAL ENGINEERING GATE`。本轮不静默改成其他数值。该门限
不是工业标准或统计定理，必须结合任务精度和 baseline 水平重新确认。

位置/速度 RMSE、最大瞬时误差、逐负载判定、多 seed 聚合、允许失败 seed 数和
NaN/Inf/发散计入方式，必须在正式评价集解封前预注册。门限只能在解封前修改；每次
修改必须记录 Decision ID、依据、批准人和适用配置。评价集解封后不得再修改本轮门限，
需要修改时必须结束当前活动并建立新的未见评价配置和实验 ID。

P1-A 未通过不表示负载侧状态不可估计。如果 P1-V 通过而 P1-A 未通过，进入
`P1_REFRAME_REVIEW`，并且只能决定 `CONTINUE_TO_ROUTE_B`、
`ONE_BOUNDED_REPAIR` 或 `ENTER_ROUTE_C`。有限修复最多一次，不得使用已解封评价集
调参；修复后必须使用新的独立评价配置。

## P2：状态可分辨性

P2 只有在 P1-V 通过并经人工审查后才能启动。

### P2-VIB

验证柔性振动能否与正常加减速和参数变化稳定区分。记录振动特征、误报、漏报、
检测延迟、多场景和多 seed 结果。量化门限尚未确定，必须在实验前预注册。

### P2-CONTACT

验证外部接触能否与正常动态、柔性振动和摩擦变化稳定区分。记录外扰估计诊断量、
接触事件级误报、漏报和检测延迟。量化门限尚未确定，必须在实验前预注册。

P2-VIB 通过而 P2-CONTACT 失败时，B 路线只能保留振动相关能力，不保留可靠接触
识别主张。

## P3：可信失效与动作

P3 只有在 P1-V 通过后才能启动；依赖接触分类的场景还要求 P2-CONTACT 通过。

### P3-DEGRADE

验证编码器无效、时间戳倒退、数据陈旧、Observer 发散、参数失配和执行器饱和时，
`valid_flag`、`confidence_score` 和原因码是否正确变化。

### P3-ACTION

验证低可信和接触危险同时发生时，`safety_action_level` 是否采用更保守动作，且
低可信模式不会清除 `contact_hazard_latched`。

### P3-RECOVERY

验证故障解除后是否经过滞回、最小保持和危险解除条件，再恢复到正常策略。

三个 P3 子门的量化阈值尚未确定。P3 任一子门失败时，相关 Confidence 或安全动作
只能用于诊断或演示，不得形成完整可信安全闭环声明。

## 路线决定

| 证据结果 | 路线 |
|---|---|
| P1-V、P1-A、P2-VIB、P2-CONTACT 和全部 P3 子门通过 | A 路线 |
| P1-V 通过，但 P1-A、P2 或 P3 至少一项未通过 | B 路线，只保留通过门禁的能力 |
| P1-V 通过、P1-A 未通过 | 先进入 `P1_REFRAME_REVIEW` |
| 有效、可复验的 P1-V 仍失败 | C 路线 SafeTune-J |
| 模型、输入或证据无效 | 保持 `NOT_VERIFIED`，修复后复验 |
