# 证据管理规范

## 原则

结果是否进入 Git 与结果是否必须留存是两件事。大型时间序列、构建产物和临时
日志可以存放在外部受控位置；机器可读汇总、证据索引、失败记录和阶段决定必须
进入版本控制。

## 目录

```text
results/
├── p1/
├── p2/
├── p3/
├── integration/
├── reports/
└── generated/
```

`06_validation/reports/**` 保存报告生成逻辑和模板，`results/reports/**` 保存由真实
证据生成的报告产物。阶段未执行时只保留 README，不创建虚构汇总。

## 每次实验必需字段

| 字段 | 要求 |
|---|---|
| `experiment_id` | 全局唯一且不可复用的实验标识 |
| `stage` | `P1`、`P2`、`P3`、`INTEGRATION`、`SIL`、`APP` 或 `DEMO` |
| `git_commit` | 实际运行对应的完整提交标识 |
| `algorithm_version` | 被测算法或规范版本 |
| `schema_version` | 输入输出 Schema 版本 |
| `scenario_id` | 场景唯一标识 |
| `configuration_id` | 版本化配置标识 |
| `random_seed` | 非负随机种子，包含 seed 0 |
| `software_environment` | 操作系统、MATLAB/Python/编译器及依赖版本 |
| `start_time` | 带时区或 UTC 的开始时间 |
| `runtime` | 总运行时间及单位；算法单步时间另存 `runtime_ms` |
| `decision` | `PASS`、`FAIL` 或 `NOT_VERIFIED` |
| `valid_flag` | 证据结构和必需输入是否有效 |
| `failure_reason` | 失败、无效或未验证原因；成功时明确为空或 `NONE` |
| `artifact_index` | 原始数据、日志、图、配置、汇总和校验值的索引 |

P1 还必须记录 Plant 真实参数、Observer 名义参数、失配比例、三类力矩追溯和评价
窗口。每次运行同时记录工作区是否干净、实际命令、负责人和审查人。

## 决定与运行状态

阶段和案例决定只使用 `PASS`、`FAIL`、`NOT_VERIFIED`。单条命令状态使用
`PASSED`、`FAILED`、`NOT RUN`，不得混用。环境缺失或命令未执行时必须写
`NOT RUN`，不能推测通过。

## 数据隔离

1. Plant 真值只进入离线评价；
2. 调参集和最终评价集必须按场景、负载和 seed 预先分离；
3. 评价数据不得用于选择 Q/R/P、阈值、权重或候选方法；
4. 修改参数后创建新实验，不回写旧实验；
5. 数据划分、冻结时间和负责人必须进入证据索引。

## 多 seed 与失败结果

- 必须报告所有已登记 seed，不能只选最好结果；
- 连续指标汇总至少包含中位数、第一四分位数、第三四分位数和失败数；
- 计数指标包含总数与逐案例分布；
- NaN、Inf、发散、提前终止和缺失案例均计入失败数；
- 失败结果不得删除、覆盖或从分母中静默排除；
- 旧结果必须保留原始历史状态，并与新运行按提交和实验 ID 区分。

## Git 与外部证据

原始大数据可以不提交 Git，但必须在 `artifact_index` 中保存受控位置、文件大小、
校验值、保管人和访问条件。小型汇总 JSON、配置快照、证据索引、失败清单和阶段
决定必须提交。外部证据不可访问或校验失败时，阶段决定为 `NOT_VERIFIED`。

## Mock 与无效证据

`configs/mock/**` 只能用于 App 和跨模块接口联调，必须标记 `data_source: MOCK` 和
`valid_for_algorithm_evaluation: false`。Mock 不得进入 `results/p1`、`p2`、`p3`
或性能汇总，也不得作为 P1/P2/P3、实时性或安全声明的证据。

## JSON 有效性

机器可读结果不得包含 NaN、Inf、未声明字段或单位不明的数值。无法计算的可选指标
应省略并记录失败原因；必需指标无法计算时令 `valid_flag=false`，决定不得为
`PASS`。
