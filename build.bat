@echo off
pip install pyinstaller
pyinstaller --onefile app.py --name VPNLeakScanner
pause
