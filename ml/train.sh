#!/usr/bin/env bash
DATA=ml/data.yaml
WEIGHTS=yolov8n.pt
IMG=640
BATCH=16
EPOCHS=100
PROJECT=runs/whirly
NAME=exp1

python ml/train_yolov8.py --data $DATA --img $IMG --batch $BATCH --epochs $EPOCHS --weights $WEIGHTS --project $PROJECT --name $NAME --amp