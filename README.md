# Crucible of the Crimson God

A long-form *Soul Land (Douluo Dalu)* fanfiction with a ruthless protagonist whose
martial soul is shaped from the **Red Priest pathway** (war, fire, plunder,
blood-sacrifice) — but stripped of its madness and loss-of-control. He pays no
price for power. Everything around him does. That displaced cost is the story.

Target length: **300,000–400,000 words**, serialized chapter by chapter.

## Read it

A clean, distraction-free reading website is generated into [`docs/`](docs/).

- **Locally:** open `docs/index.html` in any browser (works offline — no server needed).
- **Hosted:** the `docs/` folder is GitHub Pages–ready (Settings → Pages → deploy
  from branch, `/docs`). A `.nojekyll` file is included so assets serve as-is.

Reader features: light / sepia / dark themes, adjustable text size, reading-progress
bar, prev/next navigation, and keyboard shortcuts:

| Key | Action |
| --- | --- |
| `→` / `←` | Next / previous chapter |
| `T` | Cycle theme |
| `+` / `−` | Larger / smaller text |
| `Esc` | Back to contents |

Your theme, text size, and last-read chapter are remembered between visits.

## Repository layout

| Path | What it is |
| --- | --- |
| `chapters/chapter-NNN.md` | The chapters, in Markdown (the source of truth). |
| `STORY_BIBLE.md` | Living canon reference — power system, characters, world rules, threads. |
| `OUTLINE.md` | Arc structure, chapter plan, and a running progress tracker. |
| `build_site.py` | Dependency-free generator that builds `docs/` from the chapters. |
| `docs/` | The generated reading website (do not edit by hand; it is rebuilt). |

## Rebuild the site

After adding or editing any chapter, regenerate the website with:

```bash
python3 build_site.py
```

No third-party packages required (standard library only).

## Content note

Mature: graphic violence and dark themes. The narrative observes its protagonist;
it does not endorse him.
