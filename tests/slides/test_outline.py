"""OutlineScene control-flow smoke tests."""

from typing import Any, cast

import pytest

pytest.importorskip("manim")
pytest.importorskip("manim_slides")

from manim import Circle, Square

from simplex.slides.outline import OutlinePart, OutlineScene


class _Outline(OutlineScene):
    def __init__(self, *, focus_index: int | None = None, **kwargs: Any) -> None:
        super().__init__(
            parts=[
                OutlinePart(title=Circle(), label=Circle(), visual=Square()),
                OutlinePart(title=Circle(), label=Circle(), visual=Square()),
            ],
            focus_index=focus_index,
            **kwargs,
        )


def _stub_timeline(scene: OutlineScene) -> None:
    def noop(*args: Any, **kwargs: Any) -> None:
        return None

    target = cast(Any, scene)
    target.play = noop
    target.wait = noop
    target.next_slide = noop


def test_outline_scene_constructs_full_flow_without_renderer_writes() -> None:
    scene = _Outline()
    scene.setup()
    _stub_timeline(scene)

    scene.construct()

    assert scene.current_index == scene.part_count


def test_outline_scene_constructs_focused_flow_without_renderer_writes() -> None:
    scene = _Outline(focus_index=1)
    scene.setup()
    _stub_timeline(scene)

    scene.construct()

    assert scene.outline_started
    assert scene.focus_index == 1
