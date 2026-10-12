# Translation Completeness

**English** | [简体中文](./TranslationCompleteness.zh-CN.md) | [日本語](./TranslationCompleteness.ja-JP.md)

Snapshot of the locale files; the denominator is always the entry count in ja-JP.json

| Locale file | Filled / total | Filled | Valid filled | Reviewed | Reviewed rate | Needs review | Empty | Missing | Invalid | Extra IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ja-JP.json](../../ja-JP.json) | N/A | N/A | N/A | N/A | N/A | N/A | 0 | 0 | 0 | 0 |
| [zh-CN.json](../../zh-CN.json) | 11050 / 11050 | 100.00% | 100.00% | 10256 | 92.81% | 25 | 0 | 0 | 0 | 0 |

## Metric definitions

- **Filled**: nonempty, non-whitespace translations divided by the reference entry count. **Deleting untranslated entries does not increase completeness**
- **Valid filled**: filled translations whose source, file, context, control codes, placeholders, line breaks and choice conditions match the reference
- **Reviewed rate**: valid entries marked `reviewed` divided by the total; `translated` and `needs-review` do not count as reviewed
- **Needs review**: filled entries marked `needs-review`
- **Invalid**: mismatched source/location or changed control codes, line breaks or conditions; malformed entries are also invalid
- **Extra IDs**: entries absent from the reference catalog
- The source reference shows N/A
