# 贡献指南

[English](./CONTRIBUTING.md) | **简体中文** | [日本語](./CONTRIBUTING.ja-JP.md)

本仓库用于维护 Quagmare v0.15_h 的文本翻译内容

## 修改现有语言

1. 以 `ja-JP.json` 为蓝本，在对应语言文件中编辑 `entries` 下的 `translation` （建议转换为Translator++格式后翻译）
2. 保持条目 ID、`source`、`file` 和 `context` 不变
3. 新译文标记 `translated`；结合上下文复核后标记 `reviewed`。原文有疑点时可以使用 `needs-review`
4. 保留控制符、换行、占位符和选项条件，参见[翻译注意事项](./TranslationNotes.zh-CN.md)
5. 将自己的 GitHub 用户名加入 `contributors`，并在 README 语言表注明贡献者
