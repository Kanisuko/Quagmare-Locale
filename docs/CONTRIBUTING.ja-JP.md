# コントリビューションガイド

[English](./CONTRIBUTING.md) | [简体中文](./CONTRIBUTING.zh-CN.md) | **日本語**

このリポジトリでは Quagmare v0.15_h のテキスト翻訳を管理します

## 既存の言語ファイルを編集する

1. `ja-JP.json` を原文として参照し、翻訳先の言語ファイルの `entries` にある `translation` を編集します（Translator++ 形式に変換してから翻訳することをおすすめします）
2. 項目の ID、`source`、`file`、`context` は変更しないでください
3. 新しい訳文は `translated`、文脈を確認した訳文は `reviewed` にします。原文に疑問がある場合は `needs-review` を使用できます
4. 制御文字、改行、プレースホルダー、選択肢の条件を保持してください。[翻訳上の注意](./TranslationNotes.ja-JP.md)を参照してください
5. GitHub のユーザー名を `contributors` に追加し、README の言語一覧にも翻訳者として記載してください
