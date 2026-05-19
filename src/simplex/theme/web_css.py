"""Render a `WebPalette` to a `:root { --simplex-* }` CSS variables block.

Consumed by two surfaces:
- the portal `<head>` (homepage cards + section pages)
- per-deck RevealJS HTML `<head>` (slide chrome, captions)

This module intentionally emits custom properties only. Surface-specific
stylesheets decide where those values apply, so a deck palette cannot
accidentally override the portal body, navbar, or other page chrome.

The returned string is a complete `<style>`-able block; callers wrap it in
`<style>` themselves so the same producer can also be written to a `.css`
file when needed.
"""

from simplex.theme.tokens import WebPalette


def render_web_css(palette: WebPalette) -> str:
    """Return a CSS variables block for `palette`."""
    return f""":root {{
  --simplex-accent: {palette.accent};
  --simplex-bg: {palette.background};
  --simplex-surface: {palette.surface};
  --simplex-text: {palette.text_primary};
  --simplex-text-muted: {palette.text_muted};
  --simplex-link: {palette.link};
  --simplex-code-bg: {palette.code_background};
  --simplex-font-sans: {palette.font_family_sans};
  --simplex-font-mono: {palette.font_family_mono};
  --simplex-font-size: {palette.font_size_base};
}}
"""
