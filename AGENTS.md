# FlexSense-Guard 工程约束

## 范围与阶段顺序

- 项目只研究一个主导柔性关节。
- 每个分支和 PR 只完成一个阶段目标。
- P1-V 未形成有效、充分且可复现的 `PASS` 证据前，不启动 P2、P3、App、C/SIL
  或测试 Agent 主体开发；P1-A 失败不得被解释为状态不可估计。
- P2 未通过前，不形成外部接触可靠识别主张。
- P3 未通过前，可信评分不得驱动安全模式。
- 公开仓库不得存放专利、比赛敏感材料或个人数据。

## 公共数据契约

- 外扰输出统一使用 `estimated_external_torque_nm`。
- 未声明 Jacobian、等效力臂和坐标变换时，不得输出或宣称末端力。
- `confidence_score` 是工程可信评分，不是统计概率。
- `contact_score` 是接触证据评分，不是概率。
- 禁止引入 `contact_probability`。
- Plant 真值只用于评价，不得进入 Observer、Confidence、Classification、
  Mode Manager 或 Control。
- Plant 真实参数与 Observer 名义参数必须分离。
- 统一使用 `tau_s_load_nm` 表示负载侧弹性力矩；电机侧反射关系必须在模型文档中
  明确、由 Simulink 同学共同确认并通过能量一致性检查。
- 命令、Plant 实际输入和 Observer 转矩反馈必须分别使用 `ActuatorCommand`、
  `PlantInputTrace` 和 `TorqueFeedback`；Observer 只能读取 `ObserverInput`，禁止读取
  原始指令、`motor_torque_applied_nm`、Plant 真值或真实参数。
- `ImmutablePlantTrueConfig` 与 `VersionedNominalParameterStore` 必须隔离；在线校准
  不得修改 Plant 真值或使用负载侧真值作更新决定。
- 历史执行结果和当前技术结论必须分层记录；无效或不足证据对应
  `NOT_VERIFIED`，不得解释为技术路线失败。
- 公共接口变更必须同步文档、Schema、Python 类型及受影响语言定义。

## 工程与验证

- Python 公共代码保持类型明确，并使用聚焦的 pytest 测试。
- 实际运行状态使用 `PASSED`、`FAILED` 或 `NOT RUN`。
- 未运行的 MATLAB/Octave、C/SIL、App 或其他检查不得写成通过。
- 不虚构性能、硬件结果、碰撞检测率或工业安全能力。
- 失败结果和阶段决定必须保留，不得覆盖历史证据。
- 生成数据默认不进入源码版本控制，明确要求的小型汇总除外。
- 文档使用简体中文，参与者统一称为“同学”。

## Git 与 PR

- 不直接提交或推送 `main`。
- 不创建长期 `develop` 分支。
- 每个 PR 必须说明范围、非目标、验证、未运行检查和风险。
- 禁止自动合并 PR。
- 主体模块 PR 必须由对应负责同学确认。
- 项目负责人同学负责最终集成审查，但不替模块同学签署主体实现。

## Codex 使用边界

- Codex 不得自行扩大项目范围或跨越阶段门。
- 项目负责人同学可以使用 Codex 建立最小参考实现用于独立验证，但不长期代替
  模块负责同学完成主体实现。
- Codex 生成代码的责任按照代码所在模块确定，不按照发出提示词的人确定。
- 修改前先阅读现有实现；不得把占位文件、未运行测试或文档计划当成已完成功能。
- 未经明确要求，不创建提交、不推送分支、不创建或合并 PR。
