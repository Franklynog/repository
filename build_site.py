#!/usr/bin/env python3
"""
build_site.py — Generate a static, offline-capable reading website for
*Crucible of the Crimson God* from the Markdown chapters in ./chapters.

No third-party dependencies. Re-run any time after adding/editing chapters:

    python3 build_site.py

Output goes to ./docs (open docs/index.html directly, or host via GitHub Pages).
"""

from __future__ import annotations

import html
import re
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS_DIR = ROOT / "chapters"
OUT_DIR = ROOT / "docs"
ASSETS_DIR = OUT_DIR / "assets"

SITE_TITLE = "Crucible of the Crimson God"
SITE_SUBTITLE = "A Soul Land fanfiction"

# --------------------------------------------------------------------------- #
# Minimal, dependency-free Markdown -> HTML for the subset used by the chapters:
#   #/##/### headings, --- horizontal rules, **bold**, *italic*, paragraphs.
# --------------------------------------------------------------------------- #

def _inline(text: str) -> str:
    """Convert inline markdown (escaped first) to HTML."""
    text = html.escape(text, quote=False)
    # bold before italic so ** isn't eaten by the single-* pass
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    # tasteful typography
    text = text.replace("--", "&mdash;") if "—" not in text else text
    return text


def parse_chapter(md: str):
    """Return (title, meta_html, body_html) for one chapter's markdown."""
    lines = md.split("\n")
    title = "Untitled"
    meta_html = ""
    body_lines: list[str] = []

    # Pull the H1 title and the first fully-italic metadata line out of the body.
    consumed_title = False
    consumed_meta = False
    for ln in lines:
        stripped = ln.strip()
        if not consumed_title and stripped.startswith("# "):
            title = stripped[2:].strip()
            consumed_title = True
            continue
        if (
            not consumed_meta
            and consumed_title
            and stripped.startswith("*")
            and stripped.endswith("*")
            and "·" in stripped
        ):
            meta_html = _inline(stripped.strip("*").strip())
            consumed_meta = True
            continue
        body_lines.append(ln)

    body_html = render_blocks(body_lines)
    return title, meta_html, body_html


def render_blocks(lines: list[str]) -> str:
    """Group lines into block elements separated by blank lines."""
    html_parts: list[str] = []
    buf: list[str] = []

    def flush():
        if not buf:
            return
        block = [b for b in buf if b.strip() != ""]
        buf.clear()
        if not block:
            return
        first = block[0].strip()
        if first == "---":
            html_parts.append('<hr class="scene-break" />')
            return
        if first.startswith("### "):
            html_parts.append(f"<h3>{_inline(first[4:].strip())}</h3>")
            return
        if first.startswith("## "):
            html_parts.append(f"<h2>{_inline(first[3:].strip())}</h2>")
            return
        if first.startswith("# "):
            html_parts.append(f"<h1>{_inline(first[2:].strip())}</h1>")
            return
        # paragraph: join wrapped lines with a space
        para = " ".join(s.strip() for s in block)
        html_parts.append(f"<p>{_inline(para)}</p>")

    for ln in lines:
        if ln.strip() == "":
            flush()
        elif ln.strip() == "---":
            flush()
            buf.append("---")
            flush()
        else:
            buf.append(ln)
    flush()
    return "\n".join(html_parts)


# --------------------------------------------------------------------------- #
# HTML templates
# --------------------------------------------------------------------------- #

def page_shell(title: str, body: str, *, rel: str = "", extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="sepia">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="stylesheet" href="{rel}assets/style.css" />
{extra_head}
</head>
<body>
<div id="progress"><div id="progress-bar"></div></div>
{body}
<script src="{rel}assets/reader.js"></script>
</body>
</html>
"""


def reader_toolbar(rel: str) -> str:
    return f"""
<div class="toolbar">
  <a class="tb-btn home" href="{rel}index.html" title="Contents (Esc)">☰ Contents</a>
  <div class="tb-spacer"></div>
  <button class="tb-btn" data-action="font-dec" title="Smaller text">A−</button>
  <button class="tb-btn" data-action="font-inc" title="Larger text">A+</button>
  <button class="tb-btn" data-action="theme" title="Toggle theme (T)">◑ Theme</button>
</div>
"""


def build_index(chapters: list[dict]) -> str:
    items = []
    for i, ch in enumerate(chapters, 1):
        meta = f'<span class="toc-meta">{ch["meta"]}</span>' if ch["meta"] else ""
        items.append(
            f'<li><a href="{ch["slug"]}.html">'
            f'<span class="toc-num">{i:02d}</span>'
            f'<span class="toc-text"><span class="toc-title">{html.escape(ch["title"])}</span>'
            f"{meta}</span></a></li>"
        )
    toc = "\n".join(items)
    total_words = sum(ch["words"] for ch in chapters)
    body = f"""
{reader_toolbar("")}
<main class="cover">
  <header class="cover-head">
    <p class="kicker">{html.escape(SITE_SUBTITLE)}</p>
    <h1 class="cover-title">{html.escape(SITE_TITLE)}</h1>
    <p class="cover-blurb">A man from our world is reborn on the Douluo Continent
      with a martial soul shaped from the Red&nbsp;Priest pathway&mdash;war, fire,
      plunder, and blood&mdash;stripped of the madness that should have been its
      price. He pays no cost for power. Everything around him does.</p>
    <p class="cover-stats">{len(chapters)} chapters &middot; {total_words:,} words &middot; updated continually</p>
    <p class="cover-cta"><a class="start-btn" href="{chapters[0]['slug']}.html">Start reading →</a></p>
  </header>
  <nav class="toc">
    <h2>Contents</h2>
    <ol class="toc-list">
      {toc}
    </ol>
  </nav>
  <footer class="cover-foot">
    <p>Tags: ruthless protagonist &middot; transmigration &middot; original power system &middot; war &amp; conquest.
       Mature: graphic violence, dark themes. The narrative observes its protagonist; it does not endorse him.</p>
  </footer>
</main>
"""
    return page_shell(f"{SITE_TITLE} — Contents", body, rel="")


def build_chapter_page(ch: dict, prev_ch, next_ch, index_num: int, total: int) -> str:
    prev_link = f'<a class="nav-prev" href="{prev_ch["slug"]}.html" data-key="prev">← Previous</a>' if prev_ch else '<span class="nav-prev disabled">← Previous</span>'
    next_link = f'<a class="nav-next" href="{next_ch["slug"]}.html" data-key="next">Next →</a>' if next_ch else '<span class="nav-next disabled">Finis</span>'
    meta = f'<p class="ch-meta">{ch["meta"]}</p>' if ch["meta"] else ""

    body = f"""
{reader_toolbar("")}
<article class="chapter" data-prev="{prev_ch['slug'] + '.html' if prev_ch else ''}" data-next="{next_ch['slug'] + '.html' if next_ch else ''}">
  <header class="ch-head">
    <p class="ch-counter">Chapter {index_num} of {total}</p>
    <h1 class="ch-title">{html.escape(ch["title"])}</h1>
    {meta}
  </header>
  <div class="ch-body">
    {ch["body"]}
  </div>
  <nav class="ch-nav">
    {prev_link}
    <a class="nav-home" href="index.html">Contents</a>
    {next_link}
  </nav>
</article>
"""
    return page_shell(f'{ch["title"]} — {SITE_TITLE}', body, rel="")


# --------------------------------------------------------------------------- #
# Assets
# --------------------------------------------------------------------------- #

CSS = r"""
:root{
  --maxw: 42rem;
  --fs: 1.18rem;
  --lh: 1.75;
  --font-body: "Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,"Times New Roman",serif;
  --font-ui: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
html[data-theme="light"]{ --bg:#faf9f7; --fg:#1d1b18; --muted:#6b6258; --rule:#e0d8cc; --accent:#9a2c1f; --card:#ffffff; --shadow:rgba(0,0,0,.06); }
html[data-theme="sepia"]{ --bg:#f4ecd8; --fg:#3b3122; --muted:#7a6a4f; --rule:#ddccab; --accent:#9a2c1f; --card:#fbf5e6; --shadow:rgba(80,60,20,.10); }
html[data-theme="dark"]{ --bg:#15130f; --fg:#e7ddca; --muted:#a2937a; --rule:#332c20; --accent:#e0613f; --card:#1d1a14; --shadow:rgba(0,0,0,.5); }

*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; }
body{
  background:var(--bg); color:var(--fg);
  font-family:var(--font-body);
  font-size:var(--fs); line-height:var(--lh);
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
  transition:background .3s ease,color .3s ease;
}

/* progress bar */
#progress{ position:fixed; top:0; left:0; right:0; height:3px; background:transparent; z-index:50; }
#progress-bar{ height:100%; width:0; background:var(--accent); transition:width .1s linear; }

/* toolbar */
.toolbar{
  position:sticky; top:0; z-index:40;
  display:flex; align-items:center; gap:.4rem;
  padding:.5rem clamp(.8rem,4vw,1.5rem);
  background:color-mix(in srgb,var(--bg) 86%, transparent);
  backdrop-filter:saturate(140%) blur(8px);
  border-bottom:1px solid var(--rule);
  font-family:var(--font-ui);
}
.tb-spacer{ flex:1; }
.tb-btn{
  font-family:var(--font-ui); font-size:.82rem; font-weight:600;
  color:var(--muted); background:transparent; border:1px solid var(--rule);
  border-radius:.5rem; padding:.32rem .6rem; cursor:pointer; text-decoration:none;
  transition:all .15s ease; white-space:nowrap;
}
.tb-btn:hover{ color:var(--fg); border-color:var(--accent); }
.tb-btn.home{ border-color:transparent; }

/* cover / index */
.cover{ max-width:var(--maxw); margin:0 auto; padding:clamp(1.5rem,6vw,4rem) clamp(1rem,5vw,1.5rem) 4rem; }
.cover-head{ text-align:center; border-bottom:1px solid var(--rule); padding-bottom:2rem; margin-bottom:2rem; }
.kicker{ font-family:var(--font-ui); text-transform:uppercase; letter-spacing:.22em; font-size:.72rem; color:var(--accent); margin:.2rem 0 .6rem; }
.cover-title{ font-size:clamp(2.2rem,8vw,3.4rem); line-height:1.05; margin:.2rem 0 1rem; font-weight:700; letter-spacing:-.01em; }
.cover-blurb{ color:var(--fg); font-size:1.05rem; max-width:34rem; margin:0 auto 1.2rem; }
.cover-stats{ font-family:var(--font-ui); font-size:.8rem; color:var(--muted); letter-spacing:.03em; margin:.4rem 0 1.4rem; }
.start-btn{
  display:inline-block; font-family:var(--font-ui); font-weight:700; font-size:.95rem;
  background:var(--accent); color:#fff; text-decoration:none;
  padding:.7rem 1.4rem; border-radius:.6rem; box-shadow:0 2px 10px var(--shadow);
  transition:transform .12s ease, filter .12s ease;
}
.start-btn:hover{ transform:translateY(-1px); filter:brightness(1.05); }

.toc h2{ font-family:var(--font-ui); font-size:.78rem; text-transform:uppercase; letter-spacing:.18em; color:var(--muted); margin:0 0 .8rem; }
.toc-list{ list-style:none; margin:0; padding:0; counter-reset:none; }
.toc-list li{ margin:0; }
.toc-list a{
  display:flex; gap:1rem; align-items:baseline; text-decoration:none; color:inherit;
  padding:.8rem .8rem; border-radius:.6rem; border:1px solid transparent;
  transition:background .15s ease, border-color .15s ease;
}
.toc-list a:hover{ background:var(--card); border-color:var(--rule); }
.toc-num{ font-family:var(--font-ui); font-size:.85rem; font-weight:700; color:var(--accent); min-width:2ch; }
.toc-text{ display:flex; flex-direction:column; gap:.15rem; }
.toc-title{ font-size:1.12rem; font-weight:600; }
.toc-meta{ font-family:var(--font-ui); font-size:.74rem; color:var(--muted); line-height:1.4; }
.cover-foot{ margin-top:2.5rem; padding-top:1.4rem; border-top:1px solid var(--rule); }
.cover-foot p{ font-family:var(--font-ui); font-size:.74rem; color:var(--muted); text-align:center; }

/* chapter */
.chapter{ max-width:var(--maxw); margin:0 auto; padding:clamp(1.2rem,5vw,2.5rem) clamp(1rem,5vw,1.5rem) 5rem; }
.ch-head{ text-align:center; margin:1rem 0 2.4rem; }
.ch-counter{ font-family:var(--font-ui); text-transform:uppercase; letter-spacing:.2em; font-size:.7rem; color:var(--accent); margin:0 0 .6rem; }
.ch-title{ font-size:clamp(1.7rem,6vw,2.4rem); line-height:1.1; margin:.2rem 0 .8rem; font-weight:700; }
.ch-meta{ font-family:var(--font-ui); font-size:.78rem; color:var(--muted); font-style:normal; line-height:1.5; max-width:30rem; margin:0 auto; }

.ch-body{ }
.ch-body p{ margin:0 0 1.15rem; text-align:left; hyphens:auto; }
.ch-body p:first-of-type{ }
/* drop-cap on the first paragraph after the header */
.ch-body > p:first-of-type::first-letter{
  font-size:3.1em; line-height:.8; float:left; padding:.05em .08em 0 0; color:var(--accent); font-weight:700;
}
.ch-body h2{ font-family:var(--font-ui); font-size:1rem; letter-spacing:.04em; margin:2.2rem 0 1rem; }
.ch-body h3{ font-family:var(--font-ui); font-size:.9rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin:2rem 0 1rem; }
.ch-body em{ font-style:italic; }
.ch-body strong{ font-weight:700; }
hr.scene-break{
  border:0; text-align:center; margin:2.2rem 0;
}
hr.scene-break::before{
  content:"❧"; color:var(--accent); font-size:1.1rem; letter-spacing:.5em;
}

/* chapter nav */
.ch-nav{
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  margin-top:3rem; padding-top:1.4rem; border-top:1px solid var(--rule);
  font-family:var(--font-ui); font-size:.9rem; font-weight:600;
}
.ch-nav a{ color:var(--accent); text-decoration:none; padding:.4rem 0; }
.ch-nav a:hover{ text-decoration:underline; }
.ch-nav .disabled{ color:var(--muted); opacity:.5; }
.nav-home{ color:var(--muted) !important; }

@media (max-width:480px){
  .toc-list a{ padding:.7rem .4rem; }
  .ch-nav{ font-size:.82rem; }
}
@media print{
  .toolbar,#progress,.ch-nav{ display:none; }
  body{ background:#fff; color:#000; }
}
"""

JS = r"""
(function(){
  var THEMES=["light","sepia","dark"];
  var root=document.documentElement;

  // restore prefs
  try{
    var t=localStorage.getItem("ccg-theme"); if(t&&THEMES.indexOf(t)>=0) root.setAttribute("data-theme",t);
    var f=parseFloat(localStorage.getItem("ccg-fs")); if(f&&f>=0.85&&f<=1.6) root.style.setProperty("--fs",f+"rem");
  }catch(e){}

  function curFs(){
    var v=getComputedStyle(root).getPropertyValue("--fs");
    var n=parseFloat(v); return isNaN(n)?1.18:n;
  }
  function setFs(n){ n=Math.max(0.9,Math.min(1.55,n)); root.style.setProperty("--fs",n+"rem"); try{localStorage.setItem("ccg-fs",n);}catch(e){} }
  function cycleTheme(){
    var cur=root.getAttribute("data-theme")||"sepia";
    var next=THEMES[(THEMES.indexOf(cur)+1)%THEMES.length];
    root.setAttribute("data-theme",next);
    try{localStorage.setItem("ccg-theme",next);}catch(e){}
  }

  document.addEventListener("click",function(e){
    var b=e.target.closest("[data-action]"); if(!b) return;
    var a=b.getAttribute("data-action");
    if(a==="theme") cycleTheme();
    else if(a==="font-inc") setFs(curFs()+0.06);
    else if(a==="font-dec") setFs(curFs()-0.06);
  });

  // reading progress
  var bar=document.getElementById("progress-bar");
  function onScroll(){
    if(!bar) return;
    var h=document.documentElement;
    var max=(h.scrollHeight-h.clientHeight);
    var p=max>0?(h.scrollTop/max)*100:0;
    bar.style.width=p+"%";
  }
  document.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",onScroll); onScroll();

  // keyboard nav
  var art=document.querySelector(".chapter");
  document.addEventListener("keydown",function(e){
    if(e.target.matches("input,textarea")) return;
    if(e.key==="t"||e.key==="T"){ cycleTheme(); return; }
    if(e.key==="+"||e.key==="="){ setFs(curFs()+0.06); return; }
    if(e.key==="-"||e.key==="_"){ setFs(curFs()-0.06); return; }
    if(e.key==="Escape"){ window.location.href="index.html"; return; }
    if(!art) return;
    var prev=art.getAttribute("data-prev"), next=art.getAttribute("data-next");
    if((e.key==="ArrowRight")&&next){ window.location.href=next; }
    if((e.key==="ArrowLeft")&&prev){ window.location.href=prev; }
  });

  // remember last-read chapter for a "continue" hint on the index
  try{
    if(art){
      var slug=location.pathname.split("/").pop();
      localStorage.setItem("ccg-last",slug);
    }else{
      var last=localStorage.getItem("ccg-last");
      if(last){
        var link=document.querySelector('.toc-list a[href="'+last+'"]');
        if(link){ link.classList.add("last-read"); link.setAttribute("title","Last read"); }
      }
    }
  }catch(e){}
})();
"""


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build_single_file(chapters: list[dict]) -> str:
    """One self-contained .html with everything inline — ideal for phones/offline."""
    total_words = sum(c["words"] for c in chapters)

    toc_items = []
    for i, ch in enumerate(chapters, 1):
        meta = f'<span class="toc-meta">{ch["meta"]}</span>' if ch["meta"] else ""
        toc_items.append(
            f'<li><a href="#ch{i}"><span class="toc-num">{i:02d}</span>'
            f'<span class="toc-text"><span class="toc-title">{html.escape(ch["title"])}</span>'
            f"{meta}</span></a></li>"
        )
    toc = "\n".join(toc_items)

    sections = []
    for i, ch in enumerate(chapters, 1):
        meta = f'<p class="ch-meta">{ch["meta"]}</p>' if ch["meta"] else ""
        nav_up = '<a class=" js-top" href="#top">↑ Contents</a>'
        nav_next = f'<a href="#ch{i+1}">Next →</a>' if i < len(chapters) else '<span class="disabled">Finis</span>'
        nav_prev = f'<a href="#ch{i-1}">← Previous</a>' if i > 1 else '<a href="#top">← Contents</a>'
        sections.append(f"""
<section class="chapter" id="ch{i}">
  <header class="ch-head">
    <p class="ch-counter">Chapter {i} of {len(chapters)}</p>
    <h2 class="ch-title">{html.escape(ch["title"])}</h2>
    {meta}
  </header>
  <div class="ch-body">{ch["body"]}</div>
  <nav class="ch-nav">{nav_prev}{nav_up}{nav_next}</nav>
</section>
""")
    body_sections = "\n".join(sections)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="sepia">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="theme-color" content="#9a2c1f" />
<title>{html.escape(SITE_TITLE)}</title>
<style>{CSS}
/* single-file extras */
.singlefile .chapter{{ border-top:1px solid var(--rule); padding-top:3rem; }}
.singlefile .chapter:first-of-type{{ border-top:0; }}
.ch-nav a.disabled,.ch-nav span.disabled{{ color:var(--muted); opacity:.5; }}
#totop{{ position:fixed; right:1rem; bottom:1rem; z-index:45; display:none;
  font-family:var(--font-ui); font-size:.8rem; font-weight:700; color:#fff;
  background:var(--accent); border:0; border-radius:50%; width:2.8rem; height:2.8rem;
  box-shadow:0 2px 10px var(--shadow); cursor:pointer; }}
</style>
</head>
<body class="singlefile">
<div id="progress"><div id="progress-bar"></div></div>

<div class="toolbar">
  <a class="tb-btn home" href="#top">☰ Contents</a>
  <div class="tb-spacer"></div>
  <button class="tb-btn" data-action="font-dec" title="Smaller text">A−</button>
  <button class="tb-btn" data-action="font-inc" title="Larger text">A+</button>
  <button class="tb-btn" data-action="theme" title="Toggle theme">◑ Theme</button>
</div>

<main class="cover" id="top">
  <header class="cover-head">
    <p class="kicker">{html.escape(SITE_SUBTITLE)}</p>
    <h1 class="cover-title">{html.escape(SITE_TITLE)}</h1>
    <p class="cover-blurb">A man from our world is reborn on the Douluo Continent
      with a martial soul shaped from the Red&nbsp;Priest pathway&mdash;war, fire,
      plunder, and blood&mdash;stripped of the madness that should have been its
      price. He pays no cost for power. Everything around him does.</p>
    <p class="cover-stats">{len(chapters)} chapters &middot; {total_words:,} words &middot; one offline file</p>
  </header>
  <nav class="toc">
    <h2>Contents</h2>
    <ol class="toc-list">{toc}</ol>
  </nav>
</main>

{body_sections}

<button id="totop" title="Back to contents">↑</button>
<script>
(function(){{
  var THEMES=["light","sepia","dark"],root=document.documentElement;
  try{{var t=localStorage.getItem("ccg-theme");if(t)root.setAttribute("data-theme",t);
    var f=parseFloat(localStorage.getItem("ccg-fs"));if(f)root.style.setProperty("--fs",f+"rem");}}catch(e){{}}
  function curFs(){{var n=parseFloat(getComputedStyle(root).getPropertyValue("--fs"));return isNaN(n)?1.18:n;}}
  function setFs(n){{n=Math.max(0.9,Math.min(1.6,n));root.style.setProperty("--fs",n+"rem");try{{localStorage.setItem("ccg-fs",n);}}catch(e){{}}}}
  function cycle(){{var c=root.getAttribute("data-theme")||"sepia",x=THEMES[(THEMES.indexOf(c)+1)%THEMES.length];root.setAttribute("data-theme",x);try{{localStorage.setItem("ccg-theme",x);}}catch(e){{}}}}
  document.addEventListener("click",function(e){{var b=e.target.closest("[data-action]");if(!b)return;var a=b.getAttribute("data-action");if(a==="theme")cycle();else if(a==="font-inc")setFs(curFs()+0.06);else if(a==="font-dec")setFs(curFs()-0.06);}});
  var bar=document.getElementById("progress-bar"),totop=document.getElementById("totop");
  function onScroll(){{var h=document.documentElement,max=h.scrollHeight-h.clientHeight,p=max>0?h.scrollTop/max*100:0;if(bar)bar.style.width=p+"%";if(totop)totop.style.display=h.scrollTop>600?"block":"none";}}
  document.addEventListener("scroll",onScroll,{{passive:true}});window.addEventListener("resize",onScroll);onScroll();
  if(totop)totop.addEventListener("click",function(){{window.scrollTo({{top:0,behavior:"smooth"}});}});
}})();
</script>
</body>
</html>
"""


def word_count(md: str) -> int:
    text = re.sub(r"[*_#>\-]", " ", md)
    return len(text.split())


def main():
    files = sorted(CHAPTERS_DIR.glob("chapter-*.md"))
    if not files:
        raise SystemExit("No chapters found in ./chapters")

    chapters = []
    for f in files:
        md = f.read_text(encoding="utf-8")
        title, meta_html, body_html = parse_chapter(md)
        chapters.append({
            "slug": f.stem,
            "title": title,
            "meta": meta_html,
            "body": body_html,
            "words": word_count(md),
        })

    OUT_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(CSS, encoding="utf-8")
    (ASSETS_DIR / "reader.js").write_text(JS, encoding="utf-8")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: serve as-is

    total = len(chapters)
    for i, ch in enumerate(chapters):
        prev_ch = chapters[i - 1] if i > 0 else None
        next_ch = chapters[i + 1] if i < total - 1 else None
        page = build_chapter_page(ch, prev_ch, next_ch, i + 1, total)
        (OUT_DIR / f'{ch["slug"]}.html').write_text(page, encoding="utf-8")

    (OUT_DIR / "index.html").write_text(build_index(chapters), encoding="utf-8")

    # single self-contained file (great for phones / offline / sending)
    single_name = "crucible-of-the-crimson-god.html"
    (OUT_DIR / single_name).write_text(build_single_file(chapters), encoding="utf-8")

    # tiny manifest for tooling
    manifest = {
        "title": SITE_TITLE,
        "chapters": [{"slug": c["slug"], "title": c["title"], "words": c["words"]} for c in chapters],
        "total_words": sum(c["words"] for c in chapters),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Built {total} chapters -> {OUT_DIR}")
    print(f"Total words: {manifest['total_words']:,}")
    print(f"Open: {OUT_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
