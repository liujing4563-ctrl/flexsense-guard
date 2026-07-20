# FlexSense-Guard

面向柔性机器人关节的虚拟感知与安全控制仿真项目，仅使用电机侧信号。

## 当前阶段

PR-0 仓库基线已合并。首个 P1 可行性探针返回 `fail`，可复现证据见
[`docs/probe_results.md`](docs/probe_results.md)。因此，项目已降级为电机侧控制
仿真；不宣称虚拟感知、分类、控制逻辑、SIL 或应用层已得到验证。

部分编号目录在仓库基线建立前已被导入。它们仅作为探索性材料保留，后续模块必须
由独立 PR 提供验证后才可视为有效实现。

## 项目范围

- 一个主导柔性关节及其双惯量数字 Plant。
- 使用电机侧位置、速度、电流和力矩作为观测器输入。
- 输出负载侧状态估计与外部扰动**力矩**估计。
- 研究正常跟踪、振动抑制、安全减速和降级模式。

本项目不使用负载侧传感器输入，也不涉及多机器人、Kuramoto 同步、强化学习、
ROS/Gazebo/Isaac 集成、硬件效果声明或工业安全认证。仓库当前为公开状态，
不包含专利或比赛敏感材料。

## 规范文档

当前规范文档位于 [`docs/`](docs/)。历史 `00_docs/` 目录仅用于追溯，已由
`docs/` 下的对应文档取代。

核心文档：

- [`docs/project_charter.md`](docs/project_charter.md)
- [`docs/system_architecture.md`](docs/system_architecture.md)
- [`docs/interface_spec.md`](docs/interface_spec.md)
- [`docs/feasibility_probe_72h.md`](docs/feasibility_probe_72h.md)
- [`docs/scope_and_non_goals.md`](docs/scope_and_non_goals.md)

## Python 冒烟检查

```bash
python -m pip install -e ".[dev]"
python -m pytest python/tests -q
```

PR-0 阶段未执行或宣称 MATLAB/Octave 与 C/SIL 检查结果；后续任何阶段都必须如实
记录已执行和未执行的验证。

## 推进记录

1. PR-0：仓库基线与可执行数据契约——已完成。
2. P1 可行性探针：负载侧状态估计——已失败，详见记录结果。
3. 在形成独立审查的新启动决议前，虚拟感知后续开发均被阻断；不得推进分类、
   控制、SIL、应用层或测试 Agent 工作。

创建分支或 Pull Request 前，请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
