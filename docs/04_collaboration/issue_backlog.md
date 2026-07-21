# 阶段任务清单

## 当前任务总览

| ID | 工作项 | 主责同学 | 前置条件 | 当前状态 |
|---|---|---|---|---|
| GOV-01 | 冻结项目范围、架构、路线、门禁和决策规则 | 项目负责人同学 | 无 | `COMPLETED` |
| GOV-02 | 建立五个工作包、唯一路径归属和缺失目录骨架 | 项目负责人同学 | 无 | `COMPLETED` |
| CON-01 | 迁移 JSON/Python 三类力矩公共输入契约 | 项目负责人同学 | 语义冻结 | `IMPLEMENTED`，待审查 |
| CON-02 | 迁移 MATLAB 三类力矩信号链路 | Simulink 同学 | P1-01 | `READY` |
| P1-RECOVERY-01 | 修复双惯量模型和 Plant/Observer 力矩输入一致性 | Simulink 同学 | 模型语义已冻结 | `READY` |
| P1-01 | 冻结力矩所在侧、齿轮方向和输入契约 | 项目负责人同学 | 无 | `COMPLETED`，待 Simulink 实现确认 |
| P1-02 | 修正 MATLAB Plant 力矩反射和实际施加力矩 | Simulink 同学 | P1-01 | `READY` |
| P1-03 | 对齐 Observer 测量力矩输入和状态转移 | Simulink 同学 | P1-01、P1-02 | `BLOCKED` |
| P1-04 | 增加无耗散能量一致性测试 | Simulink 同学 | P1-02 | `BLOCKED` |
| P1-05 | 重建三负载、多 seed、公平评价 P1 runner | Simulink 同学 | P1-02 至 P1-04 | `BLOCKED` |
| P2-01 | 受控场景、无泄漏数据划分和分类 baseline | 深度学习通感算同学 | P1 `PASS` | `BLOCKED` |
| P3-01 | 可信失效与安全降级验证 | 项目负责人及相关同学 | P1 `PASS` | `BLOCKED` |
| APP-01 | 配置、报告和 Mock 界面联调 | 计算机软件同学 | 公共契约审查 | `PLANNED` |
| APP-02 | 完整 App 与自动报告 | 计算机软件同学 | P1 `PASS` | `BLOCKED` |
| SIL-01 | C 接口、构建、回放和资源测试计划 | 嵌入式 Linux 同学 | 公共契约审查 | `PLANNED` |
| SIL-02 | C/C++ SIL 主体实现 | 嵌入式 Linux 同学 | P1 与主算法冻结 | `BLOCKED` |

## Issue 必需字段

每个可领取 Issue 必须包含：背景、目标、输入、输出、涉及文件、不涉及内容、验收
命令、负责同学、交接对象、依赖和风险。缺少任一项时不得进入主体实现。

## P1-RECOVERY-01：修复双惯量模型和 Plant/Observer 力矩输入一致性

- **背景**：历史 P1 使用旧齿轮力矩模型，Plant 消费饱和后的实际输入，而
  Observer 消费饱和前指令；旧 runner 还存在单负载、单场景、单 seed 和用评价
  真值选择 Q 的问题，因此历史证据无效或不足。
- **目标**：先修复 MATLAB Plant、EKF、雅可比和三类力矩输入链，建立有效 P1
  复验的物理和接口基础；本 Issue 不负责证明 P1 已通过。
- **负责人**：Simulink 同学主责；项目负责人同学审查。
- **输入文档**：`docs/04_collaboration/p1_model_input_handoff.md`、
  `docs/02_architecture/system_architecture.md`、
  `docs/02_architecture/interface_spec.md`、
  `docs/03_validation/experiment_protocol.md`。
- **修改范围**：`01_plant/matlab/**`、`01_plant/tests/**`、`02_observer/**` 及为
  输入一致性所必需的 MATLAB 测试；三负载 runner 作为后续子任务处理。
- **禁止范围**：不得调 Q/R/P 追求通过，不得降低 P1 门禁，不得修改历史结果，
  不得启动 P2/P3、Confidence、Classification、App、C/SIL 或 Test Agent。
- **输出**：修正后的 Plant、EKF 和雅可比；三类力矩字段；能量、输入一致性和
  seed 复现测试；MATLAB 日志、文件清单、风险说明和 Draft PR。
- **验收标准**：电机侧使用 `tau_s_load_nm / N`；Plant 使用并输出
  `motor_torque_applied_nm`；Observer 只使用 `motor_torque_measured_nm`；无真值
  泄漏；参数结构分离；雅可比一致；`seed=0` 可复现；无 NaN/Inf；能量测试通过。
- **测试要求**：实际登记 MATLAB 命令和结果；未运行项写 `NOT RUN`；在修复前后
  分别执行输入一致性和能量检查，不以 Python 测试替代 MATLAB 复验。
- **依赖**：冻结的模型和字段语义；项目负责人对交接单的审查。
- **风险**：错误的齿轮方向、符号、噪声注入位置或静默兼容旧字段会继续产生无效
  P1 证据。
- **建议分支**：`fix/p1-model-input-consistency`。
- **建议 PR 标题**：`fix: align P1 dual-inertia model and torque input semantics`。

## P1-01：冻结模型和输入契约

- **背景**：旧 P1 的力矩所在侧和 Plant/Observer 输入不一致。
- **目标**：共同确认负载侧弹性力矩、齿轮方向、符号、能量和三类电机力矩。
- **输入**：系统架构、术语表、接口规范、历史 P1 证据。
- **输出**：共同审查记录；MATLAB 待迁移字段清单。
- **涉及文件**：`docs/02_architecture/**`、`docs/03_validation/**`。
- **不涉及内容**：不修改 Plant、EKF、runner 或 Q/R/P。
- **验收命令**：Markdown 链接检查、`python -m pytest -q`；MATLAB `NOT RUN`。
- **负责同学**：项目负责人同学主责，Simulink 同学共同确认。
- **依赖**：无。
- **风险**：未确认即改算法会再次形成无效证据。

## P1-02：修正 MATLAB Plant 输入和力矩反射

- **背景**：Plant 必须使用饱和后的实际施加力矩，并遵守负载/电机侧反射关系。
- **目标**：输出可追溯的 `motor_torque_applied_nm`，修正动力学并保留真值边界。
- **输入**：P1-01 冻结模型、Plant 参数和执行器约束。
- **输出**：Plant 源码、参数说明、模块测试和逐样本实际施加力矩。
- **涉及文件**：`01_plant/**`。
- **不涉及内容**：不修改公共门禁、分类器、App 或 C/SIL。
- **验收命令**：由 Simulink 同学登记实际 MATLAB 测试命令和结果。
- **负责同学**：Simulink 同学。
- **依赖**：P1-01。
- **风险**：齿轮反射或符号错误会破坏能量一致性。

## P1-03：对齐 Observer 测量力矩输入

- **背景**：旧 Observer 使用原始指令，不能代表 Plant 实际输入。
- **目标**：Observer 只消费 `motor_torque_measured_nm`，同步状态转移和雅可比。
- **输入**：P1-01 契约、P1-02 Plant 输出和独立 Observer 名义参数。
- **输出**：EKF 源码、维度检查、输入追溯和模块测试。
- **涉及文件**：`02_observer/**`。
- **不涉及内容**：不使用负载真值，不在最终评价集调 Q/R/P。
- **验收命令**：由 Simulink 同学登记 MATLAB Observer 测试命令和结果。
- **负责同学**：Simulink 同学。
- **依赖**：P1-01、P1-02。
- **风险**：兼容旧字段会掩盖输入不一致，应显式失败而非静默回退。

## P1-04：建立能量一致性测试

- **背景**：单看轨迹无法证明齿轮映射和符号正确。
- **目标**：无输入、无外扰、无摩擦、无阻尼、`eta=1` 时验证机械能守恒误差。
- **输入**：冻结方程、参数和数值积分设置。
- **输出**：独立测试、容差依据、实际运行日志和失败诊断。
- **涉及文件**：`01_plant/tests/**`。
- **不涉及内容**：不以调参掩盖方程错误。
- **验收命令**：由 Simulink 同学登记 MATLAB 测试命令和结果。
- **负责同学**：Simulink 同学。
- **依赖**：P1-02。
- **风险**：容差过宽会让物理错误通过，必须记录步长与积分方法。

## P1-05：重建 P1 多条件 runner

- **背景**：旧实验只有单负载、单场景、单 seed，且调参与评价未隔离。
- **目标**：运行 light/medium/heavy、seed 0-9，并公平比较 baseline 与 EKF。
- **输入**：P1-02 至 P1-04、冻结门禁、调试/评价划分和版本化配置。
- **输出**：runner、配置、原始证据索引、机器可读汇总、失败案例和决定建议。
- **涉及文件**：`scripts/run_p1_feasibility_probe.m`、`scripts/run_probe.m`、
  `results/p1/**`。
- **不涉及内容**：不启动 P2/P3，不删除失败，不用评价真值挑参数。
- **验收命令**：实际 MATLAB P1 命令；Schema 校验；汇总完整性检查。
- **负责同学**：Simulink 同学执行，项目负责人审查决定。
- **依赖**：P1-02、P1-03、P1-04。
- **风险**：缺任一负载、seed、环境或原始证据时只能判 `NOT_VERIFIED`。

## 其他同学的准备任务

| 同学 | 当前可做 | 交付路径 | 不得提前做 |
|---|---|---|---|
| 深度学习通感算同学 | 审查分类枚举；设计数据划分、故障矩阵和 Agent I/O | `04_classification/**`、`09_test_agent/**` 的设计说明 | 分类训练、正式 P2/P3 结果和 Agent 主体 |
| 计算机软件同学 | 验证 Mock；设计配置、结果索引、错误状态和报告字段 | `configs/**`、`07_app/**`、`06_validation/reports/**` 的设计说明 | 完整 App、把 Mock 当结果 |
| 嵌入式 Linux 同学 | 设计 C 类型、回放、构建、异常和资源测试清单 | `08_sil/**` 的设计说明 | Observer 移植、SIL 性能结论 |

## 阶段声明

历史 P1 执行结果为 `FAIL`，历史证据为 `INVALID / INSUFFICIENT`，当前 P1
可行性结论为 `NOT_VERIFIED`。任何 Issue 都不得绕过该状态启动被阻断的主体工作。
