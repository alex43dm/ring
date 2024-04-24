#!/bin/sh
st-info --probe
st-flash erase
st-flash --reset write build/rng01.bin 0x08000000
