# manim-simplex

[![PyPI version](https://img.shields.io/pypi/v/manim-simplex.svg)](https://pypi.org/project/manim-simplex/)
[![Python](https://img.shields.io/pypi/pyversions/manim-simplex.svg)](https://pypi.org/project/manim-simplex/)
[![CI](https://github.com/shlomi-perles/manim-simplex/actions/workflows/ci.yml/badge.svg)](https://github.com/shlomi-perles/manim-simplex/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/shlomi-perles/manim-simplex.svg)](https://github.com/shlomi-perles/manim-simplex/blob/main/LICENSE)

`manim-simplex` is the Manim plugin layer for Simplex: theme tokens,
slide bases, reusable mobjects, animation helpers, and the shared deck
manifest schema used by the Simplex web builder.

It is published as `manim-simplex` and exposes the `simplex` Manim authoring
API.

## Requirements

- Python 3.13+
- Manim Community 0.20.1+
- manim-slides 5.1.7+
- Manim's system dependencies, including FFmpeg, Cairo, Pango, and a TeX
  distribution when rendering TeX. See the Manim installation guide:
  https://docs.manim.community/en/stable/installation.html

## Install

```bash
pip install manim-simplex
```

With uv:

```bash
uv add manim-simplex
```

Verify that Manim can discover the plugin:

```bash
python -m manim plugins -l
```

The output should include `simplex`.

## Configure Manim

Enable the plugin in the `manim.cfg` next to your scenes or deck:

```ini
[CLI]
plugins = simplex
save_sections = True
```

Manim imports `simplex.plugin` through the `manim.plugins` entry point.
The plugin applies the active Simplex theme to Manim defaults, registers
the Darcula Pygments style, sets the TeX template, sets the background
color, and enables section JSON output.

## Quick Start

```python
from manim import ORIGIN, MathTex, Write

from simplex import BaseSlide, make_chrome, presets


class HelloSlide(BaseSlide):
    def setup(self) -> None:
        super().setup()
        chrome = make_chrome(
            presets.SIMPLEX_DARK,
            self.region,
            header="Hello, Simplex",
        )
        self.add_to_canvas(**chrome.mobjects)
        self.region = chrome.body_region

    def construct(self) -> None:
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.region.place(eq, ORIGIN)
        self.play(Write(eq))
        self.next_slide()  # first call -> MAIN named "Hello Slide"

        consequence = MathTex(r"\therefore\ \cos\pi + i\sin\pi = -1")
        self.region.place(consequence, ORIGIN)
        self.play(Write(consequence))
        self.next_slide()  # later bare calls -> SUB stops
```

Render as a slide deck:

```bash
manim-slides render path/to/scene.py HelloSlide
manim-slides present HelloSlide
```

Or, in a uv-managed project:

```bash
uv run manim-slides render path/to/scene.py HelloSlide
uv run manim-slides present HelloSlide
```

## What Ships Here

| Module | Public surface |
| --- | --- |
| `simplex.plugin` | `activate()` entry point used by Manim. |
| `simplex.slides` | `BaseSlide`, `OutlineScene`, `OutlinePart`, `Chrome`, `make_chrome`. |
| `simplex.engine` | `Region`, `Remove`, `clear_scene`, `exit_for`, `register_exit`, `set_exit_animation`, `HighlightResult`, `apply_theme_defaults`. |
| `simplex.mobjects` | `Node`, `Edge`, `ArrayMob`, `ArrayEntry`, `ArrayPointer`, `OutlineProgressBar`, `Paper`, `ShowPaper`, `DismissPaper`, `PickPage`. |
| `simplex.theme` | `Theme`, `Palette`, `Typography`, `Spacing`, `Motion`, `LatexProfile`, `WebPalette`, `active_theme`, `get_active_theme`, `presets`, `render_web_css`. |
| `simplex.section` | `SimplexSectionType`, the section strings written into Manim section JSON. |
| `simplex.manifest` | `DeckManifest`, `MainSlide`, `Subsection`, the Pydantic schema shared with `simplex-web`. |

Additional focused helpers live in submodules such as
`simplex.engine.glyph_map`, `simplex.engine.code`,
`simplex.engine.geometry`, `simplex.engine.text`, and
`simplex.engine.debug`.

## Slide Hierarchy

`BaseSlide.next_slide` writes Simplex section types into Manim's native
section JSON. The `simplex-web` builder later reconciles those
sections with manim-slides metadata.

```python
self.next_slide(name="Title")          # MAIN slide named "Title"
self.next_slide()                      # first bare call: MAIN named after the class
self.next_slide()                      # later bare calls: SUB slide
self.next_slide(loop=True)             # loop variant
self.next_slide(section_type="simplex.main.skip")  # explicit override
```

The first bare call is auto-named from the scene class, so
`DFSLecture` becomes `DFS Lecture`.

## Themes

Themes are frozen Pydantic models. The same theme instance drives Manim
defaults, TeX defaults, Pygments highlighting, and CSS variables for the
web portal.

```python
from manim import Tex

from simplex import active_theme, presets


with active_theme(presets.ACADEMIC_LIGHT):
    label = Tex("This Tex uses the academic light palette.")
```

Available presets include `SIMPLEX_DARK` and `ACADEMIC_LIGHT`.

## Outline Slides

`OutlineScene` turns typed `OutlinePart` objects into an animated agenda
slide with progress indicators.

```python
from manim import Circle, Square, Tex

from simplex import Caption, OutlinePart, OutlineScene


class Outline(OutlineScene):
    def __init__(self, **kwargs):
        super().__init__(
            parts=[
                OutlinePart(Tex("Research Question"), Caption("Question"), Circle()),
                OutlinePart(Tex("Algorithms"), Caption("Algorithms"), Square()),
            ],
            section_name="Outline",
            **kwargs,
        )
```

## Examples

This repository includes runnable examples:

```bash
uv run manim -pql examples/theme_demo.py ThemeDemo
uv run manim -pql examples/glyph_map_demo.py GlyphMapDemo
uv run manim-slides render examples/hello_slide.py HelloSlide
uv run manim-slides render examples/outline_slide.py OutlineDemo
```

The examples directory has its own `manim.cfg`, so the Simplex plugin is
enabled when commands are run from the repository root.

## Relationship To `simplex-web`

Simplex is split into two PyPI distributions:

| Distribution | Import namespace | Purpose |
| --- | --- | --- |
| `manim-simplex` | `simplex.*` | Manim plugin, slide bases, theme, mobjects, manifest schema. |
| `simplex-web` | `simplex.*` | CLI, deck discovery, render orchestration, and static web portal. |

`manim-simplex` provides a lightweight `simplex.__init__` facade so deck
authors can write imports such as `from simplex import BaseSlide, Caption`.
The facade extends the package path for `simplex-web`, so `simplex.web`,
`simplex.deck`, and the CLI-side modules continue to compose with it.

Install only `manim-simplex` if you want to render scenes and slides.
Install `simplex-web` later when you want the full lecture portal and CLI.

## Development

```bash
git clone https://github.com/shlomi-perles/manim-simplex.git
cd manim-simplex
uv sync --all-extras
uv run pre-commit install
```

Useful checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run pytest -q
uv build
uvx twine check dist/*
```

Run plugin smoke tests locally:

```bash
uv run python -c "import simplex.plugin; simplex.plugin.activate(); print('ok')"
uv run manim plugins -l
```

## Release

Releases are published to PyPI by GitHub Actions through PyPI Trusted
Publishing. To release a new version:

1. Update `version` in `pyproject.toml`.
2. Move changelog entries under a dated release heading.
3. Commit the release prep.
4. Push an annotated tag such as `v0.2.3`.

The `Publish to PyPI` workflow builds an sdist and wheel, checks both
with Twine, uploads them as a GitHub artifact, and publishes to PyPI via
OIDC.

## License

MIT. See [LICENSE](LICENSE).
