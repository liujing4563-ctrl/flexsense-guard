# Mock 接口样例

本目录中的 JSON 全部用于 App、报告和跨模块契约联调，不是 Plant、Observer、P1、
P2 或 P3 的运行结果。每个文件外层固定包含：

```text
fixture_type: MOCK
data_source: MOCK
valid_for_algorithm_evaluation: false
```

`payload` 才是接受对应 JSON Schema 校验的公共数据。Mock 元信息保留在包装层，
避免向 `additionalProperties: false` 的公共 Schema 注入非契约字段。

禁止把这些样例复制到 `results/**`、用于选择阈值或权重、计算性能指标，或作为
算法、实时性和安全能力证据。样例中的数值只为覆盖字段和状态，不表达性能结论。

## v2 样例覆盖

- 输入链：`ActuatorCommand`、`PlantInputTrace`、`RawMotorMeasurement`、
  `TorqueFeedback`、`SignalHealthStatus`、`ObserverInput`；
- 输出链：四种 `SystemStateSnapshot` 和 `ControlCommand`；
- 校准链：`NominalParameterVersion`、`CalibrationCandidate`、
  `CalibrationDecision`；
- 证据链：P1 stage 的 `ValidationReport`。

不适用字段必须省略。Mock 可以包含物理上合法的零值，但不得用 `0.0` 代替 N/A，
也不得把占位数值解释为算法性能。
