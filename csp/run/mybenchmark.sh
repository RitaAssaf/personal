#!/bin/bash
# Run SIP model on several graphs

# Strict mode
set -o errexit -o nounset -o pipefail
IFS=$'\n\t'

# Variables
ERR_OUT=/dev/null
MODLER=pycsp3

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
	case $1 in

		-m|--modler)
			shift
			MODLER="$1"
			shift
		;;
		-*)
			>&2 echo "Unknown option $1"
			exit 1
		;;
		*)
			POSITIONAL_ARGS+=("$1")
			shift
		;;
  esac
done
set -- "${POSITIONAL_ARGS[@]}"

# Go to script directory
cd "$(dirname "$0")"

# Activate Python venv
source ../py_venv/bin/activate

# SIP
cd ../src
#python3 solve_sip1.py --modler "$MODLER" --pattern pan		--target net --all 2> "$ERR_OUT"
#python3 solve_sip1.py --modler "$MODLER" --pattern wellFormed		--target targetBizarre --all 2> "$ERR_OUT"
python3 solve_sip1.py --modler "$MODLER" --pattern pan		--target targetLarge --all 2> "$ERR_OUT"

