# manim-simplex

The Manim plugin half of [Simplex](https://github.com/shlomi-perles/simplex):
theme tokens, mobjects, slide hierarchy, and the `manim.plugins`
entry-point. Distributed on PyPI as `manim-simplex`.

The lecture-portal platform (CLI, deck discovery, render orchestration,
web builder) lives in the sibling [`simplex`](https://github.com/shlomi-perles/simplex)
package; both contribute modules to the shared PEP 420 `simplex/`
namespace.

## What ships here

- `simplex.plugin:activate` — the `manim.plugins` entry-point. Enable it
  per deck with `plugins = simplex` in `manim.cfg`.
- `simplex.engine` — `Region`, `Remove`, `register_exit`, `exit_for`,
  `clear_scene`, `apply_theme_defaults`, `SimplexSectionType`, plus the
  `transforms`, `dynamics`, `geometry`, `code`, `text`, `scaling`,
  `debug` helper modules.
- `simplex.theme` — `Theme`, `Palette`, `WebPalette`, `LatexProfile`,
  `Motion`, `Spacing`, `Typography`, `active_theme`, `get_active_theme`,
  `presets`, `render_web_css`.
- `simplex.slides` — `BaseSlide`, `make_chrome`,
  `components.{graph, array}`.

## Install

```bash
uv add manim-simplex
```

## Quick start (plugin only)

```ini
# decks/<your-deck>/manim.cfg
[CLI]
plugins = simplex
save_sections = True
```

```python
from manim import MathTex
from simplex.slides import BaseSlide

class Hello(BaseSlide):
    def construct(self) -> None:
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.region.place(eq, "center")
        self.play(self.region.write(eq))
        self.next_slide(name="Hello")
```

## Why a separate distribution?

The plugin surface (mobjects + theme + entry-point) is reusable
independently of the lecture-portal pipeline. Splitting them lets the
plugin be a thin dependency for users who want to render slides without
pulling in Typer, watchfiles, Jinja, and the web builder stack.

Python's PEP 420 implicit namespace packages merge the two distributions
at import time. Neither wheel ships `src/simplex/__init__.py`, so
`from simplex.engine import Remove` resolves regardless of which wheel
contributed the module.

## License

MIT.
