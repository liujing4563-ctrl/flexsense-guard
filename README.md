# FlexSense-Guard


**Trusted virtual force sensing and safety control simulation for flexible robot joints without load-side sensors.**

**无负载侧传感器的机器人柔性关节可信虚拟力觉与安全控制仿真系统**

> 基于双惯量增广状态观测、事件触发校准与振动—接触可信辨识

---

## 1. 项目简介

FlexSense-Guard 是一个纯算法仿真项目，旨在**不依赖负载侧传感器**的条件下，通过电机侧可测信号（位置、速度、电流）实现对柔性机器人关节负载侧状态和外部扰动力矩的高保真估计，并对估计结果进行实时可信评分，驱动场景自适应的安全控制模式切换。

本项目参加机器人创新设计大赛赛道七，按**纯算法仿真和机器人核心零部件数字化设计作品**推进。

---

## 2. 工业问题

协作机器人、服务机器人和外骨骼机器人的柔性关节面临三个核心挑战：

1. **传感器缺失**：负载侧力矩/位置传感器增加成本、布线和维护负担，工业界亟需"虚拟力觉"方案
2. **振动干扰**：关节柔性引入弹性振荡，其动力学特征与外部接触高度相似，容易误判
3. **模型退化**：纯模型估计在参数漂移、信号异常时不可靠，缺乏工程可部署的"健康-可信"监测机制

---

## 3. 核心闭环

```
轨迹/场景 → Plant → 电机侧测量 → 信号健康检测 → EKF观测器 → 
可信评分 → 振动-接触分类 → 模式管理 → 控制与验证 → 事件触发校准（闭环）
```

详细架构见 `00_docs/system_architecture.md`。

---

## 4. 项目边界

### 包括
- 参数化双惯量柔性关节数字样机
- 电机侧可测信号驱动的增广 EKF 状态估计
- 基于创新残差和信号健康的可信评分
- 事件触发低幅校准与更新门控
- 正常/振动/接触三分类辨识
- 四种控制模式（正常跟踪/振动抑制/安全减速/降级）
- MATLAB/Simulink MIL + C/C++ SIL + Python 验证
- 智能测试 Agent 与自动报告

### 明确不做
- ❌ 不使用负载侧传感器信号作为观测器输入
- ❌ 不实现深度强化学习（最多轻量三分类）
- ❌ 不接入 ROS 2、Gazebo、Isaac Sim
- ❌ 不涉及多机器人分布式控制或 Kuramoto 同步
- ❌ 不做工业安全认证
- ❌ 不虚构硬件实测数据或未经验证的性能指标

完整列表见 `00_docs/scope_and_non_goals.md`。

---

## 5. 目录结构

```
flexsense-guard/
├── .github/                    # GitHub 协作模板与 CI
│   ├── ISSUE_TEMPLATE/         # Issue 模板（feature/bug/experiment）
│   ├── workflows/              # GitHub Actions
│   └── pull_request_template.md
├── 00_docs/                    # 项目文档
│   ├── project_charter.md      # 项目章程
│   ├── system_architecture.md  # 系统架构（含 Mermaid）
│   ├── scope_and_non_goals.md  # 范围与不做项
│   ├── feasibility_probe_72h.md# 72 小时探针计划
│   ├── interface_spec.md       # 接口规范
│   ├── experiment_protocol.md  # 实验协议
│   ├── risk_register.md        # 风险登记册
│   ├── git_workflow.md         # Git 工作流
│   ├── team_responsibilities.md# 团队分工
│   └── issue_backlog.md        # Issue 清单
├── 01_plant/                   # 柔性关节数字样机
│   ├── matlab/                 # 双惯量动力学仿真
│   ├── simulink/               # Simulink 接口约定说明
│   ├── parameters/             # 载荷参数（JSON）
│   └── tests/                  # Plant 冒烟测试
├── 02_observer/                # 状态观测器
│   ├── matlab/                 # 增广 EKF 实现
│   ├── baselines/              # 对比基线（电机映射、简单扰动估计）
│   └── tests/                  # Observer 冒烟测试
├── 03_confidence_trigger/      # 可信评分与事件触发
│   ├── confidence/             # 可信评分与信号健康
│   ├── event_trigger/          # 事件触发条件
│   ├── calibration/            # 校准策略说明
│   └── rollback/               # 更新门控
├── 04_classification/          # 振动-接触分类
│   ├── features/               # 特征提取
│   ├── rule_based/             # 规则分类器
│   ├── learning/               # 后续机器学习扩展
│   └── datasets/               # 数据集说明
├── 05_control/                 # 控制模式
│   ├── normal_tracking/        # 正常跟踪
│   ├── vibration_suppression/  # 振动抑制
│   ├── safe_slowdown/          # 安全减速
│   ├── degraded_mode/          # 降级模式
│   └── mode_manager.m          # 模式管理器
├── 06_validation/              # 验证与评估
│   ├── metrics/                # 指标计算
│   ├── fault_injection/        # 故障注入配置
│   ├── monte_carlo/            # 蒙特卡洛分析
│   └── reports/                # 测试报告
├── 07_app/                     # 应用层
│   ├── dashboard/              # 虚拟传感器看板
│   ├── state_manager/          # 状态管理
│   └── demo/                   # 一键演示
├── 08_sil/                     # C/C++ SIL 实现
│   ├── include/                # C 头文件
│   ├── src/                    # C 源文件
│   ├── tests/                  # C 冒烟测试（ctest）
│   └── benchmarks/             # 性能基准
├── 09_test_agent/              # 智能测试 Agent
│   ├── tools/                  # 测试工具（run_case, validate_schema, collect_metrics）
│   ├── workflows/              # 测试工作流定义
│   └── templates/              # 报告模板
├── common/                     # 公共模块
│   ├── schemas/                # JSON Schema 定义
│   ├── constants/              # 常量定义
│   └── utils/                  # 工具函数
├── configs/                    # 探针运行配置
├── scripts/                    # 一键运行脚本
├── tests/                      # 跨模块测试
│   └── python/                 # Python pytest 测试
├── results/                    # 仿真结果
├── .editorconfig
├── .gitattributes
├── .gitignore
├── pyproject.toml
├── requirements-dev.txt
├── README.md
├── CONTRIBUTING.md
└── LICENSE_NOTICE.md
```

---

## 6. 软件环境

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | ≥ 3.12 | 类型标注 + pytest 测试 |
| GCC/G++ | ≥ 13 | C11 标准、CMake 构建 |
| CMake | ≥ 3.28 | SIL 构建系统 |
| MATLAB | R2022b+（可选） | MATLAB/Simulink MIL（Octave 部分兼容） |
| Octave | ≥ 8.0（可选） | MATLAB 代码的免费替代运行环境 |

---

## 7. 72 小时探针运行方式

三个探针依次回答三个核心可行性问题：

| 探针 | 问题 | 命令 |
|------|------|------|
| Probe 1 | 负载侧状态能否估计？ | `run_probe` |
| Probe 2 | 外部扰动是否可分辨？ | `run_probe` |
| Probe 3 | 可信评分是否有效？ | `run_probe` |

详细定义见 `00_docs/feasibility_probe_72h.md`。

---

## 8. MATLAB 运行方式

```matlab
% 启动 MATLAB/Octave，切换到项目根目录
>> setup_project       % 添加所有模块到路径
>> run_probe           % 一键运行三个探针

% 或单独运行测试
>> runtests('01_plant/tests/test_plant_smoke.m')
>> runtests('02_observer/tests/test_observer_smoke.m')
```

**注**：本项目当前阶段的 MATLAB 代码在 Octave 环境下部分兼容。如果在 Octave 中遇到不兼容问题，请提交 Issue 或使用 MATLAB 运行。

---

## 9. Python 测试方式

```bash
# 安装依赖
pip install -r requirements-dev.txt

# 运行所有 Python 测试
python -m pytest tests/python/ -v

# 运行特定测试
python -m pytest tests/python/test_schema_validation.py -v
```

Python CI 配置见 `.github/workflows/python-ci.yml`。

---

## 10. C/SIL 构建方式

```bash
# 配置
cmake -S 08_sil -B 08_sil/build

# 构建
cmake --build 08_sil/build

# 运行测试
ctest --test-dir 08_sil/build --output-on-failure

# 或使用一键脚本
bash scripts/run_sil_tests.sh
```

C 代码实现为基线骨架（baseline skeleton），Observer 算法尚未完整移植。详见 `08_sil/` 目录。

---

## 11. 当前状态

| 模块 | 状态 | 说明 |
|------|------|------|
| 00_docs | ✅ 完成 | 全部 10 份文档已编写 |
| 01_plant | 🚧 骨架 | MATLAB 函数已实现，Simulink 待建模 |
| 02_observer | 🚧 骨架 | EKF 初始化与单步已实现 |
| 03_confidence_trigger | 🚧 骨架 | 可信评分与信号健康已实现 |
| 04_classification | 🚧 骨架 | 规则分类器已实现 |
| 05_control | 📋 占位 | 模式管理器骨架已创建 |
| 06_validation | 🚧 骨架 | 指标函数已实现 |
| 07_app | 📋 占位 | 仅 README |
| 08_sil | 🚧 骨架 | C 项目可编译、可测试 |
| 09_test_agent | 🚧 骨架 | 测试工具已创建 |
| Python tests | ✅ 通过 | 全部 pytest 通过 |
| C SIL tests | ✅ 通过 | 全部 ctest 通过 |
| MATLAB tests | ⏸️ 未执行 | 需 MATLAB/Octave 环境 |

---

## 12. 团队分工

| 角色 | 同学 | 主要负责 |
|------|------|----------|
| 项目负责人 | 待定 | 总体架构、事件触发校准、可信门控、集成 |
| Simulink 同学 | 待定 | 双惯量 Plant、EKF 框架、MIL |
| 深度学习通感算同学 | 待定 | 特征提取、规则分类、数据集、测试 Agent |
| 计算机软件同学 | 待定 | 虚拟传感器看板、状态机、自动报告 |
| 嵌入式 Linux 同学 | 待定 | C SIL 实现、一致性测试、性能基准 |

详细职责见 `00_docs/team_responsibilities.md`。

---

## 13. 不作出的声明

- ❌ 本项目**不声称**已在工业硬件上部署或验证
- ❌ 本项目**不声称**达到任何工业安全认证等级
- ❌ 本项目**不包含**虚构的实验结果或性能指标
- ❌ 本项目**不使用**负载侧传感器数据作为观测器输入
- ❌ 本项目**不实现** ROS 2、Gazebo、Isaac Sim 等外部集成
- ❌ 本项目**不涉及**深度强化学习或多机器人分布式控制

所有实验结果均来自仿真环境，仅用于学术和比赛目的。

---

## 14. 开源与比赛材料说明

本项目为比赛参赛作品，代码和文档在 GitHub 上公开用于评审和学术交流。

- 不采用正式开源许可证（`LICENSE_NOTICE.md` 仅做声明）
- 比赛材料（论文、视频、演示文稿）独立于本仓库管理
- 如有引用本项目的第三方代码或算法，已在相应文件中标注出
