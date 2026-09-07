@echo off
echo ===================================================
echo Starting NEPSE Cognitive Triad AI Trader Services
echo ===================================================

echo [1/2] Launching API Server on http://localhost:8000
start "NEPSE API Server :8000" /min python -u server.py

echo [2/2] Launching Mission Control UI on http://localhost:3000
start "NEPSE Mission Control :3000" /min python -u ui_server.py

echo.
echo Both servers started!
echo - Mission Control Dashboard: http://localhost:3000
echo - Interactive API Docs:      http://localhost:8000/docs
echo.
pause
