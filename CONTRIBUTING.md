# 贡献指南

## 分支与拉取请求

- 不直接向 `main` 提交或推送；每项工作使用短生命周期分支和一个 PR。
- 分支使用 `chore/`、`feat/`、`fix/`、`docs/`、`test/` 或 `probe/` 前缀。
- 不维护长期 `develop` 分支。
- PR 默认先创建为 Draft，并说明范围、非目标、验证、未运行检查和风险。
- 每个 PR 只解决一个阶段目标，不混入无关重构或生成数据。
- 禁止自动合并；至少由一位其他同学人工审查。
- 主体模块变更必须得到对应负责同学确认。

## 提交规范

提交信息使用 Conventional Commits：

```text
docs: approve project scope and review stage gates
fix: make Python package installable
test: validate public interface schemas
```

仅暂存本 PR 需要的文件。提交、推送和创建 PR 前遵循仓库的危险操作确认规则。

## 公共接口变更

公共字段、枚举、单位或语义变更必须同步：

- `docs/02_architecture/interface_spec.md`；
- `common/schemas/`；
- `python/flexsense_guard/types.py`；
- 受影响的 MATLAB 结构体和 C 头文件；
- 一致性测试。

PR 必须说明兼容性影响，并得到受影响模块负责同学确认。

## 验证要求

Python 基础变更至少执行：

```bash
python -m pip install -e .
python -m pytest -q
```

MATLAB/Octave、C/SIL、App 或其他环境未运行时，必须在 PR 中标为 `NOT RUN`。
不得把编译成功等同于算法通过，也不得用 Python 结果替代 MATLAB 复验。

## 数据与声明边界

- 外扰统一使用 `estimated_external_torque_nm`。
- `confidence_score` 与 `contact_score` 都不是概率。
- 禁止 `contact_probability`。
- 负载侧真值只用于评价，不得进入运行时算法。
- `ActuatorCommand`、`PlantInputTrace`、`TorqueFeedback` 和 `ObserverInput` 分责；
  Observer 不得读取原始指令、`motor_torque_applied_nm` 或 Plant 真值。
- Plant 真值配置与版本化名义参数库必须隔离，在线校准只能更新名义参数版本。
- 历史运行结果与当前可行性结论分开记录；证据无效或不足时使用
  `NOT_VERIFIED`。
- 不提交专利、比赛敏感材料、个人数据或大规模生成结果。
- 不宣称未经验证的硬件、实时性、碰撞检测或工业安全能力。

## 责任归属

项目负责人同学负责规则和集成，可以建立最小独立参考；各模块负责同学对其模块的
源码、测试、运行结果和技术说明负责。Codex 生成代码按照所在模块归属。
