# tests/

Pytest suites for the `manim-simplex` plugin (theme tokens, engine
helpers, slide bases).

## Layout

- `tests/theme/` — palette / preamble immutability, preset round-trips,
  context push/pop. Stdlib + pytest only.
- `tests/engine/` — `Region` math, `Remove` lookup, transforms, geometry,
  dynamics, text, scaling, code. Manim-touching cases use
  `pytest.importorskip("manim")`.

## Don't

- Don't render a deck here — the manim-slides subprocess is too slow.
  Render-smoke lives in the `simplex` repo's CI.
- Don't import `manim` in `conftest.py`; keep collection fast.
- Don't call `apply_theme_defaults` — it mutates global Manim state.
