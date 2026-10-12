# Translation Notes

**English** | [简体中文](./TranslationNotes.zh-CN.md) | [日本語](./TranslationNotes.ja-JP.md)

1. Interpret the source using `file`, `context`, the surrounding dialogue and the character's tone
2. Avoid adding content absent from the original unless necessary
3. **Strongly recommended:** use consistent romaji for character names, such as Purei, Rahabu, Meo and Doba

## Special characters to preserve

- Dynamic placeholders such as `%1`, `%2`, `%3` and `${...}`
- Control codes and their arguments, such as `\n[1]`, `\V[1]`, `\I[1]`, `\C[0]`, `\MP[...]` and `\MPD[...]`
- Actual line breaks and JSON escaping
- Complete Japanese identifiers inside `<リアクション: ...>`, and `if(...)` / `en(...)` conditions at the end of choices
- Numbers, multipliers, turn durations, target ranges, IDs and script logic

## Statuses and issues in the original

`untranslated` means untranslated; `translated` means translated but not yet reviewed; `reviewed` means reviewed; `needs-review` means verification is needed; `reference` is only for the source catalog (you can mark a translation as reviewed directly, but if possible, at least have AI help check it once)
