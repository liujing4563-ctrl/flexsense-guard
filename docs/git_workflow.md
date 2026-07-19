# Git 工作流

`main` 只接收经人工审查的 PR。每个阶段建立一个短生命周期分支和一个 Draft PR：

| 阶段 | 建议分支 |
|---|---|
| PR-0 | `chore/repository-baseline` |
| PR-1 | `feat/dual-inertia-plant` |
| PR-2 | `feat/baseline-observer` |
| PR-3 | `probe/confidence-trigger` |
| PR-4 | `feat/classification-control` |
| PR-5 | `feat/sil-app-test-agent` |
| PR-6 | `docs/experiment-material-freeze` |

每个 PR 必须说明范围、非目标、验证和未运行检查。禁止自动合并和长期 `develop`
分支；探针失败时先记录降级决定，再决定下一分支。
