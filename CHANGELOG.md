# Changelog

All notable changes to `manim-simplex` are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-05-26

### Added

- `SimplexSolarizedLight` Pygments style — a new built-in light code style
  living alongside `SimplexPycharm` in `simplex.theme.styles`.
- `Theme.code_style` field — each theme preset now owns its Pygments style
  class, so the active theme drives the code formatter style instead of a
  hardcoded module-level default.
- `register_style()` and `register_all_builtin_styles()` — generic Pygments
  style registration helpers that replace the single-purpose
  `register_darcula()`.
- Code token colors are now emitted as `--simplex-code-*` CSS custom
  properties via `render_web_css()`, so the web layer can pick up the
  active style's palette.

### Changed

- **BREAKING:** `DarculaStyle` is renamed to `SimplexPycharm` and moved
  into the `simplex.theme.styles` subpackage. Import sites change from
  `from simplex.theme.pygments_style import DarculaStyle` to
  `from simplex.theme.styles import SimplexPycharm`.
- **BREAKING:** `register_darcula()` is removed in favour of
  `register_style(...)` and `register_all_builtin_styles()`.
- `engine/code.py` resolves the formatter style from the active theme
  rather than hardcoding a single style class.

### Removed

- Module-level global color variables from
  `simplex.theme.pygments_style` — colors are now scoped per style class.

## [0.2.3] - 2026-05-25

### Added

- Top-level authoring imports such as `from simplex import BaseSlide, Caption`.

### Changed

- Rename the default theme from `dastimator_dark` / `DASTIMATOR_DARK` to
  `simplex_dark` / `SIMPLEX_DARK`.

## [0.2.1] - 2026-05-24

### Changed

- Highlight Pygments word operators in the Darcula code style.

## [0.2.0] - 2026-05-24

### Added

- `TexPage` mobject — fixed-width minipage helper. Width is configurable
  via the ``width_cm`` kwarg (default 20.0) or by overriding the class
  attribute on a subclass. Replaces the old ``Definition`` mobject; the
  hardcoded minipage literal no longer appears in presets or
  tests.
- `Region.split(axis, k)` — divide a region into ``k`` sub-regions
  along a cardinal direction. Each piece keeps the perpendicular extent
  and gets ``1/k`` of the axis extent; pieces are returned in the
  direction of ``axis``. Their union equals the original region.
- `Spacing.header_buff` / `Spacing.footer_buff` — chrome gap distances
  exposed on the theme so they can be tuned deck-wide without editing
  ``make_chrome``.
- `simplex.manifest` module — Pydantic models (`DeckManifest`, `MainSlide`,
  `Subsection`) that define the cross-package contract between the plugin
  and the `simplex` web builder. The web builder now imports the schema
  from the plugin rather than redefining it locally.
- `simplex.section` module — `SimplexSectionType` enum promoted to the
  package root (previously `simplex.engine.section_types`). Manim-free so
  the web builder and CLI can use it without paying for a Manim import.
- `simplex.mobjects` subpackage — `Node`, `Edge`, `ArrayMob`, `ArrayEntry`,
  `ArrayPointer` promoted from `simplex.slides.components` to a top-level
  mobjects package, matching Manim's own `manim.mobject.*` convention.
- `simplex.slides.Chrome` NamedTuple — pure factory return type combining
  the canvas mobjects dict and the body region.
- `simplex.engine.HighlightResult` dataclass — typed return for
  `highlight_code_lines`, iterable so the existing `self.play(*result)`
  pattern still works.
- `py.typed` marker — downstream `pyright`/`mypy` users now get type
  information for the `simplex` namespace.
- `examples/` directory — runnable demo scenes (`hello_slide.py`,
  `theme_demo.py`, `glyph_map_demo.py`) used as documentation and CI
  fixtures.
- `.pre-commit-config.yaml` — ruff, ruff-format, codespell, and standard
  whitespace/yaml/toml hygiene hooks.
- CHANGELOG.md.
- CI: `manim plugins -l` discovery smoke test alongside the existing
  import smoke.

### Changed

- **BREAKING:** ``Region.place`` now takes a Manim **direction vector**
  (``UP``, ``DR``, ``ORIGIN``, …) instead of a string anchor name. The
  same applies to the ``_anchor_point`` helper. Migrate
  ``region.place(mob, "top", buff=…)`` → ``region.place(mob, UP, buff=…)``.
- **BREAKING:** ``make_chrome`` no longer accepts a ``page=`` parameter.
  Slide numbering is presentation chrome and is now driven by the
  RevealJS template (toggle via ``[web]`` overrides in ``deck.toml``)
  so it survives without being baked into each frame.
- **BREAKING:** ``BodyText`` is removed. Plain ``manim.Tex`` carries the
  theme's body font size through ``apply_theme_defaults`` — call sites
  rewrite ``BodyText(...)`` to ``Tex(...)``.
- **BREAKING:** ``Definition`` is renamed to ``TexPage`` (and no longer
  reads ``theme.latex.environments["definition"]``).
- ``BaseSlide`` auto-promotion now pretty-prints the class name into a
  space-separated label (``DFSLecture`` → ``"DFS Lecture"``,
  ``ImplementBFSSlide`` → ``"Implement BFS Slide"``). The class name
  itself is unchanged.
- **BREAKING:** Python floor raised to **3.13** (was a transitional 3.14
  in the Phase 3 split commit). 3.13 is a long-term-supportable floor
  with much wider availability for lecture authors.
- **BREAKING:** `simplex.engine.section_types` → `simplex.section`.
- **BREAKING:** `simplex.slides.components.{graph, array}` →
  `simplex.mobjects.{graph, array}`.
- **BREAKING:** `simplex.engine.transforms` is split into
  `simplex.engine.glyph_map` (`TransformByGlyphMap`) and
  `simplex.engine.ghost_fade` (`GhostSlideFade`). The combined module is
  removed.
- `BaseSlide.next_slide()` still auto-promotes the first bare call to
  a main slide (named after the scene class), but no longer emits a
  `UserWarning`. Passing `name=` on the first call still works and only
  changes the slide's name; the section type is `MAIN` either way.
- **BREAKING:** `make_chrome` no longer mutates its `Region` argument.
  It returns a `Chrome(mobjects, body_region)` NamedTuple. Callers do
  `chrome = make_chrome(...); self.add_to_canvas(**chrome.mobjects);
  self.region = chrome.body_region` (or destructure).
- **BREAKING:** `highlight_code_lines` returns `HighlightResult` (a
  frozen dataclass with `.fade` and `.indicate`) instead of the prior
  tuple-or-AnimationGroup union. `*result` unpacks back into the
  previous tuple form for callers that prefer it.
- Exit animation overrides are now stored in a `WeakKeyDictionary`
  registry rather than monkey-patched onto the `Mobject` as a
  `_simplex_exit` attribute. The public API (`set_exit_animation`,
  `exit_for`, `Remove`) is unchanged.
- The exit-defaults registry is now wrapped in a singleton with
  threading.Lock-guarded lazy init, removing the module-level mutable
  global.

### Removed

- ``BodyText`` mobject. Use ``manim.Tex`` (body size + color come from
  ``apply_theme_defaults``) or ``Caption`` for smaller annotations.
- ``Definition`` mobject. Replaced by ``TexPage`` (see Added/Changed).
- ``make_chrome(..., page=…)`` parameter and the corresponding ``page``
  entry in ``Chrome.mobjects``. Slide numbering moves to the web layer.
- ``LatexProfile.environments["definition"]`` entries from
  ``SIMPLEX_DARK`` and ``ACADEMIC_LIGHT``: ``TexPage`` is now the
  single owner of the ``{minipage}{<width>cm}`` literal.
- `simplex.engine.section_types` module (replaced by `simplex.section`).
- `simplex.slides.components` subpackage (replaced by `simplex.mobjects`).
- `simplex.engine.transforms` module (split — see Changed).
- `UserWarning` on the first bare `BaseSlide.next_slide()` call. Auto-
  promotion stays (named after the class), just silently.
