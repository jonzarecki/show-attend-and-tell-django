#!/usr/bin/env bash

# cd showattendtell-tensorflow
# pip install -r requirements.txt
# chmod +x ./download.sh
# ./download.sh

# python resize.py


python prepro.py
python train.py &
tensorboard --logdir='./log' --port=6005