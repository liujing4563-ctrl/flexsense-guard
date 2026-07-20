# 贡献指南

## 分支与 Pull Request

- 不直接向 `main` 推送；每项工作使用一个短生命周期分支和一个 PR。
- 分支格式：`chore/`、`feat/`、`fix/`、`docs/` 或 `probe/` 加简短说明。
- PR 默认以 Draft 创建，描述变更范围、已执行检查、未执行检查和风险。
- 未经人工审查不要合并；不使用自动合并，也不维护长期 `develop` 分支。

## 提交与验证

- 使用 Conventional Commits，例如 `docs: establish repository baseline`。
- 只暂存本 PR 的文件；不要混入生成结果或无关格式化。
- Python 改动至少运行 `python -m pytest python/tests -q`。
- MATLAB/Octave、C/SIL 未运行时，必须在 PR 中明确标为“未运行”。

## 术语与边界

- 对外扰动仅使用力矩字段 `estimated_external_torque_nm`。
- `confidence_score` 与 `contact_score` 都不是概率。
- 负载侧真值只能用于评估；不得接入观测器。
