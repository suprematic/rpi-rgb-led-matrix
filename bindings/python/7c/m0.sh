#!/bin/bash

set -eu

cd $(dirname $0)
python3 ./m0.py --led-cols=32 --led-rows=16 --led-slowdown-gpio=5 --led-multiplexing=4 --led-row-addr-type=0 --led-parallel=2 --led-chain=3 $*
