"""Region -- mutable rectangular sub-area of the frame.

The region API speaks in Manim's direction vectors (``UP``, ``DR``, ``ORIGIN``,
…) rather than ad-hoc strings. Each direction's ``(x, y)`` components in
``{-1, 0, 1}`` pick the corresponding edge / midpoint / center of the region.
"""

from collections.abc import Iterable
from typing import Self

import numpy as np
from manim import Mobject
from pydantic import BaseModel, ConfigDict


def _as_dir(anchor: np.ndarray | Iterable[float]) -> np.ndarray:
    """Coerce ``anchor`` to a length-3 float vector with components in {-1, 0, 1}.

    Raises ``ValueError`` for non-cardinal vectors so callers fail fast instead
    of getting a silently wrong placement.
    """
    arr = np.asarray(anchor, dtype=float)
    if arr.shape == (2,):
        arr = np.append(arr, 0.0)
    if arr.shape != (3,):
        raise ValueError(f"anchor must be a 2D or 3D direction vector, got shape {arr.shape}")
    if not np.all(np.isin(np.sign(arr).astype(int), (-1, 0, 1))):
        raise ValueError(
            f"anchor components must be in {{-1, 0, 1}} (a Manim direction); got {arr.tolist()}"
        )
    return np.sign(arr)


class Region(BaseModel):
    """A mutable axis-aligned region in Manim frame coordinates."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    top: float
    bottom: float
    left: float
    right: float

    @classmethod
    def full_frame(cls) -> Self:
        from manim import config

        half_w = config.frame_width / 2
        half_h = config.frame_height / 2
        return cls(top=half_h, bottom=-half_h, left=-half_w, right=half_w)

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom

    @property
    def center(self) -> np.ndarray:
        cx = (self.left + self.right) / 2
        cy = (self.top + self.bottom) / 2
        return np.array([cx, cy, 0.0])

    def _anchor_point(self, direction: np.ndarray) -> np.ndarray:
        """Map a normalized direction vector to the matching point of this region."""
        cx, cy, _ = self.center
        x = self.left if direction[0] < 0 else (self.right if direction[0] > 0 else cx)
        y = self.bottom if direction[1] < 0 else (self.top if direction[1] > 0 else cy)
        return np.array([x, y, 0.0])

    def place(
        self,
        mob: Mobject,
        anchor: np.ndarray | Iterable[float] | None = None,
        buff: float = 0.0,
    ) -> Mobject:
        """Move ``mob`` so its anchor sits at the matching point of this region.

        ``anchor`` is a Manim direction vector (``UP``, ``DR``, ``ORIGIN``, …).
        ``buff`` pulls ``mob`` inward by that distance plus half its own size
        along the same axis, so a non-zero ``buff`` always leaves visible
        breathing room between the mob and the region edge.
        """
        from manim import ORIGIN

        direction = _as_dir(ORIGIN if anchor is None else anchor)
        mob.move_to(self._anchor_point(direction))
        half_w, half_h = mob.width / 2, mob.height / 2
        dx = -direction[0] * (buff + half_w)
        dy = -direction[1] * (buff + half_h)
        if dx or dy:
            mob.shift(np.array([dx, dy, 0.0]))
        return mob

    def update(
        self,
        *,
        top: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        right: float | None = None,
    ) -> None:
        if top is not None:
            self.top = top
        if bottom is not None:
            self.bottom = bottom
        if left is not None:
            self.left = left
        if right is not None:
            self.right = right

    def shrink(
        self,
        *,
        top: float = 0.0,
        bottom: float = 0.0,
        left: float = 0.0,
        right: float = 0.0,
    ) -> None:
        self.top -= top
        self.bottom += bottom
        self.left += left
        self.right -= right

    def reset(self) -> None:
        full = Region.full_frame()
        self.top = full.top
        self.bottom = full.bottom
        self.left = full.left
        self.right = full.right

    def split(
        self,
        axis: np.ndarray | Iterable[float],
        k: int,
    ) -> list["Region"]:
        """Split this region into ``k`` sub-regions strung along ``axis``.

        Returns sub-regions in the direction of ``axis``:

        - ``axis == RIGHT``  -> left-to-right
        - ``axis == LEFT``   -> right-to-left
        - ``axis == UP``     -> bottom-to-top
        - ``axis == DOWN``   -> top-to-bottom

        Each piece keeps the original's perpendicular extent and gets
        ``1/k`` of the size along ``axis``. The union of the pieces equals
        ``self``; their centers split the axis dimension at uniform offsets.
        """
        if k < 1:
            raise ValueError(f"k must be >= 1, got {k}")
        direction = _as_dir(axis)
        horizontal = direction[0] != 0
        vertical = direction[1] != 0
        if horizontal == vertical:
            raise ValueError(
                "axis must be a single cardinal direction (RIGHT/LEFT/UP/DOWN), "
                f"got {direction.tolist()}"
            )
        cls = type(self)
        pieces: list[Region] = []
        if horizontal:
            step = self.width / k
            for i in range(k):
                left = self.left + i * step
                pieces.append(cls(top=self.top, bottom=self.bottom, left=left, right=left + step))
            if direction[0] < 0:
                pieces.reverse()
        else:
            step = self.height / k
            for i in range(k):
                bottom = self.bottom + i * step
                pieces.append(
                    cls(top=bottom + step, bottom=bottom, left=self.left, right=self.right)
                )
            if direction[1] < 0:
                pieces.reverse()
        return pieces
