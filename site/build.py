#!/usr/bin/env python3
"""Build the Crimson Sequence reading site from fanfic/chapters/*.md into docs/."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "fanfic" / "chapters"
OUT_DIR = ROOT / "docs"

SITE_TITLE = "Crimson Sequence"
TAGLINE = "A Soul Land story — the climb of the ninth Sequence"
ABOUT = (
    "At six-year-old Huo Yuan's awakening, his martial soul manifests as a faceless "
    "priest in wound-red robes — and the crystal beneath his hand reads zero. Spirit "
    "Hall files him as a powerless freak: an idol soul with nothing in it. But the "
    "figure is no martial soul. It is the Vestige — the shadow of a dead war god's "
    "shattered seat, cast through his flesh — and the power to fill that shadow must "
    "be climbed one dangerous role at a time, from Hunter to Red Priest. To finish "
    "the climb he must out-hunt the cult that murdered his father, out-scheme Spirit "
    "Hall, and out-act the madness that consumed every climber before him."
)

CSS = """
:root {
  --bg: #faf6ef; --fg: #2b2620; --muted: #8a7f70; --accent: #a32c2c;
  --rule: #e3dccd; --card: #fffdf8;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16130f; --fg: #ddd5c7; --muted: #8a8071; --accent: #e06c5a;
    --rule: #2e2820; --card: #1d1914;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: Georgia, "Songti SC", "Noto Serif", serif;
  line-height: 1.75; font-size: 1.075rem;
}
main { max-width: 41rem; margin: 0 auto; padding: 2.5rem 1.25rem 5rem; }
h1 { font-size: 1.65rem; line-height: 1.3; margin: 0.25rem 0 0.25rem; }
h1.site { font-size: 2.2rem; letter-spacing: 0.02em; }
.subtitle, .meta { color: var(--muted); font-style: italic; margin: 0 0 1.5rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2.25rem auto; width: 60%; }
p { margin: 0 0 1.1em; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.crumb { font-size: 0.9rem; color: var(--muted); margin-bottom: 2rem; display: block; }
nav.pager {
  display: flex; justify-content: space-between; gap: 1rem;
  border-top: 1px solid var(--rule); margin-top: 3rem; padding-top: 1.25rem;
  font-size: 0.95rem;
}
nav.pager span { color: var(--muted); }
ol.toc { list-style: none; padding: 0; margin: 0; }
ol.toc li {
  background: var(--card); border: 1px solid var(--rule); border-radius: 8px;
  margin: 0 0 0.6rem; transition: border-color 0.15s;
}
ol.toc li:hover { border-color: var(--accent); }
ol.toc a { display: block; padding: 0.8rem 1.1rem; color: var(--fg); }
ol.toc a:hover { text-decoration: none; }
ol.toc .num { color: var(--accent); font-weight: bold; margin-right: 0.6rem; }
ol.toc .sub { display: block; font-size: 0.85rem; color: var(--muted); font-style: italic; }
.about { border-left: 3px solid var(--accent); padding-left: 1rem; color: var(--muted); }
.volume { margin: 2rem 0 0.75rem; font-size: 0.85rem; text-transform: uppercase;
  letter-spacing: 0.15em; color: var(--muted); }
footer { margin-top: 4rem; font-size: 0.85rem; color: var(--muted); text-align: center; }
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<main>
{body}
<footer>{site_title} · a Soul Land fanfiction</footer>
</main>
</body>
</html>
"""


def md_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def md_body(md: str) -> str:
    """Convert the chapters' simple markdown (paragraphs, --- rules) to HTML.
    The title line (# ...) and the first *subtitle* line are handled by the caller."""
    out, para = [], []

    def flush():
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para.clear()

    for line in md.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
        elif stripped == "---":
            flush()
            out.append("<hr>")
        elif stripped.startswith("#"):
            flush()
            level = min(len(stripped) - len(stripped.lstrip("#")), 6)
            out.append(f"<h{level}>{md_inline(stripped.lstrip('#').strip())}</h{level}>")
        else:
            para.append(stripped)
    flush()
    return "\n".join(out)


def parse_chapter(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    title, subtitle, body_start = path.stem, "", 0
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            continue
        if s.startswith("# ") and not title.startswith("Chapter"):
            title = s[2:].strip()
            body_start = i + 1
            continue
        if s.startswith("*") and s.endswith("*") and not subtitle:
            subtitle = s.strip("*").strip()
            body_start = i + 1
            continue
        break
    body = "\n".join(lines[body_start:])
    body = re.sub(r"^\s*---\s*\n", "", body, count=1)  # drop the rule under the header
    return title, subtitle, body


def main():
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / ".nojekyll").write_text("")

    chapters = []
    for path in sorted(CHAPTERS_DIR.glob("ch*.md")):
        num = int(re.search(r"\d+", path.stem).group())
        title, subtitle, body = parse_chapter(path)
        chapters.append((num, title, subtitle, body, f"chapter-{num:03d}.html"))

    for idx, (num, title, subtitle, body, fname) in enumerate(chapters):
        prev_link = (
            f'<a href="{chapters[idx-1][4]}">&larr; {chapters[idx-1][1]}</a>'
            if idx > 0 else "<span></span>"
        )
        next_link = (
            f'<a href="{chapters[idx+1][4]}">{chapters[idx+1][1]} &rarr;</a>'
            if idx + 1 < len(chapters) else "<span>End of posted chapters</span>"
        )
        page_body = (
            f'<a class="crumb" href="index.html">&larr; {SITE_TITLE}</a>\n'
            f"<h1>{md_inline(title)}</h1>\n"
            f'<p class="subtitle">{md_inline(subtitle)}</p>\n'
            f"{md_body(body)}\n"
            f'<nav class="pager">{prev_link}{next_link}</nav>'
        )
        (OUT_DIR / fname).write_text(
            PAGE.format(title=f"{title} · {SITE_TITLE}", css=CSS,
                        body=page_body, site_title=SITE_TITLE),
            encoding="utf-8",
        )

    items = []
    for num, title, subtitle, _, fname in chapters:
        short = title.split("—", 1)[-1].strip()
        items.append(
            f'<li><a href="{fname}"><span class="num">{num}</span>{md_inline(short)}'
            f'<span class="sub">{md_inline(subtitle)}</span></a></li>'
        )
    index_body = (
        f'<h1 class="site">{SITE_TITLE}</h1>\n'
        f'<p class="subtitle">{TAGLINE}</p>\n'
        f'<p class="about">{ABOUT}</p>\n'
        f'<p class="meta">Soul Land / Douluo Dalu AU · power system inspired by the '
        f"Red Priest pathway from <em>Lord of the Mysteries</em> · rated T (violence, "
        f"character death) · updates serially · {len(chapters)} chapters posted</p>\n"
        f'<div class="volume">Volume 1 — Hunter</div>\n'
        f'<ol class="toc">{"".join(items)}</ol>'
    )
    (OUT_DIR / "index.html").write_text(
        PAGE.format(title=SITE_TITLE, css=CSS, body=index_body, site_title=SITE_TITLE),
        encoding="utf-8",
    )
    print(f"Built {len(chapters)} chapters -> {OUT_DIR}")


if __name__ == "__main__":
    main()
