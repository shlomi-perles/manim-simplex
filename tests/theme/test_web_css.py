"""Web palette CSS emits tokens, not global page styles."""

from simplex.theme.tokens import WebPalette
from simplex.theme.web_css import render_web_css


def test_render_web_css_is_variables_only() -> None:
    css = render_web_css(WebPalette(background="#123456"))

    assert "--simplex-bg: #123456" in css
    assert "body {" not in css
    assert ".reveal" not in css


def test_default_web_background_matches_portal_chrome() -> None:
    css = render_web_css(WebPalette())

    assert "--simplex-bg: #2b2b2b" in css
