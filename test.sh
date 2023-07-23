#!/usr/bin/env bash
# ShellChecked

set -eu
set -o pipefail

if [ -n "$(command -v FileCheck)" ]; then
    FC=FileCheck
else
    FC=utils/filecheck.sh
fi

for file in examples/*.spill; do
    echo "./spill $file | $FC $file"
    ./spill "$file" | "$FC" "$file"
done
