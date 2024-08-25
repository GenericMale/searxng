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

PYGMENTS_CSS_FILES = {
    'static/styles/dark/pygments.css': 'lightbulb',
    'static/styles/frappe/pygments.css': 'catppuccin-frappe',
    'static/styles/latte/pygments.css': 'catppuccin-latte',
    'static/styles/light/pygments.css': 'default',
    'static/styles/macchiato/pygments.css': 'catppuccin-macchiato',
    'static/styles/mocha/pygments.css': 'catppuccin-mocha',
}

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


def generate_css(style_name) -> str:
    css = HEADER
    for line in Formatter(style=style_name).get_style_lines():
        css += '\n  ' + line
    css += FOOTER
    return css


if __name__ == '__main__':
    for file, style in PYGMENTS_CSS_FILES.items():
        print("update: %s" % file)
        with open(Path(searx_dir) / file, 'w', encoding='utf-8') as f:
            f.write(generate_css(style))
