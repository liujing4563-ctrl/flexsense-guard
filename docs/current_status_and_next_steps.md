# 当前完成情况与下一步

## 状态快照

快照日期：2026-07-21。

当前分支：`chore/project-lead-foundation`。本分支内容尚未提交、推送或合并，因此
“本分支已完成”表示工作区实现和本地验证完成，仍需团队审查。

| 工作部分 | 当前完成情况 | 证据或说明 |
|---|---|---|
| 项目章程与范围 | 本分支已完成 | 单关节范围、必做项、非目标和 A/B/C 路线已写明 |
| 系统架构 | 本分支已完成 | 运行时数据、真值、评价、配置和各实现层已分离 |
| 数学模型与力矩侧定义 | 本分支形成冻结候选 | 负载侧弹性力矩、齿轮方向、电机侧反射和能量检查已定义，待 Simulink 同学共同确认 |
| 公共输出接口 | 本分支形成冻结候选 | 分类状态、运行模式、输出 Schema 和 Python 输出类型已统一 |
| 公共输入接口 | `NOT FROZEN` | 三类力矩字段已定义，Python、MATLAB 和输入 Schema 尚待迁移 |
| P1/P2/P3 门禁 | 本分支已完成 | 指标、证据、失败条件和降级路线已明确 |
| 五位同学职责 | 本分支已完成 | 输入、输出、交付、验收、依赖、交接和禁止越界已明确 |
| 仓库治理 | 本分支已完成 | Git、PR、Issue、Codex 和真实测试记录规则已完善 |
| 中文文档 | 本分支已完成 | 当前规范和协作模板使用中文，技术标识保持原样 |
| Python 包安装 | 本地验证通过 | `python3 -m pip install -e .` 成功 |
| Python 基础测试 | 本地验证通过 | `python3 -m pytest -q`：6 passed |
| MATLAB Plant / EKF | 仅有历史代码，当前未验证 | 旧实现存在力矩侧定义和输入一致性问题；本工作包未修改主体算法 |
| 历史 P1 执行结果 | `FAIL` | 保留仓库旧 MATLAB 运行记录 |
| 历史 P1 证据有效性 | `INVALID / INSUFFICIENT` | 模型未冻结、Plant/Observer 输入不一致、单负载单场景单 seed、同批真值选择 Q |
| 当前 P1 可行性结论 | `NOT_VERIFIED` | 不能由无效或不足证据判断 EKF 路线可行或不可行 |
| P2 / P3 | `BLOCKED` | P1 尚未形成有效、充分且可复现的 `PASS` 证据 |
| Simulink `.slx` | 未完成 | 由 Simulink 同学后续负责 |
| C/C++ SIL | 未开始 | 等待 P1 和主算法冻结 |
| App | 未开始 | 等待 P1，通过前只允许 Mock 方案设计 |
| 测试 Agent | 仅占位 | 等待 P1，通过前不开发主体 |

## 当前唯一项目动作

先由项目负责人同学冻结力矩所在侧、齿轮方向、Plant 方程、Observer 输入和 P1
证据有效性规则，再由 Simulink 同学共同确认。确认后将数学模型、接口、P1 门禁
和实验协议交给 Simulink 同学，由其修改 MATLAB 主实现并重新运行 P1。

在得到新的 MATLAB P1 证据前：

- 不启动 P2 或 P3；
- 不开发完整 App；
- 不开发 C/C++ SIL；
- 不开发测试 Agent 主体；
- 不把当前 P1 写成 `PASS` 或基于旧证据写成技术路线 `FAIL`；
- 不用 Python 结果替代 MATLAB 复验。

## 每位同学现在要做什么

| 同学 | 立即行动 | 本阶段交付 | 当前禁止事项 |
|---|---|---|---|
| 项目负责人同学 | 冻结力矩侧、齿轮方向、数学模型、三类力矩字段、证据有效性和 P1 门禁；组织共同确认 | 模型与输入契约、状态修正、审查记录、P1 交接清单 | 不直接修改 Plant、EKF、runner 或 Q/R/P |
| Simulink 同学 | 先共同确认模型和输入契约；再修改 Plant、EKF 输入与 runner 并实际运行 MATLAB P1 | 三负载、多随机种子的 MATLAB P1 配置、日志、指标、曲线和结论 | 未确认模型前不改算法；不降低门限、不输入负载真值 |
| 深度学习通感算同学 | 审查分类状态和数据接口；准备 P2 数据划分、故障场景和无泄漏方案 | P2 数据与评价方案，不含主体分类实现 | P1 形成有效 `PASS` 证据前不训练分类器、不批量生成正式 P2 结果、不开发测试 Agent 主体 |
| 计算机软件同学 | 审查配置、状态和报告 Schema；设计 Mock 数据与结果管理方案 | App 信息架构、字段映射和自动报告方案 | P1 形成有效 `PASS` 证据前不开发完整 App，不把 Mock 数据当实验数据 |
| 嵌入式 Linux 同学 | 审查公共类型、单位和异常处理要求；准备 SIL 移植与一致性验收清单 | C/C++ 接口、构建、回放和资源测试计划 | 主算法冻结前不移植 Observer，不自行改变模型或公共字段 |

## P1 交接清单

项目负责人同学向 Simulink 同学交付：

1. [`project_charter.md`](01_project/project_charter.md) 中的项目范围和有效证据路线；
2. [`system_architecture.md`](02_architecture/system_architecture.md) 中的数学模型、力矩侧、能量检查和数据流；
3. [`interface_spec.md`](02_architecture/interface_spec.md) 中的三类力矩字段和公共输入输出；
4. [`feasibility_probe_72h.md`](03_validation/feasibility_probe_72h.md) 中的 P1 门禁；
5. [`experiment_protocol.md`](03_validation/experiment_protocol.md) 中的公平比较和证据规则；
6. [`probe_results.md`](03_validation/probe_results.md) 中保留的旧 P1 失败记录；
7. [`risk_register.md`](01_project/risk_register.md) 中与 P1 有关的风险和降级条件。

Simulink 同学交回：

1. MATLAB 版本、提交标识和干净工作区状态；
2. Plant 与 Observer 参数及失配比例；
3. light、medium、heavy 和随机种子 0 到 9 的配置；
4. baseline 与 EKF 的位置、速度误差；
5. 有限性、发散、最大误差和运行时间；
6. 实际命令、完整输出和机器可读汇总；
7. `PASS`、`FAIL` 或 `NOT_VERIFIED` 结论及失败分类。

## 下一阶段决策

```text
P1 PASS
→ 进入 P2，并继续验证 A/B 路线

P1 证据 INVALID / INSUFFICIENT
→ 当前结论为 NOT_VERIFIED，先修复模型、输入和实验设计

P1 基于有效证据 FAIL
→ 项目负责人组织 C 路线决策

P1 NOT_VERIFIED
→ 补齐 MATLAB、参数、多负载和多随机种子证据
```

## 本工作包完成条件

- 核心文档对历史结果、证据有效性和当前 P1 状态表述一致；
- 五位同学当前行动和禁止边界明确；
- 公共输出文档、Schema 和 Python 类型一致，公共输入迁移缺口已明确；
- 根目录安装和测试无需 `PYTHONPATH`；
- Plant、EKF 和其他主体算法没有被本工作包修改；
- 历史 P1 执行结果保持 `FAIL`，当前可行性结论统一为 `NOT_VERIFIED`；
- MATLAB、C/SIL 和 App 未运行项如实标记；
- 经至少一位其他同学审查后，才能进入合并流程。
