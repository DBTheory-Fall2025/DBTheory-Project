#!/bin/sh
BANNER="
==================================================
Flask app starting...
Access the application at: http://localhost:51932
=================================================="
sleep 1 && echo "$BANNER" &
flask --debug run --host=0.0.0.0 --port=51932
