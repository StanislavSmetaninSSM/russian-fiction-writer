#!/usr/bin/env python3
"""Combine the folder skill into one UTF-8 Markdown attachment (stdlib only).

Usage: python scripts/build_chat_edition.py /path/outside/package/SKILL.md
No optional checker is embedded or executed. The source package is never edited.
"""

import argparse
import html
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


AUTHORED = ("notron-chronicle-writer", "notron-prose-examples")
SPECIALISTS = ("novel-writing", "dialogue", "prose-style", "novel-revision", "cliche-transcendence")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE = re.compile(r"(?P<code>(?P<ticks>`+).*?(?P=ticks))|(?P<link>\]\()(?P<url><[^>]+>|[^\s)]+)")
DEFINITION = re.compile(r"^( {0,3}\[[^]]+\]:\s*)(<[^>]+>|\S+)")


def frontmatter(text):
    """Separate initial YAML without interpreting or changing its fields."""
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "".join(lines[:index + 1]), "".join(lines[index + 1:])
        raise ValueError("Unclosed YAML frontmatter")
    return "", text


def prose_lines(text):
    """Identify fenced/indented code so its examples remain unchanged."""
    fence = None
    for line in text.splitlines(keepends=True):
        match = FENCE.match(line)
        if fence:
            yield line, False
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match:
            fence = match[1]
            yield line, False
        else:
            yield line, not line.startswith(("    ", "\t"))


def heading_slug(text):
    """Recognize the GitHub-style source fragments used by these manuals."""
    text = re.sub(r"\s+#+\s*$", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]*>", "", text)
    text = html.unescape(text).lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def build(root):
    """Read all required text first, then resolve local links to explicit anchors."""
    manuals = [root / "references/skills" / name / "SKILL.md" for name in (*AUTHORED, *SPECIALISTS)]
    references = [path for manual in manuals for path in sorted(manual.parent.rglob("*.md")) if path != manual]
    licenses = [root / "references/skills" / name / "LICENSE" for name in SPECIALISTS]
    paths = [root / "SKILL.md", *manuals, *references, *licenses]
    documents = {path: frontmatter(path.read_text(encoding="utf-8")) for path in paths}
    if not documents[paths[0]][0]:
        raise ValueError("Root SKILL.md must begin with its original frontmatter")
    file_ids = {path: f"file-{index + 1:02d}" for index, path in enumerate(paths)}
    heading_ids = {}
    line_ids = {}
    for path, (_, body) in documents.items():
        used = set()
        number = 0
        for index, (line, prose) in enumerate(prose_lines(body)):
            match = HEADING.match(line) if prose else None
            if match:
                number += 1
                slug = base = heading_slug(match[1])
                duplicate = 0
                while slug in used:
                    duplicate += 1
                    slug = f"{base}-{duplicate}"
                used.add(slug)
                anchor = f"{file_ids[path]}-heading-{number:02d}"
                heading_ids[path, slug] = anchor
                line_ids[path, index] = anchor

    targets = set()

    def destination(source, target):
        bare = target[1:-1] if target.startswith("<") else target
        url = urlsplit(bare)
        if url.scheme or url.netloc:
            return target
        path = (source.parent / unquote(url.path)).resolve() if url.path else source
        if path not in file_ids or url.query:
            raise ValueError(f"{source.relative_to(root)}: link is not embedded: {bare}")
        fragment = unquote(url.fragment)
        if fragment:
            anchor = heading_ids.get((path, fragment))
            if anchor is None:
                raise ValueError(f"{source.relative_to(root)}: unknown heading: {bare}")
        else:
            anchor = file_ids[path]
        targets.add(anchor)
        return f"#{anchor}"

    # Resolve every link before writing so forward targets are known and errors
    # cannot leave a partially assembled attachment.
    rewritten = {}
    for path, (_, body) in documents.items():
        lines = []
        for line, prose in prose_lines(body):
            if prose and path not in licenses:
                definition = DEFINITION.match(line)
                if definition:
                    start, end = definition.span(2)
                    line = line[:start] + destination(path, definition[2]) + line[end:]
                else:
                    line = INLINE.sub(lambda match: match[0] if match["code"] else match["link"] + destination(path, match["url"]), line)
            lines.append(line)
        rewritten[path] = lines

    notice = (
        "\n## Как читать приложенную редакцию\n\n"
        "Это единый файл для чата без доступа к папке или сети: основная инструкция, "
        "два авторских руководства, пять скиллов специалистов и их справочные тексты. "
        "Выбирай их по задаче, как указано в основной инструкции. Ссылки на файлы "
        "пакета ведут к разделам здесь; YAML в блоках кода хранит сведения об "
        "исходных скиллах.\n\n"
        "Необязательные скрипты сюда не включены. Команды в руководствах относятся "
        "к полной папочной версии и запускаются из папки соответствующего скилла. "
        "В чате выполняй проверки по тексту, а результат выдай сообщением, если "
        "сохранение файлов недоступно.\n"
    )
    output = [documents[paths[0]][0], notice]
    for path, (metadata, body) in documents.items():
        output.append(f"\n<!-- Source: {path.relative_to(root).as_posix()} -->\n\n")
        if file_ids[path] in targets:
            output.append(f'<a id="{file_ids[path]}"></a>\n\n')
        if metadata and path != paths[0]:
            output.append("```yaml\n" + "".join(metadata.splitlines(keepends=True)[1:-1]) + "```\n\n")
        if path in licenses:
            output.append(f"## MIT notice: {path.parent.name}\n\n```text\n{body.rstrip()}\n```\n")
            continue
        for index, line in enumerate(rewritten[path]):
            anchor = line_ids.get((path, index))
            if anchor in targets:
                output.append(f'<a id="{anchor}"></a>\n\n')
            output.append(line)
        output.append("\n")
    return "".join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="UTF-8 .md attachment destination outside this package")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output = args.output.resolve()
    if output == root or root in output.parents:
        parser.error("output must be outside the source package")
    if output.suffix.lower() != ".md":
        parser.error("output must have a .md extension")
    try:
        combined = build(root)
        output.write_text(combined, encoding="utf-8", newline="\n")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Wrote {output} ({len(combined.encode('utf-8')):,} UTF-8 bytes)")


if __name__ == "__main__":
    main()
