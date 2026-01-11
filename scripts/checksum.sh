#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/checksum.sh <file>
F=${1:?"file required"}
shasum -a 256 "$F" | awk '{print $1 "  " $2}' > "$F.sha256"
echo "Wrote $F.sha256"