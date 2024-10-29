#!/usr/bin/env bash

/opt/bin/entry_point.sh &
sleep 5
python3 /web-watcher.py
