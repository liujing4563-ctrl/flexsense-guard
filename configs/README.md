# 配置目录

主责：计算机软件同学。项目负责人维护公共配置 Schema 和早期 Mock 样例。

- `mock/`：仅用于接口联调，所有文件必须明确标记 `MOCK`；
- 正式运行配置须关联 Schema、提交、随机种子和结果索引；
- 模块算法参数由对应模块同学确认，软件同学不得自行改动；
- Mock 数据不是仿真结果，不得进入阶段验收。
- `ImmutablePlantTrueConfig` 与 `VersionedNominalParameterStore` 必须是独立配置域；
  软件同学不得把校准候选写回 Plant 真值配置。
- 场景配置必须声明 `plant_true_configuration_id`、
  `nominal_parameter_version` 和数据分区，供证据追溯与调参隔离。

当前状态只以 [`docs/current_status_and_next_steps.md`](../docs/current_status_and_next_steps.md)
为准。本目录说明责任和格式，不声明正式配置管理已经实现。
