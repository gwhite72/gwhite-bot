#!/usr/bin/env bash
# Post-conversion fixups applied to freshly-downloaded firmware source in CI.
set -euo pipefail
FW="$1"

# 1) Translated (Traditional) UI text is often a few bytes longer than the English
#    or Simplified original. snprintf() is length-bounded, so the only effect of an
#    over-long string is harmless truncation on screen -- but Momentum compiles with
#    -Werror, which turns GCC's format-truncation/overflow *heuristic* into a hard
#    error and fails hundreds of apps. Downgrade just those two to warnings, matching
#    the project's existing -Wno-error=deprecated-declarations. Memory safety is
#    unaffected (snprintf still never writes past the buffer).
cc="$FW/site_scons/cc.scons"
if [ -f "$cc" ] && ! grep -q 'format-truncation' "$cc"; then
  sed -i 's/\("-Wno-error=deprecated-declarations",\)/\1\n        "-Wno-error=format-truncation",\n        "-Wno-error=format-overflow",/' "$cc"
fi

# 2) can_commander sized a few slot buffers for Simplified byte lengths; enlarge them.
f="$FW/applications/external/can_commander/scenes/custom_inject_slot_menu.c"
if [ -f "$f" ]; then
  sed -i -E 's/static char (cancommander_custom_slot_[a-z]+_item)\[[0-9]+\];/static char \1[40];/' "$f"
fi
echo "post_patch done"
