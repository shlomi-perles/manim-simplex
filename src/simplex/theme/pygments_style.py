"""DarculaStyle Pygments scheme shared by the engine (videos) and the web
(notes code blocks). Kept manim-free so the web build doesn't pull manim in.
"""

import sys
import types
from typing import ClassVar

from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Operator,
    Punctuation,
    Text,
)

_BACKGROUND = "#111111"
_SELECTION = "#333333"
_FOREGROUND = "#A9B7C6"

_RED = "#BC3F3C"
_ERROR_RED = "#960050"

_GRAY = "#808080"
_GRAY_ATTRIBUTE = "#BABABA"

_GREEN = "#6A8759"
_GREEN_DOC = "#629755"
_GREEN_INSERTED = "#A5C261"
_EMERALD = "#88BE05"

_GOLD = "#F1C829"
_YELLOW = "#BBB529"

_ORANGE = "#CC7832"

_AQUA = "#6897BB"
_BLUE_BUILTIN = "#8888C6"
_BLUE_ENTITY = "#6D9CBE"

_PURPLE = "#9876AA"

_TAG = "#E8BF6A"


def register_darcula(style_name: str = "darcula") -> None:
    """Register `DarculaStyle` under `style_name` in Pygments. Idempotent.

    Called automatically by `simplex.plugin.activate` and `engine.code.code_block`.
    Exposed so users with their own Code mobjects can opt into the same palette.
    """
    import pygments.styles

    if style_name in pygments.styles.STYLE_MAP:
        return
    cls_name = DarculaStyle.__name__
    module = types.ModuleType(style_name)
    setattr(module, cls_name, DarculaStyle)
    setattr(pygments.styles, style_name, module)
    sys.modules[f"pygments.styles.{style_name}"] = module
    style_map: dict[str, str] = pygments.styles.STYLE_MAP  # type: ignore[assignment]
    style_map[style_name] = f"{style_name}::{cls_name}"


class DarculaStyle(Style):
    """Pygments scheme inspired by JetBrains Darcula, ported from Simplex."""

    background_color = _BACKGROUND
    highlight_color = _SELECTION

    styles: ClassVar[dict[object, str]] = {
        Text: _FOREGROUND,
        Error: _ERROR_RED,
        Comment: _GRAY,
        Comment.Multiline: _GRAY,
        Comment.Preproc: _GRAY,
        Comment.Single: _GRAY,
        Comment.Special: _GRAY,
        Keyword: _ORANGE,
        Keyword.Constant: _ORANGE,
        Keyword.Declaration: _ORANGE,
        Keyword.Namespace: _ORANGE,
        Keyword.Pseudo: _ORANGE,
        Keyword.Reserved: _ORANGE,
        Keyword.Type: _ORANGE,
        Operator: _FOREGROUND,
        Operator.Word: _ORANGE,
        Punctuation: _FOREGROUND,
        Name: _FOREGROUND,
        Name.Attribute: _GRAY_ATTRIBUTE,
        Name.Builtin: _BLUE_BUILTIN,
        Name.Builtin.Pseudo: _PURPLE,
        Name.Class: _GOLD,
        Name.Constant: _PURPLE,
        Name.Decorator: _YELLOW,
        Name.Entity: _BLUE_ENTITY,
        Name.Exception: _GOLD,
        Name.Function: _GOLD,
        Name.Label: _FOREGROUND,
        Name.Namespace: _FOREGROUND,
        Name.Other: _EMERALD,
        Name.Tag: _TAG,
        Name.Variable: _FOREGROUND,
        Name.Variable.Class: _PURPLE,
        Name.Variable.Global: _PURPLE,
        Name.Variable.Instance: _PURPLE,
        Literal: _AQUA,
        Literal.Date: _GREEN,
        Literal.Number: _AQUA,
        Literal.String: _GREEN,
        Literal.String.Doc: _GREEN_DOC,
        Literal.String.Escape: _AQUA,
        Generic: _GRAY,
        Generic.Deleted: _RED,
        Generic.Emph: f"italic {_FOREGROUND}",
        Generic.Heading: _FOREGROUND,
        Generic.Inserted: _GREEN_INSERTED,
        Generic.Output: _FOREGROUND,
        Generic.Prompt: _GRAY,
        Generic.Strong: f"bold {_FOREGROUND}",
        Generic.Subheading: _FOREGROUND,
        Generic.Traceback: _RED,
    }
