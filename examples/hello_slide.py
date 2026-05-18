"""Minimal Simplex deck: one main slide, two sub-stops.

Demonstrates:
- `BaseSlide.next_slide(name=...)` to open a *main* slide.
- bare `BaseSlide.next_slide()` for a *sub* slide.
- `region.place(...)` to position via anchor.
- `Region` body shrunk by `make_chrome` for a clean header + body band.
"""

from manim import MathTex, Write

from simplex.slides import BaseSlide, make_chrome
from simplex.theme import presets


class HelloSlide(BaseSlide):
    def setup(self) -> None:
        super().setup()
        chrome = make_chrome(presets.DASTIMATOR_DARK, self.region, header="Hello, Simplex")
        self.add_to_canvas(**chrome.mobjects)
        self.region = chrome.body_region

    def construct(self) -> None:
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.region.place(eq, "center")
        self.play(Write(eq))
        self.next_slide(name="Hello: Euler")

        consequence = MathTex(r"\therefore\ \cos\pi + i\sin\pi = -1")
        self.region.place(consequence, "center")
        self.play(Write(consequence))
        self.next_slide()  # bare -> sub-stop of the Euler main slide
