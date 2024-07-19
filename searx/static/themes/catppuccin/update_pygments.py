#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Update pygments style

Call this script after each upgrade of pygments

"""
# pylint: disable=too-few-public-methods

from pathlib import Path
import pygments
from pygments.formatters.html import HtmlFormatter
from os.path import dirname
from pygments.styles import get_style_by_name

LESS_FILE = Path(dirname(__file__)) / 'src/generated/pygments.less'

HEADER = f"""\
/*
   this file is generated automatically by searxng_extra/update/update_pygments.py
   using pygments version {pygments.__version__}
*/

"""

START_LATTE_THEME = """
.code-highlight {
"""

END_LATTE_THEME = """
}
"""

START_FRAPPE_THEME = """
.code-highlight-frappe(){
  .code-highlight {
"""

START_MACCHIATO_THEME = """
.code-highlight-macchiato(){
  .code-highlight {
"""

START_MOCHA_THEME = """
.code-highlight-mocha(){
  .code-highlight {
"""

END_DARK_THEME = """
  }
}
"""


class Formatter(HtmlFormatter):  # pylint: disable=missing-class-docstring
    @property
    def _pre_style(self):
        return 'line-height: 100%;'

    def get_style_lines(self, arg=None):
        style_lines = []
        style_lines.extend(self.get_linenos_style_defs())
        style_lines.extend(self.get_background_style_defs(arg))
        style_lines.extend(self.get_token_style_defs(arg))
        return style_lines


def generat_css() -> str:
    css = HEADER + START_LATTE_THEME
    for line in Formatter(style='catppuccin-latte').get_style_lines():
        css += '\n  ' + line
    css += END_LATTE_THEME + START_FRAPPE_THEME
    for line in Formatter(style='catppuccin-frappe').get_style_lines():
        css += '\n    ' + line
    css += END_DARK_THEME + START_MACCHIATO_THEME
    for line in Formatter(style='catppuccin-macchiato').get_style_lines():
        css += '\n    ' + line
    css += END_DARK_THEME + START_MOCHA_THEME
    for line in Formatter(style='catppuccin-mocha').get_style_lines():
        css += '\n    ' + line
    css += END_DARK_THEME
    return css


if __name__ == '__main__':
    print("update: %s" % LESS_FILE)
    with LESS_FILE.open('w', encoding='utf8') as f:
        f.write(generat_css())
