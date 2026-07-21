# 历史 Issue 清单

> 本文件仅用于历史追溯。当前任务以 [`docs/04_collaboration/issue_backlog.md`](../docs/04_collaboration/issue_backlog.md) 为准。

## P0 — Probe 阶段（必须完成）

### P0-01: 建立双惯量柔性关节 Plant V1

- **标签**: `P0-probe`, `model`
- **描述**: 实现参数化双惯量柔性关节动力学模型，包含：
  - J_m * θ̈_m = τ_m − τ_s − τ_fm
  - J_l * θ̈_l = τ_s − τ_ext − τ_fl
  - τ_s = K_s * (θm/N − θl) + D_s * (ωm/N − ωl)
  - 摩擦模型（库仑 + 黏性）
  - 力矩饱和
  - 测量时延
- **验收标准**:
  - `flex_joint_dynamics.m` 输入/输出/单位完善
  - `flex_joint_default_params.m` 定义所有 Plant 参数
  - `simulate_flex_joint.m` 能生成完整仿真轨迹
  - `test_plant_smoke.m` 通过
  - 三个载荷参数 JSON 文件创建

### P0-02: 完成线性化可观测性检查与增广 EKF 基线

- **标签**: `P0-probe`, `observer`
- **描述**: 实现增广 EKF 观测器，状态向量 [θm, ωm, θl, ωl, τext]ᵀ
  - Plant 参数 ≠ Observer 名义参数
  - 测量 y = [θm, ωm]ᵀ（禁止使用负载侧真值）
  - 线性化系统可观测性检查
- **验收标准**:
  - `augmented_ekf_init.m` 和 `augmented_ekf_step.m` 实现
  - `observer_default_config.m` 定义 Observer 名义参数
  - `test_observer_smoke.m` 通过
  - 明确标注参数失配

### P0-03: 构建正常加速、柔性振动和外部冲击场景

- **标签**: `P0-probe`, `test`
- **描述**: 在 `generate_probe_scenarios.m` 中生成三个标准测试场景
  - 正常加减速（正弦轨迹）
  - 柔性振动（接近共振频率）
  - 外部冲击（脉冲力矩注入）
- **验收标准**:
  - 三个场景可重复生成
  - 每个场景有明确的时间参数
  - 场景配置符合 `scenario_config.schema.json`

### P0-04: 建立初步可信评分与信号健康检测

- **标签**: `P0-probe`, `confidence`
- **描述**: 实现：
  - 基于创新残差的置信度评分
  - 信号健康检测（电流卡死、编码器丢包、参数失配）
- **验收标准**:
  - `confidence_score.m` 输出 [0, 1] 范围
  - `signal_health_check.m` 输出各信号健康标志
  - 故障注入后评分显著下降

### P0-05: 完成 72 小时探针一键脚本和三组结果

- **标签**: `P0-probe`, `integration`
- **描述**: 实现 `run_probe.m`，一键执行三个探针：
  - Probe 1: 三条位置曲线
  - Probe 2: 三个场景的估计外扰矩 + 创新残差
  - Probe 3: 三种故障注入的可信评分变化
- **验收标准**:
  - `run_probe.m` 无错误运行完成
  - 产生可视化输出
  - 结果记录到 `results/generated/`

---

## P1 — 后续迭代

### P1-01: 建立传统扰动观测器基线

- **标签**: `observer`, `baseline`
- **描述**: 实现简单的扰动观测器（DOB）作为 EKF 对比基线

### P1-02: 建立规则式振动—接触分类器

- **标签**: `classifier`
- **描述**: 基于特征的规则分类器，输出正常/振动/接触三分类

### P1-03: 建立事件触发低幅校准与更新门控

- **标签**: `trigger`, `confidence`
- **描述**: 可信度低时触发校准信号注入；更新门控接受/保持/回退

### P1-04: 建立 MATLAB/C SIL 一致性测试

- **标签**: `sil`
- **描述**: 相同输入下 MATLAB 和 C 实现输出对比测试

### P1-05: 建立测试 Agent 确定性工具链

- **标签**: `test`, `agent`
- **描述**: 批量运行测试用例、Schema 校验、指标收集、报告生成

### P1-06: 建立虚拟传感器 App 原型

- **标签**: `app`
- **描述**: 基于 Python 或网页的传感器看板原型

---

## 标签说明

| 标签 | 含义 |
|------|------|
| P0-probe | 72 小时探针必须完成 |
| model | Plant 模型相关 |
| observer | 观测器相关 |
| test | 测试相关 |
| confidence | 可信评分相关 |
| integration | 集成相关 |
| baseline | 基线实现 |
| classifier | 分类器相关 |
| trigger | 事件触发相关 |
| sil | C/C++ SIL 相关 |
| agent | 测试 Agent 相关 |
| app | 应用层相关 |
