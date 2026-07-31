#!/usr/bin/env bash
# check.sh - diff every py02 exercise against the subject's expected output.
#
#   usage:  ./check.sh [path-to-py02-exceptions]
#   lives in py02-exceptions/expected/, so the module is one level up.

here="$(cd "$(dirname "$0")" && pwd)"
mod="${1:-$here/..}"

if [ ! -d "$mod" ]; then
    echo "module not found: $mod" >&2
    exit 2
fi

declare -A SRC=(
    [ex0]=ft_first_exception.py
    [ex1]=ft_raise_exception.py
    [ex2]=ft_different_errors.py
    [ex3]=ft_custom_errors.py
    [ex4]=ft_finally_block.py
)

pass=0
fail=0

for ex in ex0 ex1 ex2 ex3 ex4; do
    src="$mod/$ex/${SRC[$ex]}"
    exp="$here/$ex.txt"

    if [ ! -f "$src" ]; then
        printf '  MISSING  %s\n' "$src"
        fail=$((fail + 1))
        continue
    fi

    got=$(cd "$mod/$ex" && python3 "${SRC[$ex]}" </dev/null 2>&1)

    if diff -q <(printf '%s\n' "$got") "$exp" >/dev/null 2>&1; then
        printf '  \033[32mOK      \033[0m %s\n' "$ex/${SRC[$ex]}"
        pass=$((pass + 1))
    else
        printf '  \033[31mDIFFERS \033[0m %s\n' "$ex/${SRC[$ex]}"
        diff <(printf '%s\n' "$got") "$exp" \
            | sed 's/^/           /' | head -20
        fail=$((fail + 1))
    fi
done

printf '\n  %d matching, %d differing\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
