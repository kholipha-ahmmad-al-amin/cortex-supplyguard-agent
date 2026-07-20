@echo off
title Snowflake CoCo CLI - Web Dashboard Server
echo Opening browser to http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
py -3 main.py --web
pause
