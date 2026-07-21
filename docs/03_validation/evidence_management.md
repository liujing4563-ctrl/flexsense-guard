# 证据管理规范

## 原则

大型时间序列、构建产物和临时日志可以保存在外部受控位置；机器可读汇总、证据
索引、失败记录和阶段决定必须进入版本控制。Mock 只能用于契约联调。

## 结果目录

```text
results/
├── p1/
├── p2/
├── p3/
├── integration/
├── reports/
└── generated/
```

阶段未执行时只保留 README，不创建虚构性能汇总。

## 公共 Evidence Envelope

每份阶段报告至少包含：

| 字段 | 要求 |
|---|---|
| `schema_version` | 当前 v2 为 `2.0.0` |
| `report_id` | 全局唯一报告标识 |
| `experiment_id` | 全局唯一且不可复用的实验标识 |
| `stage` | `P1`、`P2`、`P3`、`SIL` 或 `INTEGRATION` |
| `git_commit` | 实际运行对应的完整提交标识 |
| `algorithm_version` | 被测算法版本 |
| `configuration_id` | 版本化配置标识 |
| `scenario_id` | 场景标识 |
| `random_seed` | 非负随机种子，包含 seed 0 |
| `software_environment` | 操作系统、MATLAB/Python/编译器和依赖版本 |
| `decision` | `PASS`、`FAIL` 或 `NOT_VERIFIED` |
| `valid_flag` | 报告和必需证据是否有效 |
| `failure_reason_codes` | 失败、无效或未验证原因；无原因时为空数组 |
| `artifact_index` | 原始数据、日志、图、配置和校验值索引 |
| `runtime_ms` | 报告所声明计时边界对应的运行时间 |
| `result` | 与 `stage` 对应的阶段 payload |

`ArtifactIndexEntry` 记录 artifact ID、类型、受控 URI、SHA-256、大小、保管人和可用
状态。外部证据不可访问或校验失败时，报告不得 `PASS`。

## 阶段 Payload

### P1

只要求位置、速度、最大误差、baseline、公平改善、有限性和发散等 P1 指标。P1-A
还必须报告改善中位数、四分位距、评价 seed 总数和胜出 seed 数。
`external_torque_rmse_nm` 可以作为可选诊断指标，不是 P1 强制门禁。

### P2

只要求 P2-VIB、P2-CONTACT 结论及适用的事件级误报、漏报和延迟。没有成功检出时
省略 `detection_delay_s`，并通过漏检计数和失败原因表达。

### P3

只要求 P3-DEGRADE、P3-ACTION、P3-RECOVERY 结论以及评分、动作和恢复指标。

### SIL 与 Integration

SIL 记录数值一致性、运行时间、内存和异常保护。Integration 记录契约回放、组件
版本和违反次数。

不适用指标必须省略，不得使用 `0.0`、空字符串或 NaN 表示 N/A。

## 数据隔离

1. `ImmutablePlantTrueConfig` 与 `VersionedNominalParameterStore` 独立；
2. `PlantInputTrace` 和 Plant 真值只进入 Plant 或离线评价；
3. `ObserverInput` 禁止 applied torque、真实负载状态和 Plant 真参数；
4. 调参集与最终评价集按场景、负载和 seed 预先分离；
5. 评价数据不得选择 Q/R/P、阈值、权重或候选方法；
6. 在线校准验收不得读取离线真值；
7. 修改参数后创建新实验，不回写旧实验。

## 多 seed 和失败结果

- 报告全部登记 seed，不选择最好结果；
- 连续指标至少汇总中位数、Q1、Q3 和失败数；
- 计数指标报告总数和逐案例分布；
- NaN、Inf、发散、提前终止和缺失案例均计入失败；
- 失败结果不得删除、覆盖或静默排除；
- 历史结果按提交和实验 ID 与新结果区分。

## Mock

`configs/mock/**` 必须包含：

```text
fixture_type: MOCK
data_source: MOCK
valid_for_algorithm_evaluation: false
```

Mock 不得进入正式结果目录或阶段汇总。Mock payload 中只填写该阶段适用字段；不适用
指标省略，不能用零值冒充“零误差”或“零延迟”。

## 运行状态

阶段决定只使用 `PASS/FAIL/NOT_VERIFIED`；单条命令只使用
`PASSED/FAILED/NOT_RUN`。一种语言的测试不能替代另一种语言或算法实验。

## JSON 有效性

机器结果不得包含 NaN、Inf、未声明字段或单位不明数值。必需指标无法计算时设置
`valid_flag=false`、记录原因并使用 `NOT_VERIFIED`，不得填入虚构数值。
