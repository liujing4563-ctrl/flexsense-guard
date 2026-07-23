# 阶段任务清单

## 当前任务总览

| ID | 工作项 | 主责同学 | 前置条件 |
|---|---|---|---|
| GOV-01 | 批准项目范围并审查架构、路线和门禁框架 | 项目负责人同学 | 无 |
| GOV-02 | 建立五个工作包、唯一路径归属和目录骨架 | 项目负责人同学 | 无 |
| CON-01 | 迁移 Python/Schema v2 公共契约 | 项目负责人同学 | DTO 规范审查 |
| CON-02 | 迁移 MATLAB v2 输入链路 | Simulink 同学 | P1-01、CON-01 |
| PL-READY-01 | 建立项目负责人并行准备与审查组织 | 项目负责人同学 | PR #16 保持 Draft |
| SIM-PREP-01 | 审查 P1 数学模型并制定 MATLAB 实施计划 | Simulink 同学 | PR #16 候选规范 |
| P2-PREP-01 | 制定 P2 场景、标签和数据需求 | 深度学习通感算同学 | v2 DTO 和 P2 子门框架 |
| APP-PREP-01 | 制定 Mock 驱动的只读 App 原型方案 | 计算机软件同学 | v2 Schema 和 Mock |
| SIL-PREP-01 | 制定 C/SIL 工具链和跨语言映射方案 | 嵌入式 Linux 同学 | v2 Schema/Python 类型 |
| P1-01 | 共同确认理想齿轮、带符号力矩和 DTO 边界 | 项目负责人同学 | PR #16 审查 |
| P1-02 | 修正 MATLAB Plant 力矩反射和 PlantInputTrace | Simulink 同学 | P1-01 |
| P1-03 | 对齐 ObserverInput、状态转移和雅可比 | Simulink 同学 | P1-01、P1-02 |
| P1-04 | 增加无耗散能量一致性测试 | Simulink 同学 | P1-02 |
| P1-05 | 重建 P1-V/P1-A 多条件 runner | Simulink 同学 | P1-02 至 P1-04 |
| P2-01 | P2-VIB/P2-CONTACT 数据和分类 baseline | 深度学习通感算同学 | P1-V `PASS` |
| P3-01 | P3-DEGRADE/ACTION/RECOVERY 验证 | 项目负责人及相关同学 | P1-V `PASS` |
| APP-01 | 配置、报告和 Mock 契约审查 | 计算机软件同学 | v2 契约 `REVIEWED` |
| APP-02 | 完整 App 与自动报告 | 计算机软件同学 | P1-V `PASS` |
| SIL-01 | C 接口、构建、回放和资源测试计划 | 嵌入式 Linux 同学 | v2 契约 `REVIEWED` |
| SIL-02 | C/C++ SIL 主体实现 | 嵌入式 Linux 同学 | P1-V `PASS`，所依赖算法验证通过且接口获批 |

任务是否可启动及其当前状态只以
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md) 为准。本表不单独
维护状态，避免任务卡与阶段决定分叉。

## Issue 必需字段

每个可领取 Issue 必须包含：背景、目标、输入、输出、涉及文件、不涉及内容、验收
命令、负责同学、交接对象、依赖和风险。缺少任一项时不得进入主体实现。

并行准备任务的完整边界见
[`team_parallel_preparation_plan.md`](team_parallel_preparation_plan.md)，统一格式见
[`module_work_package_template.md`](module_work_package_template.md)。

## PL-READY-01：建立项目负责人并行准备与审查组织

- **背景**：PR #16 已具备审查条件，但尚无真人 Review；各模块需要可领取的准备任务。
- **目标**：维护状态、依赖、风险、Issue 和审查记录，组织模块交接，不实现主体算法。
- **主责**：项目负责人同学。
- **审查人**：Simulink 同学及至少一位非作者模块同学。
- **输入**：PR #16、权威状态文件、职责矩阵、风险登记和模块反馈。
- **输出**：Review 意见表、五个工作包、依赖图、Issue 清单、交付检查表和规范验证矩阵。
- **涉及文件**：`docs/**`、协作 Issue 和 PR Review。
- **禁止范围**：Plant、EKF、runner、分类器、Confidence、Mode、App、C/SIL 和
  Test Agent 主体；任何正式性能数据。
- **依赖**：PR #16 保持 Draft，所有状态与权威状态文件一致。
- **交接对象**：全部模块同学。
- **验收**：每项任务有唯一主责、输入生产者、输出消费者、依赖、禁止范围和可定位交付；
  主体算法路径改动为 0。
- **测试**：Markdown 链接检查、状态一致性检查、禁止路径检查。
- **风险**：准备工作被误写成实现完成；发现后阻止合并并纠正状态。
- **当前状态**：
  `Specification Status: DRAFT`；
  `Implementation Status: PARTIAL`；
  `Verification Status: NOT_VERIFIED`。

## SIM-PREP-01：审查 P1 数学模型并制定 MATLAB 实施计划

- **背景**：MATLAB Plant/EKF 仍为 `INVALID`，旧 P1 证据无效且 PR #16 数学内容待确认。
- **目标**：审查数学、力矩反射、输入边界和配置隔离，形成文件影响及测试计划。
- **主责**：Simulink 同学。
- **审查人**：项目负责人同学。
- **输入**：系统架构、术语表、接口规范、P1-V/P1-A 门禁、当前 MATLAB 文件。
- **输出**：数学审查表、MATLAB 文件影响清单、P1 测试计划、待确认问题和 PR Review。
- **涉及文件**：PR Review、`01_plant/simulink/README.md` 等现有准备说明。
- **禁止范围**：`01_plant/matlab/**`、`02_observer/**`、P1 runner、Q/R/P 和算法门限。
- **依赖**：PR #16 候选规范。
- **交接对象**：项目负责人同学；后续 P1-02 至 P1-05。
- **验收**：定义逐项使用 `APPROVE/NEEDS_REVISION/NOT_SURE`；DTO 有 MATLAB 映射建议；
  能量、雅可比、符号、seed 0、P1-V/P1-A 测试方案可执行。
- **测试**：本任务只审查方案；MATLAB execution 记录为 `NOT RUN`，不得伪造运行结果。
- **风险**：未独立推导就认可候选公式；存在不确定项时必须标 `NOT_SURE`。
- **当前状态**：
  `Specification Status: DRAFT`；
  `Implementation Status: MISSING`；
  `Verification Status: NOT_VERIFIED`。

## P2-PREP-01：制定 P2 场景、标签和数据需求

- **背景**：P2 正式开发被 P1-V 阻断，但场景和数据契约可提前准备。
- **目标**：分开定义 P2-VIB/P2-CONTACT 的场景、标签、信号需求、数据隔离和事件级评价。
- **主责**：深度学习通感算同学。
- **审查人**：项目负责人同学；Simulink 同学审查信号可提供性。
- **输入**：v2 DTO、P2 子门、指标定义、真值隔离规则和可提供场景信号。
- **输出**：场景表、标签规则、信号及候选特征表、事件级指标、数据依赖图和阻塞项。
- **涉及文件**：`04_classification/datasets/README.md`、
  `06_validation/fault_injection/README.md`、`06_validation/monte_carlo/README.md`。
- **禁止范围**：分类器训练、最终阈值、运行时真值特征、正式 P2 实验和性能结论。
- **依赖**：v2 DTO 与 P2 子门框架；正式开发仍依赖 P1-V `PASS`。
- **交接对象**：Simulink 同学、项目负责人同学和后续 P2 实现。
- **验收**：至少覆盖正常运动、柔性振动、摩擦变化和外部接触；误报漏报按事件统计；
  训练/验证/测试划分和混淆场景明确。
- **测试**：字段生产者检查、真值泄漏审查和数据划分复核；不运行 P2 算法。
- **风险**：提前选择最终特征或阈值导致评价污染；本任务只保留候选和规则。
- **当前状态**：
  `Specification Status: DRAFT`；
  `Implementation Status: MISSING`；
  `Verification Status: NOT_VERIFIED`。

## APP-PREP-01：制定 Mock 驱动的只读 App 原型方案

- **背景**：App 主体受 P1-V 阻断，但可用 Mock 审查页面和字段契约。
- **目标**：建立页面信息架构、DTO 到 UI 映射以及缺失、无效和版本不兼容状态规则。
- **主责**：计算机软件同学。
- **审查人**：项目负责人同学；数据生产模块审查字段语义。
- **输入**：v2 Schema、Mock、枚举、单位、失效规则和 Evidence Envelope。
- **输出**：页面结构、字段—组件映射、页面状态、Mock 说明和低保真原型说明。
- **涉及文件**：`07_app/**` 和 `06_validation/reports/README.md` 的现有准备说明。
- **禁止范围**：App 主体代码、真实算法接入、实时控制链、虚构准确率或性能提升。
- **依赖**：v2 Schema/Mock；真实集成仍依赖稳定契约和真实生产者。
- **交接对象**：项目负责人同学和后续 App 实现。
- **验收**：所有 Mock 页面显示 `MOCK DATA` 与 `NOT FOR ALGORITHM EVALUATION`；
  工程评分不显示为概率；状态和数据来源可区分。
- **测试**：Mock Schema 回放设计审查、字段覆盖和错误状态清单审查。
- **风险**：Mock 被误认为真实结果；标识不得被页面模式或截图裁掉。
- **当前状态**：
  `Specification Status: DRAFT`；
  `Implementation Status: MISSING`；
  `Verification Status: NOT_VERIFIED`。

## SIL-PREP-01：制定 C/SIL 工具链和跨语言映射方案

- **背景**：C 映射为 `MISSING`，且当前没有有效 MATLAB 参考，不允许移植旧 EKF。
- **目标**：形成工具链、DTO 到 C 映射、回放、一致性、资源和异常保护计划。
- **主责**：嵌入式 Linux 同学。
- **审查人**：项目负责人同学；Simulink 同学审查参考输入输出。
- **输入**：v2 Schema/Python 类型、单位、枚举、失效规则和未来 MATLAB 测试向量。
- **输出**：工具链清单、C 类型映射、SIL I/O、回放、一致性、runtime/memory 方案和阻塞项。
- **涉及文件**：`08_sil/**` 的现有 README 准备说明。
- **禁止范围**：任何 `.c`、`.h`、`.cpp`，旧 Plant/EKF 移植，稳定 ABI 声明和
  MATLAB 算法修改。
- **依赖**：v2 契约；正式迁移依赖获批接口和有效 MATLAB 参考。
- **交接对象**：项目负责人、Simulink 和计算机软件同学。
- **验收**：每个字段有 C 类型和有效性建议；版本/未知枚举显式失败；回放含版本、
  配置和校验；资源测量声明平台与边界。
- **测试**：映射审查和测试计划评审；C/SIL execution 记录为 `NOT RUN`。
- **风险**：过早固定 `PARTIAL` 契约形成错误 ABI；正式头文件必须等待接口批准。
- **当前状态**：
  `Specification Status: DRAFT`；
  `Implementation Status: MISSING`；
  `Verification Status: NOT_VERIFIED`。

## P1-01：共同确认模型和输入契约

- **背景**：旧 P1 的力矩所在侧和 Plant/Observer 输入不一致。
- **目标**：共同确认理想齿轮、负载侧弹性力矩、带符号负载力矩、能量和 v2 DTO。
- **输入**：系统架构、术语表、接口规范、历史 P1 证据。
- **输出**：共同审查记录；MATLAB 待迁移 DTO 和字段清单。
- **涉及文件**：`docs/02_architecture/**`、`docs/03_validation/**`。
- **不涉及内容**：不修改 Plant、EKF、runner 或 Q/R/P。
- **验收命令**：Markdown 链接检查、`python -m pytest -q`；MATLAB `NOT RUN`。
- **负责同学**：项目负责人同学主责，Simulink 同学共同确认。
- **依赖**：无。
- **风险**：未确认即改算法会再次形成无效证据。

## P1-02：修正 MATLAB Plant 输入和力矩反射

- **背景**：Plant 必须使用饱和后的实际施加力矩，并遵守负载/电机侧反射关系。
- **目标**：输出可追溯的 `motor_torque_applied_nm`，修正动力学并保留真值边界。
- **输入**：P1-01 共同确认的模型、Plant 参数和执行器约束。
- **输出**：Plant 源码、参数说明、模块测试和逐样本实际施加力矩。
- **涉及文件**：`01_plant/**`。
- **不涉及内容**：不修改公共门禁、分类器、App 或 C/SIL。
- **验收命令**：由 Simulink 同学登记实际 MATLAB 测试命令和结果。
- **负责同学**：Simulink 同学。
- **依赖**：P1-01。
- **风险**：齿轮反射或符号错误会破坏能量一致性。

## P1-03：对齐 ObserverInput

- **背景**：旧 Observer 使用原始指令，不能代表 Plant 实际输入。
- **目标**：Observer 只消费 `ObserverInput.motor_torque_feedback_nm`，同步状态转移和雅可比。
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
- **输入**：共同确认的方程、参数和数值积分设置。
- **输出**：独立测试、容差依据、实际运行日志和失败诊断。
- **涉及文件**：`01_plant/tests/**`。
- **不涉及内容**：不以调参掩盖方程错误。
- **验收命令**：由 Simulink 同学登记 MATLAB 测试命令和结果。
- **负责同学**：Simulink 同学。
- **依赖**：P1-02。
- **风险**：容差过宽会让物理错误通过，必须记录步长与积分方法。

## P1-05：重建 P1-V/P1-A 多条件 runner

- **背景**：旧实验只有单负载、单场景、单 seed，且调参与评价未隔离。
- **目标**：运行 light/medium/heavy、seed 0-9，先判断 P1-V，再公平评价 P1-A。
- **输入**：P1-02 至 P1-04、实验前批准的门禁、调试/评价划分和版本化配置。
- **输出**：runner、配置、原始证据索引、机器可读汇总、失败案例和决定建议。
- **涉及文件**：`scripts/run_p1_feasibility_probe.m`、`scripts/run_probe.m`、
  `results/p1/**`。
- **不涉及内容**：不启动 P2/P3，不删除失败，不用评价真值挑参数。
- **验收命令**：实际 MATLAB P1 命令；Schema 校验；汇总完整性检查。
- **负责同学**：Simulink 同学执行，项目负责人审查决定。
- **依赖**：P1-02、P1-03、P1-04。
- **风险**：缺任一负载、seed、速度门限、环境或原始证据时只能判 `NOT_VERIFIED`；
  P1-A 失败不得直接触发 C 路线。

## 阶段声明

阶段状态不在本文件重复维护，统一见
[`current_status_and_next_steps.md`](../current_status_and_next_steps.md)。任何 Issue 都
不得绕过权威状态启动被阻断的主体工作。
