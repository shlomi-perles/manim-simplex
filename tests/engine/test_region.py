"""Region geometry: full_frame, shrink, anchor math, reset, split."""

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR

from simplex.engine.region import Region


def test_full_frame_center_is_origin() -> None:
    r = Region.full_frame()
    assert tuple(r.center) == (0.0, 0.0, 0.0)


def test_shrink_top_moves_center_down() -> None:
    r = Region.full_frame()
    original_top = r.top
    r.shrink(top=1.0)
    assert r.top == pytest.approx(original_top - 1.0)
    assert r.center[1] < 0.0


def test_reset_restores_full_frame() -> None:
    r = Region.full_frame()
    r.shrink(top=1.0, bottom=0.5, left=0.25, right=0.25)
    r.reset()
    full = Region.full_frame()
    assert (r.top, r.bottom, r.left, r.right) == (full.top, full.bottom, full.left, full.right)


def test_anchor_point_for_each_direction() -> None:
    """Each cardinal direction maps to the corresponding region edge/corner."""
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    cases = {
        tuple(ORIGIN.tolist()): (0.0, 0.0),
        tuple(UP.tolist()): (0.0, 2.0),
        tuple(DOWN.tolist()): (0.0, -2.0),
        tuple(LEFT.tolist()): (-3.0, 0.0),
        tuple(RIGHT.tolist()): (3.0, 0.0),
        tuple(UL.tolist()): (-3.0, 2.0),
        tuple(UR.tolist()): (3.0, 2.0),
        tuple(DR.tolist()): (3.0, -2.0),
    }
    for direction, expected in cases.items():
        point = r._anchor_point(np.array(direction))
        assert (point[0], point[1]) == expected, f"direction {direction} wrong"


def test_place_with_buff_pulls_mob_inward() -> None:
    """A non-zero buff plus the mob's half-extent keeps the mob inside."""
    from manim import Dot

    r = Region.full_frame()
    dot = Dot(radius=0.1)
    r.place(dot, UP, buff=0.25)
    # Dot's top edge should be 0.25 below the region's top edge.
    assert dot.get_top()[1] == pytest.approx(r.top - 0.25)


def test_place_rejects_string_anchor() -> None:
    """Region directions are vectors now; strings raise instead of silently
    routing to the legacy match-case path."""
    from manim import Dot

    r = Region.full_frame()
    with pytest.raises((ValueError, TypeError)):
        r.place(Dot(), "top", buff=0.0)  # type: ignore[arg-type]


def test_split_right_returns_left_to_right_pieces() -> None:
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    pieces = r.split(RIGHT, 3)
    assert len(pieces) == 3
    assert [(p.left, p.right) for p in pieces] == [(-3.0, -1.0), (-1.0, 1.0), (1.0, 3.0)]
    for p in pieces:
        assert p.top == 2.0
        assert p.bottom == -2.0


def test_split_left_returns_right_to_left_pieces() -> None:
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    pieces = r.split(LEFT, 3)
    assert [(p.left, p.right) for p in pieces] == [(1.0, 3.0), (-1.0, 1.0), (-3.0, -1.0)]


def test_split_up_returns_bottom_to_top_pieces() -> None:
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    pieces = r.split(UP, 4)
    assert len(pieces) == 4
    heights = [p.height for p in pieces]
    for h in heights:
        assert h == pytest.approx(1.0)
    # bottom-first ordering
    assert pieces[0].bottom == pytest.approx(-2.0)
    assert pieces[-1].top == pytest.approx(2.0)


def test_split_pieces_union_equals_original() -> None:
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    for axis, k in [(RIGHT, 5), (UP, 4), (DOWN, 2), (LEFT, 3)]:
        pieces = r.split(axis, k)
        total_extent = sum(p.width for p in pieces)
        # Width sums to original along horizontal split; height along vertical.
        if axis[0] != 0:
            assert total_extent == pytest.approx(r.width)
        else:
            total_h = sum(p.height for p in pieces)
            assert total_h == pytest.approx(r.height)


def test_split_k_one_returns_copy() -> None:
    r = Region(top=2.0, bottom=-2.0, left=-3.0, right=3.0)
    pieces = r.split(RIGHT, 1)
    assert len(pieces) == 1
    p = pieces[0]
    assert (p.top, p.bottom, p.left, p.right) == (r.top, r.bottom, r.left, r.right)


def test_split_rejects_non_cardinal_axis() -> None:
    r = Region.full_frame()
    with pytest.raises(ValueError, match="cardinal direction"):
        r.split(UR, 3)


def test_split_rejects_k_zero() -> None:
    r = Region.full_frame()
    with pytest.raises(ValueError, match=r"k must be >= 1"):
        r.split(RIGHT, 0)
