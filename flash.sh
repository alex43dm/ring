#!/bin/sh

st-flash --reset write build/rng01.bin 0x08000000
