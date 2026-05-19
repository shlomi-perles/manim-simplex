"""``make_chrome`` -- header / footer / page-number factory for ``BaseSlide``.

Authors call ``self.add_to_canvas(**chrome.mobjects)`` in their scene's
``setup()`` and re-bind ``self.region = chrome.body_region``. The chrome
lives on the manim-slides canvas so it survives ``clear_scene`` and
``Wipe``-style transitions automatically.

``make_chrome`` is a *pure* factory: it doesn't mutate its ``region``
argument. It returns a :class:`Chrome` ``NamedTuple`` carrying both the
mobjects for the canvas and a fresh, shrunk ``Region`` for the body.
"""

from typing import Any, NamedTuple

from manim import Tex

from simplex.engine.region import Region
from simplex.theme.tokens import Theme


class Chrome(NamedTuple):
    """Result of :func:`make_chrome`.

    ``mobjects`` -- dict ready to splat into ``Slide.add_to_canvas(**...)``.
    ``body_region`` -- a *new* ``Region`` shrunk to the body band; the
    original argument is left untouched.
    """

    mobjects: dict[str, Any]
    body_region: Region


def make_chrome(
    theme: Theme,
    region: Region,
    *,
    header: str | None = None,
    footer: str | None = None,
    page: int | None = None,
) -> Chrome:
    """Build optional header/footer/page mobjects and return a shrunk body Region.

    The ``region`` argument is **not** mutated. The returned
    ``Chrome.body_region`` is a fresh Region shrunk to fit beneath the
    requested chrome elements.
    """
    mobs: dict[str, Any] = {}

    if header:
        head = Tex(header, font_size=theme.typography.h2)
        region.place(head, "top", buff=0.15)
        mobs["header"] = head
    if footer:
        foot = Tex(footer, font_size=theme.typography.caption)
        region.place(foot, "bottom-left", buff=0.2)
        mobs["footer"] = foot
    if page is not None:
        pg = Tex(str(page), font_size=theme.typography.caption)
        region.place(pg, "bottom-right", buff=0.2)
        mobs["page"] = pg

    body = Region(
        top=region.top - (theme.spacing.header_height if header else 0.0),
        bottom=region.bottom
        + (theme.spacing.footer_height if (footer or page is not None) else 0.0),
        left=region.left,
        right=region.right,
    )
    return Chrome(mobjects=mobs, body_region=body)
