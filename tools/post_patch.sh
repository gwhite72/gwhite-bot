#!/usr/bin/env bash
# Post-conversion fixups: Traditional terms can be 1 character longer than the
# Simplified originals, overflowing a few fixed buffers that upstream sized for
# Simplified byte lengths. Enlarge those specific buffers. Idempotent.
set -euo pipefail
FW="$1"

f="$FW/applications/external/can_commander/scenes/custom_inject_slot_menu.c"
if [ -f "$f" ]; then
  sed -i -E 's/static char (cancommander_custom_slot_[a-z]+_item)\[[0-9]+\];/static char \1[40];/' "$f"
fi
echo "post_patch done"
