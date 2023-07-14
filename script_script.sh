#!/bin/bash
python findIntrinsicValue.py -S $1
python findStickerPrice.py -S $1
python screenSystemOne_yf.py -S $1
