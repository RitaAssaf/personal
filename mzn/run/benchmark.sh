#!/bin/bash
# Run SIP model with PyCSP3 on several graphs

set -o errexit -o nounset -o pipefail
IFS=$'\n\t'

# Variables
ERR_OUT=/dev/null

# Activate Python virtual environment
source /home/etud/Bureau/projet/bin/activate



# SIP
cd "../src"
python3 sip2.py "../dat/stick.dot" "../dat/net_2.dot" > "../res/stick_in_net_2.txt"
python3 sip2.py "../dat/square.dot" "../dat/net.dot" 2> "$ERR_OUT"
python3 sip2.py "../dat/pan.dot" "../dat/net.dot" 2> "$ERR_OUT"
