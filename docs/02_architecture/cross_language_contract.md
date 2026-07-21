# 跨语言契约矩阵

## 目的与状态定义

本矩阵逐字段记录文档、Python、JSON Schema、MATLAB、C 和 App 的真实落地状态。
字段语义冻结不代表算法已经实现，也不代表端到端链路已经验证。

状态只能使用：

| 状态 | 含义 |
|---|---|
| `FROZEN` | 该层的字段名称、类型、单位和枚举已经对齐并受契约测试约束 |
| `PARTIAL` | 已有部分定义或实现，但仍存在缺项、候选值或未验证映射 |
| `NOT FROZEN` | 已有旧实现或草案，但尚未迁移到当前权威契约 |
| `MISSING` | 当前仓库中不存在该层映射 |
| `NOT APPLICABLE` | 该字段按架构不应出现在该层 |

## 字段矩阵

| 字段 | 含义 | 单位 | 文档 | Python | Schema | MATLAB | C | App | 当前状态 |
|---|---|---:|---|---|---|---|---|---|---|
| `timestamp_s` | 当前样本时间 | s | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `torque_command_nm` | 执行器模型前的电机侧力矩指令 | N·m | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `motor_torque_applied_nm` | 执行器约束后实际施加到 Plant 的电机侧力矩 | N·m | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `motor_torque_measured_nm` | Observer 可获得的电机侧测量或估计力矩 | N·m | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `motor_position_rad` | 电机侧角位置测量 | rad | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `motor_velocity_rad_s` | 电机侧角速度测量 | rad/s | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `motor_current_a` | 电机电流测量 | A | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `estimated_load_position_rad` | 负载侧角位置估计 | rad | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `estimated_load_velocity_rad_s` | 负载侧角速度估计 | rad/s | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `estimated_torsion_rad` | `theta_m/N-theta_l` 的估计 | rad | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `estimated_external_torque_nm` | 负载侧外部关节扰动力矩估计 | N·m | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `innovation_norm` | Observer 创新残差范数 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `confidence_score` | 工程可信评分，不是概率 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `contact_score` | 接触证据评分，不是概率 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `classification_state` | 四值分类状态 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `operation_mode` | 四值运行模式 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `valid_flag` | 当前状态是否可供下游使用 | - | `FROZEN` | `FROZEN` | `FROZEN` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |
| `reason_codes` | 无效、降级或回退原因数组 | - | `PARTIAL` | `PARTIAL` | `PARTIAL` | `NOT FROZEN` | `MISSING` | `MISSING` | `PARTIAL` |

`reason_codes` 保持 `PARTIAL`，因为可信设计文档已经提出扩展候选原因码，而公共
Schema 和 Python 当前仍只包含基础枚举。本 PR 不把候选原因码伪装成已实现接口。

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

## 迁移规则

1. 项目负责人冻结字段名称、单位、枚举、失效行为和版本规则。
2. 模块负责同学在各自主责路径完成语言映射，不保留含糊兼容别名。
3. 旧数据只能在模块边界显式转换，不能污染当前公共结构。
4. 字段变更必须同步本矩阵、Mock、Schema、Python 类型和受影响测试。
5. MATLAB、C 和 App 未共同回放前，跨语言契约整体保持 `PARTIAL`。
6. 端到端通过只能由实际生产者、消费者和证据共同证明，不能由文档状态推断。
