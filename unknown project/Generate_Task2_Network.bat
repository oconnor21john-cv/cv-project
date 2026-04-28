@echo off
title Task 2 Network Generator
color 0A

echo.
echo ========================================
echo    TASK 2 NETWORK GENERATOR
echo ========================================
echo.
echo This will create all your Packet Tracer
echo configuration files automatically!
echo.
pause

echo.
echo Starting network generation...
echo.

python run_task2_generator.py

echo.
echo Generation complete!
echo.
pause

