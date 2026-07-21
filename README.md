# FlexSense-Guard

**无负载侧传感器的机器人柔性关节可信虚拟力觉与安全控制仿真系统**

> 基于双惯量增广状态观测、事件触发校准与振动—接触可信辨识

## 项目定位

FlexSense-Guard 是一个纯算法与数字化仿真项目。项目只研究一个主导柔性关节，
目标是在不使用负载侧传感器的条件下，仅根据电机侧位置、速度、电流和力矩，
估计负载侧运动状态与外部关节扰动力矩，评价估计是否可信，并依据正常、柔性
振动、外部接触和低可信状态切换控制模式。

项目当前仍处于可行性验证阶段，不是完整产品，也不包含硬件验证。

## 当前核心阻塞

仓库保留一份旧 P1 MATLAB 失败记录，但该实验存在模型定义、输入一致性和证据
覆盖不足问题。历史执行结果与当前技术结论必须分开：

| 项目 | 当前状态 |
|---|---|
| 历史 P1 执行结果 | `FAIL` |
| 历史证据有效性 | `INVALID / INSUFFICIENT` |
| 当前 P1 可行性结论 | `NOT_VERIFIED` |
| P2：状态可分辨性 | `BLOCKED`，未运行 |
| P3：可信失效识别 | `BLOCKED`，未运行 |
| MATLAB/Octave 当前复验 | `NOT RUN` |
| C/SIL、App、测试 Agent | 尚未进入主体开发 |

旧实验不能用于认定负载侧状态不可估计或 EKF 路线不可行。当前仍不能宣称外部
接触识别、可信安全闭环、C/SIL、App 或测试 Agent 已完成。

当前完成情况、唯一下一动作和五位同学的立即任务见
[当前完成情况与下一步](docs/current_status_and_next_steps.md)。

## 技术主线

```text
场景与轨迹
→ 双惯量柔性关节 Plant
→ 电机侧测量
→ 信号健康检测
→ 增广状态观测器
→ 负载侧状态与外部扰动力矩估计
→ 工程可信评分
→ 状态分类
→ 模式管理
→ 控制策略
→ 自动验证、验收与回退
```

仿真真值只能进入评价模块，禁止进入 Observer、Confidence、Classification、
Mode Manager 或 Control。

## P1 模型与输入冻结

- 传动比方向统一为理想刚性关系 `theta_l = theta_m / N`；
- `tau_s_load_nm` 表示负载侧弹性力矩；理想效率下反射到电机侧的力矩为
  `tau_s_load_nm / N`；
- 必须区分 `torque_command_nm`、`motor_torque_applied_nm` 和
  `motor_torque_measured_nm`；
- Plant 使用实际施加力矩，Observer 使用测量力矩，禁止直接使用原始力矩指令；
- 文档语义、JSON Schema 和 Python 输入类型已完成三类力矩迁移；MATLAB 信号
  结构仍由 Simulink 同学迁移，端到端输入链路状态为 `NOT_VERIFIED`。

## 公共状态

分类状态：

```text
NORMAL
FLEXIBLE_VIBRATION
EXTERNAL_CONTACT
LOW_CONFIDENCE
```

运行模式：

```text
NORMAL_TRACKING
VIBRATION_SUPPRESSION
SAFE_SLOWDOWN
LOW_CONFIDENCE_DEGRADED
```

`confidence_score` 和 `contact_score` 都是工程评分，不是概率。禁止字段
`contact_probability`。外扰输出统一为 `estimated_external_torque_nm`；没有
Jacobian 或等效力臂时，不称为末端力。

## 三级技术路线

- A 路线：P1、P2、P3 均基于有效证据通过，推进可信虚拟力觉、接触辨识、校准、安全控制、
  SIL、App 和测试 Agent。
- B 路线：P1 基于有效证据通过但 P2 失败，降级为可信状态估计与主动抑振，不再主张可靠接触
  识别。
- C 路线：模型、输入和实验设计修复后，P1 仍基于有效证据失败，降级为 SafeTune-J 事件触发可信自整定与自动验收
  系统。

## 项目负责人工作包范围

项目负责人基础工作包负责：

- 项目章程、范围和系统架构；
- 公共接口和跨语言枚举；
- P1/P2/P3 门禁、实验协议和风险；
- 五位同学职责和交接规则；
- Git、PR、Issue 和 Codex 使用边界；
- 术语、跨语言契约、验收矩阵、指标、证据和决策日志；
- Python 包安装、公共类型、Schema、Mock 样例和基础 CI；
- 缺失模块目录骨架及路径责任规划。

本工作包不修改双惯量 Plant、MATLAB EKF、Simulink `.slx`、分类算法、可信评分
主体、App、C/SIL 或测试 Agent。

## Python 基础验证

支持 Python 3.11 及以上版本。在仓库根目录执行：

```bash
python -m pip install -e .
python -m pytest -q
```

项目安装会同时安装基础契约测试所需的 pytest 和 jsonschema，不需要设置
`PYTHONPATH`。

## MATLAB 说明

MATLAB 主实现和 P1 复验由 Simulink 同学负责。运行前切换到仓库根目录：

```matlab
setup_project
run_probe
```

当前环境或当前分支未实际运行 MATLAB 时，必须记录 `NOT RUN`，不能用 Python
结果替代 MATLAB 复验。

## 目录说明

```text
FlexSense-Guard/
├── docs/                    # 当前规范来源
├── 00_docs/                 # 早期文档，保留追溯
├── 01_plant/                # Plant 和 MATLAB/Simulink 工作区
├── 02_observer/             # Observer 与 baseline
├── 03_confidence_trigger/   # 可信评分和事件触发
├── 04_classification/       # 特征和分类
├── 05_control/              # 模式管理和控制
├── 06_validation/           # 指标与验证
├── 07_app/                  # 软件同学工作包骨架
├── 08_sil/                  # 嵌入式 Linux 同学工作包骨架
├── 09_test_agent/           # 测试 Agent 工作包
├── configs/                 # 配置与 MOCK 接口样例
├── results/                 # 阶段证据索引与报告
├── common/schemas/          # JSON Schema
├── python/                  # Python 公共契约与基础测试
├── scripts/                 # 运行入口
└── .github/                 # CI 与协作模板
```

目录存在不代表功能已完成。实际能力以可运行实现、测试和报告为准。

## 同学职责

| 角色 | 主要责任 |
|---|---|
| 项目负责人同学 | 章程、架构、接口、门禁、风险、集成和答辩 |
| Simulink 同学 | Plant、MATLAB EKF、MIL、`.slx` 和 P1 复验 |
| 深度学习通感算同学 | 数据、特征、分类、故障注入和测试 Agent |
| 计算机软件同学 | 配置、App、结果管理、自动报告和演示 |
| 嵌入式 Linux 同学 | C/C++、CMake、CTest、SIL 和一致性验证 |

项目负责人同学可以建立最小参考实现用于独立验证，但不长期代替模块负责同学
完成主体实现。Codex 生成代码按所在模块归属。

## 文档入口

- [当前完成情况与下一步](docs/current_status_and_next_steps.md)
- [项目章程](docs/01_project/project_charter.md)
- [项目范围与非目标](docs/01_project/scope_and_non_goals.md)
- [风险登记册](docs/01_project/risk_register.md)
- [系统架构](docs/02_architecture/system_architecture.md)
- [公共接口规范](docs/02_architecture/interface_spec.md)
- [术语与符号表](docs/02_architecture/glossary_and_symbols.md)
- [跨语言契约矩阵](docs/02_architecture/cross_language_contract.md)
- [可信评分设计规范](docs/02_architecture/confidence_design_spec.md)
- [事件触发校准规范](docs/02_architecture/event_trigger_calibration_spec.md)
- [模式管理规范](docs/02_architecture/mode_manager_spec.md)
- [72 小时技术探针](docs/03_validation/feasibility_probe_72h.md)
- [实验协议](docs/03_validation/experiment_protocol.md)
- [阶段验收矩阵](docs/03_validation/acceptance_matrix.md)
- [指标定义](docs/03_validation/metric_definitions.md)
- [证据管理规范](docs/03_validation/evidence_management.md)
- [技术探针执行记录](docs/03_validation/probe_results.md)
- [同学职责与交接规则](docs/04_collaboration/team_responsibilities.md)
- [阶段任务清单](docs/04_collaboration/issue_backlog.md)
- [Git 协作流程](docs/04_collaboration/git_workflow.md)
- [决策日志](docs/decision_log.md)

## 不作出的声明

- 不声称已经完成真实硬件部署或验证；
- 不声称达到工业安全认证；
- 不声称未经实验支持的碰撞检测率、零误报或实时性能；
- 不把占位代码、空目录、未运行测试或文档计划视为已完成能力；
- 不公开专利、比赛敏感材料、个人数据或无权公开的第三方内容。

许可和比赛使用边界见 [许可与使用声明](LICENSE_NOTICE.md)。
