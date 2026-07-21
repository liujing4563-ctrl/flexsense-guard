# 跨语言契约矩阵

## 目的

本矩阵用于跟踪公共字段在文档、JSON、Python、MATLAB、C/C++ 和 App 中的落地
状态。语义冻结不等于所有语言已经迁移，只有各实现完成一致性测试后，端到端
契约才可标记为已验证。

状态取值：`FROZEN`、`IMPLEMENTED`、`PENDING`、`BLOCKED`、`NOT_APPLICABLE`。

## 当前矩阵

| 契约项 | 文档语义 | JSON Schema | Python | MATLAB/Simulink | C/C++ SIL | App | 当前结论 |
|---|---|---|---|---|---|---|---|
| 三类电机力矩字段 | `FROZEN` | `IMPLEMENTED` | `IMPLEMENTED` | `PENDING` | `BLOCKED` | `BLOCKED` | 端到端 `NOT_VERIFIED` |
| `VirtualSensingEstimate` 输出 | `FROZEN` | `IMPLEMENTED` | `IMPLEMENTED` | `PENDING` | `BLOCKED` | `BLOCKED` | Python/JSON 一致 |
| 分类状态枚举 | `FROZEN` | `IMPLEMENTED` | `IMPLEMENTED` | `PENDING` | `BLOCKED` | `BLOCKED` | 主体功能受 P2 阻断 |
| 运行模式枚举 | `FROZEN` | `IMPLEMENTED` | `IMPLEMENTED` | `PENDING` | `BLOCKED` | `BLOCKED` | 状态机规范已定义 |
| 原因码 | `FROZEN` | `IMPLEMENTED` | `IMPLEMENTED` | `PENDING` | `BLOCKED` | `BLOCKED` | 新增值须走接口 PR |
| 验证结论 | `FROZEN` | `IMPLEMENTED` | `NOT_APPLICABLE` | `PENDING` | `BLOCKED` | `BLOCKED` | 统一为 `PASS/FAIL/NOT_VERIFIED` |
| 场景配置 | `FROZEN` | `IMPLEMENTED` | `PENDING` | `PENDING` | `NOT_APPLICABLE` | `BLOCKED` | 尚无端到端运行证据 |

## 权威来源

| 内容 | 权威来源 |
|---|---|
| 字段语义、单位、范围 | [`interface_spec.md`](interface_spec.md) |
| 符号和力矩所在侧 | [`glossary_and_symbols.md`](glossary_and_symbols.md) |
| JSON 结构 | `common/schemas/*.schema.json` |
| Python 参考类型 | `python/flexsense_guard/types.py` |
| MATLAB 信号定义 | 由 Simulink 同学在 `01_plant/**`、`02_observer/**` 和 runner 中迁移 |
| C/C++ 类型 | 由嵌入式 Linux 同学在 `08_sil/include/**` 中实现 |
| App 映射 | 由计算机软件同学在 `07_app/**` 中实现 |

## 兼容与迁移规则

1. 项目负责人先冻结语义、单位、枚举和失效行为。
2. 公共 Schema 与 Python 参考类型在同一契约 PR 中迁移并通过自动测试。
3. 模块负责同学在各自主责路径迁移语言类型，不得保留含糊的兼容别名。
4. 旧数据如需读取，必须在模块边界做显式版本转换，不得污染新公共结构。
5. 任何字段变更都要更新本矩阵、Mock 样例和受影响测试。
6. 端到端状态只有在真实生产者和消费者共同回放通过后才能标记为 `FROZEN`。

## 当前交接

项目负责人已完成文档、JSON Schema 和 Python 公共契约层。Simulink 同学下一步
负责 MATLAB 三类力矩字段、Plant 输出和 Observer 输入迁移；该工作完成并复验前，
不得声称公共输入链路已完全冻结。
