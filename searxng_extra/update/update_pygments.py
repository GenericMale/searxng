#!/usr/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Update pygments style

Call this script after each upgrade of pygments

"""
# pylint: disable=too-few-public-methods

from pathlib import Path
import pygments
from pygments.formatters.html import HtmlFormatter

from searx import searx_dir

FILE_LIGHT_THEME = Path(searx_dir) / 'static/styles/light/pygments.css'
FILE_DARK_THEME = Path(searx_dir) / 'static/styles/dark/pygments.css'

HEADER = f"""\
/*
   this file is generated automatically by searxng_extra/update/update_pygments.py
   using pygments version {pygments.__version__}
*/

.code-highlight {{
"""

FOOTER = """
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


def generate_css(style) -> str:
    css = HEADER
    for line in Formatter(style=style).get_style_lines():
        css += '\n  ' + line
    css += FOOTER
    return css


if __name__ == '__main__':
    print("update: %s" % FILE_LIGHT_THEME)
    with FILE_LIGHT_THEME.open('w', encoding='utf8') as f:
        f.write(generate_css('default'))

    print("update: %s" % FILE_DARK_THEME)
    with FILE_DARK_THEME.open('w', encoding='utf8') as f:
        f.write(generate_css('lightbulb'))
