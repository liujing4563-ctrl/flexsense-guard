# 当前完成情况与下一步

## 状态快照

快照日期：2026-07-21。项目负责人基础工作包已通过 PR #14 合并到 `main`。本轮
在独立分支补齐控制、可信机制和验证治理规范；P1 Simulink 交接由独立 Draft PR
#15 管理，不在本分支修改 Plant、EKF 或 runner。

| 工作部分 | 当前状态 | 证据或说明 |
|---|---|---|
| 项目范围、路线和职责 | `FROZEN` | 章程、A/B/C 路线、五个工作包和唯一路径归属已写明 |
| 数学模型语义 | `FROZEN` | 负载侧弹性力矩、齿轮方向、电机侧反射和能量检查已定义 |
| 术语、符号和公共字段语义 | `FROZEN` | 字段、单位、枚举和失效行为已定义 |
| JSON/Python 公共契约 | `IMPLEMENTED` | 三类力矩字段已进入输入 Schema 和 Python 类型；旧字段已禁止 |
| 跨语言公共契约 | `PARTIAL` | MATLAB 为 `NOT FROZEN`，C 和 App 映射仍为 `MISSING` |
| MATLAB 输入契约迁移 | `PENDING` | 由 Simulink 同学迁移 Plant 输出、Observer 输入和 runner |
| 端到端输入链路 | `NOT_VERIFIED` | MATLAB 生产者和消费者尚未完成共同回放 |
| P1/P2/P3 与集成门禁 | `FROZEN` | 验收矩阵、实验协议、指标和证据规则已建立 |
| 可信评分设计 | `SPECIFIED`，未实现 | 输入、输出、失效、恢复和优先级已规定；权重和阈值待实验 |
| 事件触发设计 | `SPECIFIED`，未实现 | `UPDATE/HOLD/ROLLBACK`、备份和禁止触发条件已规定 |
| 模式管理设计 | `SPECIFIED`，未实现 | 四模式、优先级、冲突处理和恢复原则已规定 |
| 模块目录规划 | `COMPLETED` | `configs`、`07_app`、`08_sil`、验证、Agent 和结果骨架已创建 |
| Mock 接口样例 | `AVAILABLE` | 六个样例均标记 `data_source: MOCK` 且禁止算法评价 |
| Plant / EKF / P1 runner | `UNCHANGED` | 本工作包没有修改 Simulink 同学的主体实现 |
| Python 自动检查 | `PASSED` | 本地 `python3 -m pytest -q`：17 passed；CI 结果以本分支实际运行为准 |
| MATLAB / C/SIL / App 检查 | `NOT RUN` | 未进入对应主体实现或当前环境未复验 |

## 阶段状态

```text
Historical P1 execution result: FAIL
Evidence validity: INVALID / INSUFFICIENT
Current P1 feasibility decision: NOT_VERIFIED
P2: BLOCKED
P3: BLOCKED
```

旧 P1 只能作为历史失败记录，不能用于认定负载侧状态不可估计或 EKF 路线失败。

## 下一项目动作

项目负责人先完成本规范 PR 的非作者审查和一致性检查。随后由 Simulink 同学根据
独立 P1 交接任务迁移 MATLAB Plant/Observer 输入链路；模型和输入一致性通过后，
再重建三负载、10 seed P1 runner。项目负责人只审查契约、证据和阶段决定，不
代写主体实现。

其他同学可以完成接口审查和交付计划，但在 P1 形成有效 `PASS` 证据前，不启动
P2/P3、完整 App、C/SIL 或 Test Agent 主体开发。

## 每位同学现在要做什么

| 同学 | 主责路径 | 立即行动 | 本阶段交付 | 当前禁止事项 |
|---|---|---|---|---|
| 项目负责人同学 | `docs/**`、`common/schemas/**`、`python/**`、`03_confidence_trigger/**`、`05_control/**`、`06_validation/metrics/**` | 组织模型和契约审查；维护 Issue、决策、门禁和证据索引；审查模块 PR | 冻结规范、公共契约、验收矩阵、Mock 与交接记录 | 不代写 Plant、EKF、分类器、App 或 C/SIL 主体 |
| Simulink 同学 | `01_plant/**`、`02_observer/**`、P1 runner、`results/p1/**` | 确认模型；迁移实际/测量力矩；增加能量检查；重建三负载十 seed P1 | MATLAB 源码、配置、日志、曲线、汇总、失败案例和决定建议 | 不使用原始指令代替测量力矩；不降低门限或使用测试真值调参 |
| 深度学习通感算同学 | `04_classification/**`、故障/批量验证、`09_test_agent/**`、`results/p2/**` | 审查分类字段；设计无泄漏数据划分、故障矩阵和 P2 任务卡 | 数据与评价方案、特征/规则计划、Agent 输入输出草案 | P1 通过前不训练分类器、不生成正式 P2/P3 结果、不开发 Agent 主体 |
| 计算机软件同学 | `configs/**`、`06_validation/reports/**`、`07_app/**`、`results/reports/**` | 校验 Mock 与 Schema；设计配置、结果索引、错误状态和报告映射 | App 信息架构、字段映射和报告计划 | P1 通过前不开发完整 App，不把 Mock 当实验数据 |
| 嵌入式 Linux 同学 | `08_sil/**` | 审查类型、单位、范围和异常处理；设计 C 接口、回放和资源验收 | SIL 接口、构建、测试和基准计划 | 算法冻结前不移植 Observer，不自行改变公共字段 |

完整路径归属见
[`team_responsibilities.md`](04_collaboration/team_responsibilities.md)。

## P1 交接清单

项目负责人向 Simulink 同学交付：

1. [`system_architecture.md`](02_architecture/system_architecture.md) 中的模型与能量检查；
2. [`glossary_and_symbols.md`](02_architecture/glossary_and_symbols.md) 中的符号和所在侧；
3. [`interface_spec.md`](02_architecture/interface_spec.md) 中的三类力矩字段；
4. [`cross_language_contract.md`](02_architecture/cross_language_contract.md) 中的 MATLAB 待迁移项；
5. [`acceptance_matrix.md`](03_validation/acceptance_matrix.md) 中的 P1 强制门禁；
6. [`experiment_protocol.md`](03_validation/experiment_protocol.md) 中的公平比较规则；
7. [`evidence_management.md`](03_validation/evidence_management.md) 中的结果保存要求；
8. [`probe_results.md`](03_validation/probe_results.md) 中保留的旧 P1 失败记录。

Simulink 同学交回：

1. 模型与输入契约共同确认记录；
2. MATLAB 版本、Git 提交和工作区状态；
3. light、medium、heavy 与 seed 0 到 9 的版本化配置；
4. baseline 与 EKF 的位置、速度误差及强制有效性指标；
5. 能量检查、实际施加/测量力矩逐样本追溯；
6. 原始证据索引、机器可读汇总、失败案例和实际运行命令；
7. 基于冻结门禁的 `PASS`、`FAIL` 或 `NOT_VERIFIED` 建议。

## 决策路径

```text
P1 PASS -> 进入 P2，并继续验证 A/B 路线
证据 INVALID / INSUFFICIENT -> 保持 NOT_VERIFIED，修复后复验
P1 基于有效证据 FAIL -> 由项目负责人组织 C 路线决策
```

## 负责人工作包完成条件

- 权威文档、责任路径、阶段门、指标、证据和决策记录一致；
- JSON Schema、Python 类型和 Mock 样例通过自动一致性测试；
- MATLAB/C/App 尚未迁移项明确标为 `PENDING` 或 `BLOCKED`；
- Plant、EKF、分类器、App 和 C/SIL 主体没有被本工作包接管；
- 历史 P1 `FAIL` 与当前 `NOT_VERIFIED` 始终分层；
- 至少一位其他同学完成审查后，才进入提交和合并流程。
