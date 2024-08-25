#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-or-later

declare _Blue
declare _creset

themes.help(){
    cat <<EOF
themes.:
  live      : to get live builds of CSS & JS use 'make run'
  build     : build theme
  test      : test theme
EOF
}

themes.live() {
    build_msg GRUNT "theme (live build)"
    nodejs.ensure
    {
        npm install
        npm run watch
    } 2>&1 \
        | prefix_stdout "${_Blue}THEME ${1} ${_creset}  " \
        | grep -E --ignore-case --color 'error[s]?[:]? |warning[s]?[:]? |'
}

themes.build() {
    (   set -e
        pygments.less
        node.env
        build_msg GRUNT "theme"
        npm run build
    )
    dump_return $?
}

themes.test() {
    build_msg TEST "theme"
    nodejs.ensure
    npm install
    npm run test
    dump_return $?
}
