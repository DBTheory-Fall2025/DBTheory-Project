#!/bin/sh
echo "================================================="
echo "Flask app starting..."
echo "Access the application at: http://localhost:51932"
echo "================================================="
exec flask run --host=0.0.0.0 --port=51932
