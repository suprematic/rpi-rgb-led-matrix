#!/bin/bash 

cd "$(dirname "$0")"

# Extra options:
#  1) fix for Raspberry Pi 4 (s. issue 861)
#    --led-slowdown-gpio=2
#  2) options for LysonLed SMD3535 16*32 P8_1_4_3535_PR4538_HSD
#    --led-rows=16 --led-multiplexing=8

./tema -s 0 -f fonts/6x10.bdf --led-slowdown-gpio=2 --led-rows=16 --led-multiplexing=8 $@
