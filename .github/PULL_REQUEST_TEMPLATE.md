## 变更摘要

<!-- 说明本 PR 只解决的一个阶段性问题。 -->

## 边界检查

- [ ] 未引入 `contact_probability`
- [ ] 未将外力写为终端力；外扰输出为 `estimated_external_torque_nm`
- [ ] 未将负载侧真值作为观测器输入
- [ ] 未加入公开仓库不应包含的材料

## 验证

- [ ] `python -m pytest python/tests -q`
- [ ] MATLAB/Octave：未运行 / 已运行（说明结果）
- [ ] C/SIL：未运行 / 已运行（说明结果）

## 风险与后续

<!-- 记录已知限制、降级路径或后续 Issue。 -->
