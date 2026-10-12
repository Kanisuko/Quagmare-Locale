# Contribution Guidelines

**English** | [简体中文](./CONTRIBUTING.zh-CN.md) | [日本語](./CONTRIBUTING.ja-JP.md)

This repository maintains the text translations for Quagmare v0.15_h

## Editing an existing locale

1. Use `ja-JP.json` as the reference and edit `translation` under `entries` in the target locale file (converting to Translator++ before translating is recommended)
2. Keep entry IDs, `source`, `file` and `context` unchanged
3. Mark new translations as `translated`; after checking them in context, mark them as `reviewed`. Use `needs-review` when the source is uncertain
4. Preserve control codes, line breaks, placeholders and choice conditions; see [Translation Notes](./TranslationNotes.md)
5. Add your GitHub username to `contributors` and list yourself in the README locale table
