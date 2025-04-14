#!/bin/bash
# Run SIP model on several graphs

# Strict mode
set -o errexit -o nounset -o pipefail
IFS=$'\n\t'

# Variables
ERR_OUT=/dev/null

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
	case $1 in
		-e|--err)
			ERR_OUT=/dev/stderr
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

# Activate Python venv
source /home/etud/Bureau/projet/bin/activate

# SIP
cd "../src"
python3 sip.py --pattern stick	--target net --all 2> "$ERR_OUT"
python3 sip.py --pattern square --target net --all 2> "$ERR_OUT"
python3 sip.py --pattern pan	--target net --all 2> "$ERR_OUT"
