#!/usr/bin/env bash
# check.sh - run every py04 exercise against the subject's expected output.
#
#   ./check.sh              run every case
#   ./check.sh -c           test exN/color/*_vc.py instead
#   ./check.sh ex1          run only cases whose name starts with "ex1"
#   ./check.sh -v           show full stdout/stderr for every case, pass or fail
#   ./check.sh -v ex2-denied
#
# Every run also writes a line-by-line trace to expected/traces.txt: your
# output and the expected output side by side, with a '!' on every line that
# differs. Override the path with TRACE_FILE=/somewhere/else.txt ./check.sh
#
# Each case in cases/ is a set of files sharing one name:
#   NAME.args   argv, one per line   (optional; absent = no arguments)
#   NAME.in     stdin                (optional; absent = /dev/null, i.e. EOF)
#   NAME.out    expected stdout      (required)
#   NAME.err    expected stderr      (optional; absent = stderr must be EMPTY)
#
# stdout and stderr are captured SEPARATELY - never merged. That is the whole
# point of ex2, and it means a crash shows up as a traceback on stderr rather
# than as mysterious "wrong output".

set -u

here="$(cd "$(dirname "$0")" && pwd)"
mod="$here/.."
cases="$here/cases"

verbose=0
filter=""
colorver=0
for arg in "$@"; do
    case "$arg" in
        -v|--verbose) verbose=1 ;;
        -c|--color)   colorver=1 ;;
        -*) echo "unknown option: $arg" >&2; exit 2 ;;
        *)  filter="$arg" ;;
    esac
done

# NOT an associative array: macOS ships bash 3.2, which has no `declare -A`.
# A case statement works in every shell you will meet, school Macs included.
src_for() {
    case "$1" in
        ex0) echo ft_ancient_text.py ;;
        ex1) echo ft_archive_creation.py ;;
        ex2) echo ft_stream_management.py ;;
        ex3) echo ft_vault_security.py ;;
        *)   echo "" ;;
    esac
}

# `timeout` is GNU coreutils and is absent on stock macOS. Use it when it is
# there, run bare when it is not - a missing watchdog is better than a
# tester that refuses to start.
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT="timeout 10"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT="gtimeout 10"
else
    TIMEOUT=""
fi

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; DIM=$'\033[2m'; OFF=$'\033[0m'

# --- traces.txt -------------------------------------------------------------
# Plain text, no colours: it is meant to be read in an editor and diffed.
trace="${TRACE_FILE:-$here/traces.txt}"
: > "$trace"
{
    printf 'py04 trace - %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'filter: %s\n' "${filter:-<none>}"
    printf "'!' marks a line where your output and the expected output differ.\n"
} >> "$trace"

# Pair two files line by line. Not `paste`: this marks the differing lines and
# shows <missing> where one side ran out, which is the whole point.
#
# FILENAME == f1 rather than the usual NR == FNR: when the first file is EMPTY,
# NR == FNR is still true for the SECOND file's lines and every "got" line
# would be filed as expected output. An empty stderr is the normal case here,
# so that bug would fire constantly.
pair_lines() {
    awk -v f1="$1" -v w=60 '
        FILENAME == f1 { g[FNR] = $0; gn = FNR; next }
        { e[FNR] = $0; en = FNR }
        END {
            n = (gn > en ? gn : en)
            if (n == 0) { print "      (both empty)"; exit }
            printf "      %4s | %-*s | %s\n", "line", w, "got", "expected"
            for (i = 1; i <= n; i++) {
                gv = (i <= gn ? g[i] : "<missing>")
                ev = (i <= en ? e[i] : "<missing>")
                printf "    %s %4d | %-*s | %s\n", \
                       (gv == ev ? " " : "!"), i, w, gv, ev
            }
        }
    ' "$1" "$2"
}

pass=0; fail=0; skip=0

for expfile in "$cases"/*.out; do
    name="$(basename "$expfile" .out)"
    [ -n "$filter" ] && case "$name" in "$filter"*) ;; *) continue ;; esac

    ex="${name%%-*}"
    base="$(src_for "$ex")"
    if [ "$colorver" = 1 ]; then
        # the signature-style variant in exN/color/
        src="$mod/$ex/color/${base%.py}_vc.py"
    else
        src="$mod/$ex/$base"
    fi

    if [ ! -s "$src" ]; then
        printf '  %sSKIP%s    %-16s %s(%s is empty or missing)%s\n' \
               "$YEL" "$OFF" "$name" "$DIM" "$ex/$base" "$OFF"
        printf '\n=== %s === SKIP (%s is empty or missing)\n' \
               "$name" "$ex/$base" >> "$trace"
        skip=$((skip + 1))
        continue
    fi

    # isolated working directory so writes never touch the repo
    work="$(mktemp -d)"
    cp "$here/ancient_fragment.txt" "$work/"
    cp "$src" "$work/$base"

    args=()
    [ -f "$cases/$name.args" ] && while IFS= read -r line; do
        [ -n "$line" ] && args+=("$line")
    done < "$cases/$name.args"

    stdin_file=/dev/null
    [ -f "$cases/$name.in" ] && stdin_file="$cases/$name.in"

    # ${args[@]+"${args[@]}"} - under `set -u`, bash 3.2 treats "${args[@]}"
    # on an EMPTY array as an unbound variable and aborts. This guard is what
    # keeps the no-argument case (ex0-usage) working on a school Mac.
    ( cd "$work" && $TIMEOUT python3 "$base" ${args[@]+"${args[@]}"} \
        < "$stdin_file" > "$work/.got.out" 2> "$work/.got.err" )
    rc=$?

    got_out="$work/.got.out"; got_err="$work/.got.err"
    want_err="$cases/$name.err"
    [ -f "$want_err" ] || { : > "$work/.want.err"; want_err="$work/.want.err"; }

    out_ok=0; err_ok=0
    diff -q "$got_out" "$expfile"  >/dev/null 2>&1 && out_ok=1
    diff -q "$got_err" "$want_err" >/dev/null 2>&1 && err_ok=1

    crashed=0
    grep -q 'Traceback (most recent call last)' "$got_err" 2>/dev/null && crashed=1

    if [ "$out_ok" = 1 ] && [ "$err_ok" = 1 ]; then
        printf '  %sOK%s      %-16s %sexit %d%s\n' \
               "$GRN" "$OFF" "$name" "$DIM" "$rc" "$OFF"
        pass=$((pass + 1))
        [ "$verbose" = 1 ] && {
            printf '%s' "$DIM"; sed 's/^/            | /' "$got_out"; printf '%s' "$OFF"
        }
    else
        printf '  %sFAIL%s    %-16s %sexit %d%s\n' \
               "$RED" "$OFF" "$name" "$DIM" "$rc" "$OFF"
        fail=$((fail + 1))

        if [ "$crashed" = 1 ]; then
            printf '          %sCRASHED - traceback:%s\n' "$RED" "$OFF"
            sed 's/^/            /' "$got_err"
        else
            [ "$out_ok" = 0 ] && {
                printf '          %s--- stdout (< yours, > expected) ---%s\n' "$YEL" "$OFF"
                diff "$got_out" "$expfile" | sed 's/^/            /' | head -30
            }
            [ "$err_ok" = 0 ] && {
                printf '          %s--- stderr (< yours, > expected) ---%s\n' "$YEL" "$OFF"
                diff "$got_err" "$want_err" | sed 's/^/            /' | head -20
            }
        fi
    fi

    [ "$verbose" = 1 ] && [ -s "$got_err" ] && [ "$crashed" = 0 ] && {
        printf '          %sstderr:%s\n' "$DIM" "$OFF"
        sed 's/^/            /' "$got_err"
    }

    argv_str="<none>"
    [ "${#args[@]}" -gt 0 ] && argv_str="${args[*]}"

    {
        printf '\n=== %s ===\n' "$name"
        printf '    source : %s\n' "$ex/$base"
        printf '    argv   : %s\n' "$argv_str"
        printf '    stdin  : %s\n' \
               "$([ "$stdin_file" = /dev/null ] && echo '<empty>' \
                  || echo "cases/$name.in")"
        printf '    exit   : %d\n' "$rc"
        printf '    result : stdout %s, stderr %s\n' \
               "$([ "$out_ok" = 1 ] && echo OK || echo DIFFERS)" \
               "$([ "$err_ok" = 1 ] && echo OK || echo DIFFERS)"
        printf '\n    --- stdout ---\n'
        pair_lines "$got_out" "$expfile"
        printf '\n    --- stderr ---\n'
        pair_lines "$got_err" "$want_err"
    } >> "$trace"

    rm -rf "$work"
done

printf '\n  %d passed, %d failed, %d skipped\n' "$pass" "$fail" "$skip"
printf '\n%d passed, %d failed, %d skipped\n' "$pass" "$fail" "$skip" >> "$trace"
printf '  %strace: %s%s\n' "$DIM" "$trace" "$OFF"
[ "$fail" -eq 0 ]
