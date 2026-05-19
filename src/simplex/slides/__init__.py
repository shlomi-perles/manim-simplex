"""Slide base class and chrome factory.

Re-usable mobjects live in :mod:`simplex.mobjects`; the slide hierarchy
enum lives in :mod:`simplex.section`; the deck manifest schema lives in
:mod:`simplex.manifest`.
"""

from simplex.slides.base import BaseSlide
from simplex.slides.chrome import Chrome, make_chrome

__all__ = ["BaseSlide", "Chrome", "make_chrome"]
