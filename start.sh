#!/usr/bin/env bash

/opt/bin/start-selenium-standalone.sh &
sleep 3
python3 /web-watcher.py
