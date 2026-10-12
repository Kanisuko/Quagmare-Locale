import argparse
import collections
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOKENS = re.compile(r"\\(?:[A-Za-z]+\[[^\]]*\]|[A-Za-z]+|[.!|^{}$><])|%\d+|\$\{[^}]*\}|<リアクション:[^>]*>|(?:if|en)\([^\n]*\)\s*$")
STATES = {"untranslated", "translated", "reviewed", "needs-review", "reference"}
LABELS = {
    "en": ("Translation Completeness", "Locale file", "Filled / total", "Filled", "Valid filled", "Reviewed", "Reviewed rate", "Needs review", "Empty", "Missing", "Invalid", "Extra IDs", "Snapshot of the locale files; the denominator is always the entry count in ja-JP.json", "Metric definitions"),
    "zh-CN": ("语言文件翻译完整性", "语言文件", "已填 / 总数", "填写率", "有效填写率", "已复核", "复核率", "待核实", "空白", "缺失", "异常", "多余 ID", "根据语言 JSON 生成；分母始终是 ja-JP.json 的条目数", "统计含义"),
    "ja-JP": ("言語ファイルの翻訳完成度", "言語ファイル", "入力済み / 総数", "入力率", "有効入力率", "確認済み", "確認率", "要確認", "空欄", "欠落", "異常", "余分な ID", "言語 JSON の集計です。分母は常に ja-JP.json の項目数です", "指標の説明"),
}
GUIDES = {
    "en": """- **Filled**: nonempty, non-whitespace translations divided by the reference entry count. **Deleting untranslated entries does not increase completeness**
- **Valid filled**: filled translations whose source, file, context, control codes, placeholders, line breaks and choice conditions match the reference
- **Reviewed rate**: valid entries marked `reviewed` divided by the total; `translated` and `needs-review` do not count as reviewed
- **Needs review**: filled entries marked `needs-review`
- **Invalid**: mismatched source/location or changed control codes, line breaks or conditions; malformed entries are also invalid
- **Extra IDs**: entries absent from the reference catalog
- The source reference shows N/A
""",
    "zh-CN": """- **填写率**：非空、非纯空白的译文数 ÷ 参考条目总数。**删掉未译条目不会提高完成度**
- **有效填写率**：已填且原文、文件位置、控制符、占位符、换行与选项条件匹配的条目数 ÷ 总数
- **复核率**：有效且状态为 `reviewed` 的条目数 ÷ 总数；`translated` 与 `needs-review` 不计入已复核
- **待核实**：已填但状态为 `needs-review`
- **异常**：原文/来源不匹配，或控制符、换行、条件改变；条目格式错误也计为异常
- **多余 ID**：参考目录之外的旧条目
- 原文参考显示 N/A
""",
    "ja-JP": """- **入力率**：空欄でも空白文字のみでもない訳文の件数 ÷ 原文の総項目数。**未翻訳の項目を削除しても完成度は上がりません**
- **有効入力率**：訳文が入力済みで、原文・ファイル・参照位置・制御文字・プレースホルダー・改行・選択肢の条件が原文と一致する項目の割合
- **確認率**：有効かつ `reviewed` の項目数 ÷ 総数。`translated` と `needs-review` は確認済みに含めません
- **要確認**：訳文が入力済みで `needs-review` の項目
- **異常**：原文・参照位置の不一致、制御文字・改行・条件の変更、または項目形式の誤り
- **余分な ID**：原文カタログに存在しない項目
- 原文参照は N/A と表示します
""",
}

def filename(base, language):
    return base + ("" if language == "en" else "." + language) + ".md"

def nav(base, language):
    return " | ".join("**" + label + "**" if code == language else "[" + label + "](./" + filename(base, code) + ")" for code, label in [("en", "English"), ("zh-CN", "简体中文"), ("ja-JP", "日本語")])

def escape(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;").replace("`", "&#96;").replace("\r", " ").replace("\n", " ")

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result

def decode(data):
    return json.loads(data.decode("utf-8-sig"), object_pairs_hook=unique)

def valid_catalog(doc):
    return isinstance(doc, dict) and doc.get("schemaVersion") == 1 and isinstance(doc.get("entries"), dict)

def metrics(reference, doc, path):
    if not valid_catalog(reference):
        raise ValueError("invalid reference catalog")
    if not valid_catalog(doc):
        raise ValueError("invalid locale catalog")
    originals, entries = reference["entries"], doc["entries"]
    n = len(originals)
    filled = valid = reviewed = pending = empty = invalid = 0
    is_reference = doc.get("locale") == doc.get("sourceLocale")
    for key, source in originals.items():
        if key not in entries:
            continue
        e = entries[key]
        if not isinstance(e, dict):
            invalid += 1
            continue
        text = e.get("translation")
        has_text = isinstance(text, str) and bool(text.strip())
        filled += has_text
        empty += not has_text
        pending += has_text and e.get("status") == "needs-review"
        okay = isinstance(source, dict) and all(isinstance(e.get(k), str) for k in ("file", "source", "translation", "status", "category", "notes"))
        okay = okay and isinstance(e.get("context"), list) and all(isinstance(c, str) for c in e["context"])
        okay = okay and e.get("status") in STATES and (e["status"] == "reference" if is_reference else e["status"] != "reference")
        okay = okay and all(e.get(k) == source.get(k) for k in ("source", "file", "context"))
        if okay:
            expected = "q_" + hashlib.sha256((e["file"] + "\0" + e["source"]).encode("utf-8")).hexdigest()
            okay = key == expected
        if okay and has_text:
            okay = collections.Counter(TOKENS.findall(e["source"])) == collections.Counter(TOKENS.findall(text)) and e["source"].count("\n") == text.count("\n")
        if is_reference:
            okay = okay and text == e.get("source")
        invalid += not okay
        valid += has_text and okay
        reviewed += has_text and okay and e.get("status") == "reviewed"
    return dict(path=path, total=n, filled=filled, valid=valid, reviewed=reviewed, pending=pending, empty=empty,
                missing=len(originals.keys() - entries.keys()), invalid=invalid, extra=len(entries.keys() - originals.keys()), reference=is_reference)

def read_rows(files, read):
    rows, errors = [], []
    for path in sorted(files):
        if not path.endswith(".json") or pathlib.PurePosixPath(path).name in {"schema.json", "romanization.json", "translation-progress.json"}:
            continue
        try:
            doc = decode(read(path))
            # Non-catalog JSON is not a locale file. Catalog-shaped malformed JSON is reported.
            if not isinstance(doc, dict) or not ({"entries", "locale", "schemaVersion"} & doc.keys()):
                continue
            parent = pathlib.PurePosixPath(path).parent
            refpath = str(parent / "ja-JP.json")
            reference = doc if path == refpath else decode(read(refpath))
            row = metrics(reference, doc, path)
            if doc.get("locale") != pathlib.PurePosixPath(path).stem or doc.get("sourceLocale") != "ja-JP":
                raise ValueError("locale metadata mismatch")
            rows.append(row)
        except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as ex:
            errors.append(path + ": " + str(ex))
    return rows, errors

def table(rows, errors, language):
    l = LABELS[language]
    output = "| " + " | ".join(l[1:12]) + " |\n| " + " | ".join(["---"] * 11) + " |\n"
    for r in rows:
        name = escape(r["path"])
        name = "[" + name + "](../../" + r["path"] + ")"
        if r["reference"]:
            cells = [name, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", str(r["empty"]), str(r["missing"]), str(r["invalid"]), str(r["extra"])]
        else:
            pct = lambda v: f"{100 * v / r['total']:.2f}%" if r["total"] else "0.00%"
            cells = [name, f"{r['filled']} / {r['total']}", pct(r["filled"]), pct(r["valid"]), str(r["reviewed"]), pct(r["reviewed"]), str(r["pending"]), str(r["empty"]), str(r["missing"]), str(r["invalid"]), str(r["extra"])]
        output += "| " + " | ".join(cells) + " |\n"
    for error in errors:
        output += "\n- Error: " + escape(error) + "\n"
    return output

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.PIPE)

def committed_rows():
    # Only the current commit is needed; never traverse or report commit history.
    files = git("ls-tree", "-r", "--name-only", "-z", "HEAD").decode("utf-8").rstrip("\0").split("\0")
    return read_rows(files, lambda path: git("show", "HEAD:" + path))

def write_reports(rows, errors, output=None):
    folder = output or ROOT / "docs" / "reports"
    folder.mkdir(parents=True, exist_ok=True)
    for language, l in LABELS.items():
        snapshot = f"# {l[0]}\n\n{nav('TranslationCompleteness', language)}\n\n{l[12]}\n\n"
        snapshot += table(rows, errors, language) + f"\n## {l[13]}\n\n" + GUIDES[language]
        (folder / filename("TranslationCompleteness", language)).write_text(snapshot, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--committed", action="store_true")
    options = parser.parse_args()
    if options.committed:
        rows, errors = committed_rows()
        write_reports(rows, errors)
    else:
        files = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.json") if ".git" not in p.relative_to(ROOT).parts]
        rows, errors = read_rows(files, lambda p: (ROOT / p).read_bytes())
        write_reports(rows, errors)
    print("Updated docs/reports in English, Simplified Chinese and Japanese")

if __name__ == "__main__":
    main()
