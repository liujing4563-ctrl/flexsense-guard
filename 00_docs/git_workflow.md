# Git Workflow

## 分支策略

采用简化 Trunk-Based Development：

```
main  ← 生产就绪状态
  └── chore/*       仓库初始化、CI 配置等基础设施变更
  └── feat/*        新功能开发
  └── fix/*         Bug 修复
  └── docs/*        文档变更
  └── probe/*       可行性探针开发
```

### 规则

1. **main 分支受保护**：不允许直接推送。所有变更通过 Pull Request 合并。
2. **分支命名**：`<type>/<short-description>`，如 `feat/ekf-tuning`、`fix/observer-initialization`
3. **PR 合入**：使用 Squash Merge 保持 main 历史整洁。
4. **长期分支**：不允许存在长期 `develop` 分支。所有分支生命周期不超过一周。

## Commit 规范

使用 Conventional Commits 格式：

```
<type>: <简短描述>

<可选正文>
```

### Type 类型

| Type | 用途 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| chore | 基础设施、构建、配置 |
| refactor | 重构 |
| test | 测试相关 |
| ci | CI/CD 变更 |
| style | 格式调整（不影响逻辑） |

### 示例

```
feat: add augmented EKF observer step function
fix: correct sign error in torsion spring model
docs: update interface specification for SystemState
chore: initialize CMake build system for SIL
test: add smoke test for observer initialization
```

## Pull Request 规范

1. PR 标题使用 Conventional Commits 格式
2. PR 正文必须包含：
   - 变更内容摘要
   - 如何验证
   - 已通过/未通过的测试
   - 如果相关，附上仿真实例截图或数据
3. PR 审查由至少一位其他同学完成
4. 所有 CI 检查通过后才可合并

## Issue 管理

- 每个 Issue 标注优先级（P0/P1/P2）和类型标签
- P0：阻塞性，必须优先解决
- P1：重要但不阻塞
- P2：锦上添花

## 首次提交

本项目首次初始化直接提交到 `chore/project-bootstrap` 分支，创建 Pull Request 合并到 `main`。后续所有开发遵循上述规范。
