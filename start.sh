#!/usr/bin/env bash
export SRC_DIR=$(cd "$(dirname "$0")"; pwd)

screen -S Telegrambot -d -m python3 ${SRC_DIR}/main.py
