"""Darcula registration + HighlightResult shape."""

import pytest

pytest.importorskip("pygments")

from simplex.engine.code import DarculaStyle, HighlightResult, register_darcula


def test_register_darcula_adds_to_style_map() -> None:
    import pygments.styles

    register_darcula()
    assert "darcula" in pygments.styles.STYLE_MAP


def test_register_darcula_is_idempotent() -> None:
    register_darcula()
    register_darcula()
    register_darcula()


def test_darcula_style_has_expected_background() -> None:
    assert DarculaStyle.background_color == "#111111"


def test_highlight_result_iterates_fade_only_when_indicate_is_none() -> None:
    pytest.importorskip("manim")
    from manim import AnimationGroup

    result = HighlightResult(fade=AnimationGroup())
    assert list(result) == [result.fade]


def test_highlight_result_iterates_fade_then_indicate() -> None:
    pytest.importorskip("manim")
    from manim import AnimationGroup, Indicate, Square

    fade = AnimationGroup()
    ind = Indicate(Square())
    result = HighlightResult(fade=fade, indicate=ind)
    assert list(result) == [fade, ind]


def test_highlight_result_is_frozen() -> None:
    pytest.importorskip("manim")
    from dataclasses import FrozenInstanceError

    from manim import AnimationGroup

    result = HighlightResult(fade=AnimationGroup())
    with pytest.raises(FrozenInstanceError):
        result.indicate = None  # type: ignore[misc]
