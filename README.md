# manim-simplex

[![PyPI version](https://img.shields.io/pypi/v/manim-simplex.svg)](https://pypi.org/project/manim-simplex/)
[![Python](https://img.shields.io/pypi/pyversions/manim-simplex.svg)](https://pypi.org/project/manim-simplex/)
[![License](https://img.shields.io/pypi/l/manim-simplex.svg)](https://github.com/shlomi-perles/manim-simplex/blob/main/LICENSE)

The Manim plugin half of [Simplex](https://github.com/shlomi-perles/simplex):
theme tokens, reusable mobjects, slide hierarchy, deck manifest schema,
and the `manim.plugins` entry-point. Distributed on PyPI as
`manim-simplex`.

The lecture-portal platform (CLI, deck discovery, render orchestration,
web builder) lives in the sibling [`simplex`](https://github.com/shlomi-perles/simplex)
package; both contribute modules to the shared PEP 420 `simplex/`
namespace.

## What ships here

| Module | Contents |
|---|---|
| `simplex.plugin` | `activate()` -- the `manim.plugins` entry-point. Applies the active theme to `manim.config`. |
| `simplex.section` | `SimplexSectionType` enum -- the slide-hierarchy strings written into Manim's sections JSON. Manim-free. |
| `simplex.manifest` | `DeckManifest`, `MainSlide`, `Subsection` Pydantic models -- the cross-package contract consumed by the `simplex` web builder. Manim-free. |
| `simplex.theme` | `Theme`, `Palette`, `Typography`, `Spacing`, `Motion`, `LatexProfile`, `WebPalette`, `active_theme`, `get_active_theme`, `presets`, `render_web_css`. |
| `simplex.engine` | Animation primitives -- `Region`, `Remove`, `clear_scene`, `exit_for`, `register_exit`, `set_exit_animation`, `HighlightResult`, `apply_theme_defaults`, plus the `glyph_map`, `ghost_fade`, `dynamics`, `geometry`, `code`, `text`, `scaling`, `debug` submodules. |
| `simplex.mobjects` | `Node`, `Edge`, `ArrayMob`, `ArrayEntry`, `ArrayPointer`, `OutlineProgressBar`. |
| `simplex.slides` | `BaseSlide`, `OutlineScene`, `OutlinePart`, `Chrome`, `make_chrome`. |

## Install

```bash
uv add manim-simplex
# or
pip install manim-simplex
```

System dependencies (texlive, ffmpeg, cairo, pango) are the same as
Manim's -- see the [Manim install guide](https://docs.manim.community/en/stable/installation.html).

## Quick start

```ini
# decks/<your-deck>/manim.cfg
[CLI]
plugins = simplex
save_sections = True
```

```python
from manim import MathTex
from simplex.slides import BaseSlide, make_chrome
from simplex.theme import presets

class Hello(BaseSlide):
    def setup(self) -> None:
        super().setup()
        chrome = make_chrome(presets.DASTIMATOR_DARK, self.region, header="Hello")
        self.add_to_canvas(**chrome.mobjects)
        self.region = chrome.body_region

    def construct(self) -> None:
        from manim import ORIGIN, Write
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.region.place(eq, ORIGIN)
        self.play(Write(eq))
        self.next_slide(name="Hello")
```

```bash
uv run manim-slides render path/to/your_deck/scene.py Hello
```

## Slide hierarchy

`BaseSlide.next_slide` writes a `SimplexSectionType` value into Manim's
native section JSON. The web builder reconciles that with manim-slides'
`PresentationConfig` to build a main/sub tree.

- `self.next_slide(name="Title")` -> **MAIN** slide named `"Title"`.
- `self.next_slide()` as the *first* call -> **MAIN** slide
  auto-named after the scene class with PascalCase boundaries spaced
  out (``DFSLecture`` → ``"DFS Lecture"``; no warning).
- `self.next_slide()` after a named main -> **SUB** slide.
- `self.next_slide(..., loop=True)` -> the `LOOP` variant.
- `self.next_slide(..., section_type="simplex.main.skip")` -> explicit
  override always wins.

## Outline slides

`OutlineScene` composes typed `OutlinePart` objects into an animated
`BaseSlide` outline. Each part owns already-built Manim mobjects for its
feature title, compact label, and optional visual. Progress dots are
positioned with `self.region.linspace(RIGHT, n)` defaults, so edge
margins and inter-dot gaps are equal.

```python
from manim import Circle, Square, Tex
from simplex.engine.text import Caption
from simplex.slides import OutlinePart, OutlineScene

class Outline(OutlineScene):
    def __init__(self, **kwargs):
        super().__init__(
            parts=[
                OutlinePart(Tex("Research Question"), Caption("Question"), Circle()),
                OutlinePart(Tex("Algorithms"), Caption("Algorithms"), Square()),
            ],
            **kwargs,
        )
```

## Theme

Themes are frozen Pydantic models -- the same instance produces:

1. Manim defaults (via `apply_theme_defaults`, called by the plugin).
2. A `TexTemplate` (via `LatexProfile.as_tex_template`).
3. CSS variables for the web portal + RevealJS HTML (via
   `render_web_css(theme.web_palette)`).
4. The `darcula` Pygments style (registered by the plugin).

Switch themes per-scope with `active_theme`:

```python
from simplex.theme import presets
from simplex.theme.context import active_theme

from manim import Tex

with active_theme(presets.ACADEMIC_LIGHT):
    label = Tex("This Tex picks up the academic light palette.")
```

## Cross-package contract

`manim-simplex` owns the manifest schema; `simplex` imports it:

```python
from simplex.manifest import DeckManifest, MainSlide, Subsection
```

When the schema bumps `schema_version`, the web builder hard-fails on
unknown versions with a pointer at the `manim-simplex` upgrade. This
keeps the two repos honest about their contract.

## Why a separate distribution?

The plugin surface (mobjects + theme + entry-point + manifest schema)
is reusable independently of the lecture-portal pipeline. Splitting
them lets the plugin be a thin dependency for users who want to render
slides without pulling in Typer, watchfiles, Jinja, and the web
builder stack.

Python's PEP 420 implicit namespace packages merge the two distributions
at import time. Neither wheel ships `src/simplex/__init__.py`, so
`from simplex.engine import Remove` resolves regardless of which wheel
contributed the module.

## Development

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/shlomi-perles/manim-simplex.git
cd manim-simplex
uv sync --all-extras
uv run pre-commit install
uv run pytest -q
uv run ruff check .
uv run basedpyright
```

Examples under `examples/` are runnable demo scenes; they double as
documentation and CI smoke tests:

```bash
uv run manim -pql examples/hello_slide.py HelloSlide
```

## License

MIT.
