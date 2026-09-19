@echo off
cd /d C:\ticketmaster-analytics
C:\ticketmaster-analytics\.venv\Scripts\python.exe src\refresh_pipeline.py > logs\pipeline.log 2>&1
