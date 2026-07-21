# 阶段验收矩阵

## 决策规则

- `PASS`：证据有效、充分、可复现，并满足全部强制门禁；
- `FAIL`：证据有效，但至少一个强制性能门禁失败；
- `NOT_VERIFIED`：模型、输入、实验设计或证据无效/不足；
- 阶段状态不得由单张曲线、单一 seed 或未运行命令决定。

## 验收矩阵

| 阶段 | 验证问题 | 强制输入 | 强制证据 | 负责同学 | 当前状态 | 后续影响 |
|---|---|---|---|---|---|---|
| P1 | 仅凭电机侧测量能否稳定估计负载侧状态 | 冻结模型、三类力矩、三负载、seed 0-9、独立 Plant/Observer 参数 | MATLAB 主链路、baseline/EKF 公平比较、位置与速度指标、能量检查、完整失败案例 | Simulink 同学执行，项目负责人审查 | `NOT_VERIFIED` | 未 `PASS` 时阻断 P2/P3 |
| P2 | 能否区分正常、柔性振动和外部接触 | 有效 P1 输出、冻结场景、无泄漏数据划分 | 受控场景、规则 baseline、多 seed、误报/漏报/延迟、泛化结果 | 深度学习通感算同学执行，项目负责人审查 | `BLOCKED` | 失败时进入 B 路线 |
| P3 | 可信评分能否识别估计失效并安全降级 | 有效 P1，必要时有效 P2，冻结故障矩阵 | 信号故障、参数失配、模型外工况、可信变化、原因码、模式切换和恢复 | 项目负责人主责规则，相关同学执行模块实验 | `BLOCKED` | 失败时不得主张可信安全闭环 |
| 集成 | 各语言和模块能否按同一契约运行 | 已通过的前置阶段、版本化配置 | MATLAB/Python/C/App 回放、Schema、资源、报告和演示记录 | 项目负责人集成，各模块同学签字 | `BLOCKED` | 决定最终交付范围 |

## P1 证据有效性前置条件

1. 力矩所在侧、齿轮方向和符号已共同确认；
2. Plant 使用 `motor_torque_applied_nm`；Observer 使用
   `motor_torque_measured_nm`，且逐样本可追溯；
3. 无耗散模型通过能量一致性检查；
4. light、medium、heavy 与 seed 0 到 9 均纳入汇总；
5. 调试集和最终评价集分离，不用测试真值选择 Q/R/P；
6. 历史失败、NaN、Inf 和发散案例完整保留；
7. 结果关联配置、提交、环境、命令和原始证据。

任一前置条件不满足，P1 当前结论只能是 `NOT_VERIFIED`，不能据此选择 C 路线。

## 当前正式状态

```text
Historical P1 execution result: FAIL
Evidence validity: INVALID / INSUFFICIENT
Current P1 feasibility decision: NOT_VERIFIED
P2: BLOCKED
P3: BLOCKED
```
