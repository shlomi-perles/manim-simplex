# tests/

Pytest suites for the `manim-simplex` plugin.

## Layout

- `tests/test_section.py` -- `SimplexSectionType` enum behaviour. Pure
  Python.
- `tests/test_manifest.py` -- `DeckManifest`, `MainSlide`, `Subsection`
  schema, JSON round-trip, helper methods. Pure Python.
- `tests/theme/` -- palette / preamble immutability, preset round-trips,
  context push/pop. Stdlib + pytest only.
- `tests/engine/` -- `Region` math, `Remove` lookup (WeakKeyDictionary +
  thread-safe registry), `HighlightResult`, glyph_map / ghost_fade
  animations, geometry, dynamics, text, scaling, debug. Manim-touching
  cases use `pytest.importorskip("manim")`.
- `tests/mobjects/` -- smoke construction tests for `Node`, `Edge`, ...
- `tests/slides/` -- `BaseSlide.next_slide` section-type resolution
  (no auto-promotion, fail-loudly path) and `make_chrome` purity tests.

## Don't

- Don't render a deck here -- the manim-slides subprocess is too slow.
  Render-smoke lives in the `simplex` repo's CI and in
  `examples/` (which can be manually rendered for visual checks).
- Don't import `manim` in `conftest.py`; keep collection fast.
- Don't call `apply_theme_defaults` -- it mutates global Manim state.
