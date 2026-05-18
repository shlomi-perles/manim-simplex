"""BaseSlide -- thin manim-slides ``Slide`` with the Simplex hierarchy API.

Theme and Manim defaults are wired in ``simplex.plugin:activate`` (the
``manim.plugins`` entry-point) once per render process. What stays in
``BaseSlide`` is the slide-hierarchy override:

- ``self.next_slide(name="...")`` -> **main** slide, named.
- ``self.next_slide()`` after at least one named main -> **sub** of the
  previous main.
- ``self.next_slide()`` *before* any named main -> ``RuntimeError`` with a
  fix-it message. Authors must mark the first slide explicitly; no silent
  auto-promotion.
- ``loop=True`` flips to the ``LOOP`` variant; an explicit ``section_type=``
  always wins.

The chosen ``SimplexSectionType.value`` round-trips into Manim's native
section JSON (``Section(type_=...) -> JSON "type"``), which the reconciler
in ``simplex.render.reconcile`` reads back to build the main/sub tree.
"""

from collections.abc import Iterable
from typing import Any

from manim_slides.slide import Slide

from simplex.engine.animations import clear_scene as _clear_scene
from simplex.engine.region import Region
from simplex.section import SimplexSectionType


class BaseSlide(Slide):
    """``manim_slides.Slide`` with the Simplex hierarchy + ``clear_scene``."""

    _current_main: str | None

    def setup(self) -> None:
        super().setup()
        self.region = Region.full_frame()
        self._current_main = None

    def next_slide(
        self,
        name: str | None = None,
        *,
        section_type: SimplexSectionType | str | None = None,
        loop: bool = False,
        **kwargs: Any,
    ) -> None:
        """Hierarchical next_slide.

        See module docstring for the rules; this method just forwards to
        ``manim_slides.Slide.next_slide`` with the resolved ``section_type``
        and a sensible default for RevealJS ``direction``.
        """
        resolved = self._resolve_section_type(name, section_type, loop)

        if resolved.is_main:
            # Required by SimplexSectionType.MAIN; section_type-explicit MAIN
            # without a name is also unambiguous since the user named it the
            # scene class.
            if name is None:
                name = type(self).__name__
            self._current_main = name

        kwargs.setdefault(
            "direction",
            "vertical" if resolved.is_sub else "horizontal",
        )

        super().next_slide(
            name=name or self._current_main or "unnamed",
            section_type=resolved.value,
            loop=loop,
            **kwargs,
        )

    def _resolve_section_type(
        self,
        name: str | None,
        section_type: SimplexSectionType | str | None,
        loop: bool,
    ) -> SimplexSectionType:
        # Explicit section_type always wins.
        if section_type is not None:
            if isinstance(section_type, SimplexSectionType):
                return section_type
            return SimplexSectionType(section_type)
        # Named call -> MAIN (LOOP variant on loop=True).
        if name is not None:
            return SimplexSectionType.MAIN_LOOP if loop else SimplexSectionType.MAIN
        # Bare call requires a current main; fail loudly otherwise.
        if self._current_main is None:
            cls_name = type(self).__name__
            raise RuntimeError(
                f"{cls_name}.next_slide(): first call must carry a name=, e.g. "
                f"`self.next_slide(name={cls_name!r})`. Bare next_slide() is a "
                "sub-slide and needs a preceding named main."
            )
        return SimplexSectionType.SUB_LOOP if loop else SimplexSectionType.SUB

    def clear_scene(self, *, exclude: Iterable[Any] = ()) -> None:
        """Play the registered exit animation for every mobject not in ``exclude``."""
        _clear_scene(self, exclude=exclude)
