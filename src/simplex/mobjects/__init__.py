"""Reusable Simplex mobjects.

Mirrors Manim's own ``manim.mobject.*`` namespace convention: each module
here ships VMobject subclasses that authors can use anywhere -- inside a
Slide, in a one-off Scene, or in a notebook. None of them require the
slide system.
"""

from simplex.mobjects.array import ArrayEntry, ArrayMob, ArrayPointer
from simplex.mobjects.graph import Edge, Node
from simplex.mobjects.outline import OutlineProgressBar

__all__ = ["ArrayEntry", "ArrayMob", "ArrayPointer", "Edge", "Node", "OutlineProgressBar"]
