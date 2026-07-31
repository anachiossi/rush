#!/usr/bin/env bash
# check.sh - run the deterministic py03 exercises against the
# subject's expected output.
#
#   ./check.sh                run every case against ex*/ft_*.py
#   ./check.sh ex1            only cases whose name starts with "ex1"
#   ./check.sh -a 3           test ex*/alt/ft_*_v3.py instead
#   ./check.sh -c             test ex*/color/ft_*_vc.py instead
#   ./check.sh -a 3 ex4       both
#   ./check.sh -v ex1-mixed   verbose: show output even when passing
#
# Covers ex0, ex1, ex2 and ex4 - the exercises whose output is fully
# determined by their input. ex3, ex5 and ex6 use random, so their
# output cannot be compared literally: use ./properties.py for those.
#
# Each case in cases/ is a set of files sharing one name:
#   NAME.args   argv, one per line   (optional; absent = no arguments)
#   NAME.in     stdin                (optional; absent = /dev/null, i.e. EOF)
#   NAME.out    expected stdout      (required)
#   NAME.err    expected stderr      (optional; absent = stderr must be EMPTY)
#
# stdout and stderr are captured SEPARATELY, never merged, so a crash
# shows up as a traceback on stderr rather than as a confusing diff.
#
# IMPORTANT: the source under test is copied into a temp directory under
# its CANONICAL name (ft_score_analytics.py, never ft_score_analytics_v3.py)
# so that argv[0] is identical for every version. ex1 prints argv[0] in its
# usage line, so without this an alt version could never match.

set -u

here="$(cd "$(dirname "$0")" && pwd)"
mod="$here/.."
cases="$here/cases"

verbose=0
filter=""
altver=""
colorver=0
while [ $# -gt 0 ]; do
    case "$1" in
        -v|--verbose) verbose=1 ;;
        -a|--alt)     shift; altver="${1:-}" ;;
        -c|--color)   colorver=1 ;;
        -*) echo "unknown option: $1" >&2; exit 2 ;;
        *)  filter="$1" ;;
    esac
    shift
done

# NOT an associative array: macOS ships bash 3.2, which has no `declare -A`.
src_for() {
    case "$1" in
        ex0) echo ft_command_quest.py ;;
        ex1) echo ft_score_analytics.py ;;
        ex2) echo ft_coordinate_system.py ;;
        ex3) echo ft_achievement_tracker.py ;;
        ex4) echo ft_inventory_system.py ;;
        ex5) echo ft_data_stream.py ;;
        ex6) echo ft_data_alchemist.py ;;
        *)   echo "" ;;
    esac
}

# `timeout` is GNU coreutils and absent on stock macOS. Use it when it is
# there, run bare when it is not.
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT="timeout 10"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT="gtimeout 10"
else
    TIMEOUT=""
fi

RED=$'\033[31m'; GRN=$'\033[32m'; YEL=$'\033[33m'; DIM=$'\033[2m'; OFF=$'\033[0m'

if [ -n "$altver" ]; then
    printf '  %stesting alt version v%s%s\n\n' "$DIM" "$altver" "$OFF"
fi
if [ "$colorver" = 1 ]; then
    printf '  %stesting signature-style color/ versions%s\n\n' "$DIM" "$OFF"
fi

# --- traces.txt -------------------------------------------------------------
# Plain text, no colours: meant to be read in an editor. Every run rewrites it
# with your output and the expected output side by side, for EVERY case - not
# just the failing ones - so you can see what a passing case looks like too.
# Override the path with TRACE_FILE=/somewhere/else.txt ./check.sh
trace="${TRACE_FILE:-$here/traces.txt}"
: > "$trace"
{
    printf 'py03 trace - %s\n' "$(date '+%Y-%m-%d %H:%M:%S')"
    printf 'target: %s\n' \
           "$([ -n "$altver" ] && echo "alt version v$altver" || echo 'ex*/ft_*.py')"
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
    canonical="$(src_for "$ex")"
    if [ -z "$canonical" ]; then
        continue
    fi

    if [ "$colorver" = 1 ]; then
        # the signature-style variant in exN/color/
        src="$mod/$ex/color/${canonical%.py}_vc.py"
    elif [ -n "$altver" ]; then
        stem="${canonical%.py}"
        src="$mod/$ex/alt/${stem}_v${altver}.py"
    else
        src="$mod/$ex/$canonical"
    fi

    # "Not written yet" is not the same as "empty file": the exercise
    # skeletons ship with a shebang and a comment header. Treat a file
    # with no line whose first non-blank character is anything but '#'
    # as unimplemented, so an untouched skeleton SKIPs instead of
    # failing every case with empty output.
    if [ ! -f "$src" ] \
       || ! grep -qE '^[[:space:]]*[^#[:space:]]' "$src" 2>/dev/null; then
        printf '  %sSKIP%s    %-16s %s(%s not written yet)%s\n' \
               "$YEL" "$OFF" "$name" "$DIM" "${src#$mod/}" "$OFF"
        printf '\n=== %s === SKIP (%s not written yet)\n' \
               "$name" "${src#$mod/}" >> "$trace"
        skip=$((skip + 1))
        continue
    fi

    work="$(mktemp -d)"
    # canonical name so argv[0] matches the subject for every version
    cp "$src" "$work/$canonical"

    args=()
    [ -f "$cases/$name.args" ] && while IFS= read -r line; do
        [ -n "$line" ] && args+=("$line")
    done < "$cases/$name.args"

    stdin_file=/dev/null
    [ -f "$cases/$name.in" ] && stdin_file="$cases/$name.in"

    # ${args[@]+"${args[@]}"} - under `set -u`, bash 3.2 aborts on
    # "${args[@]}" when the array is empty. This guard keeps the
    # no-argument cases working on a school Mac.
    ( cd "$work" && $TIMEOUT python3 "$canonical" ${args[@]+"${args[@]}"} \
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

    argv_str="<none>"
    [ "${#args[@]}" -gt 0 ] && argv_str="${args[*]}"

    {
        printf '\n=== %s ===\n' "$name"
        printf '    source : %s\n' "${src#$mod/}"
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
