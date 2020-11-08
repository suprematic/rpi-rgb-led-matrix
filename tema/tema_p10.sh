#!/bin/bash 

cd "$(dirname "$0")"

./tema -s 0 -f fonts/6x10.bdf --led-rows=16 --led-row-addr-type=2 --led-multiplexing=3 $@
