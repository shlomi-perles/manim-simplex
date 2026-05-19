"""Minimal OutlineScene demo."""

from manim import Circle, Square, Triangle

from simplex.engine.text import Caption, TexPage
from simplex.slides import OutlinePart, OutlineScene


class OutlineDemo(OutlineScene):
    def __init__(self, **kwargs):
        parts = [
            OutlinePart(
                title=TexPage(r"\textbf{Research Question}"),
                label=Caption(r"Research\\Question"),
                visual=Circle(),
            ),
            OutlinePart(
                title=TexPage(r"\textbf{Low-Rank Algorithms}"),
                label=Caption("Algorithms"),
                visual=Square(),
            ),
            OutlinePart(
                title=TexPage(r"\textbf{Case Study}"),
                label=Caption(r"Case\\Study"),
                visual=Triangle(),
            ),
        ]
        super().__init__(parts=parts, section_name="Outline Demo", **kwargs)
