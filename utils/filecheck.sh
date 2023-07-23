#!/usr/bin/env bash
# ShellChecked

set -eu
set -o pipefail

if grep -q CHECK "$1"; then
    diff -u --color=always \
        <(sed -n "s/\s*CHECK:\s*\(.*\)$/\1/p" "$1") \
        <(while read -r line; do echo "$line"; done)
fi
