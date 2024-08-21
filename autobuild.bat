@echo off
call "venv\Scripts\activate"

:: requirements.txt 설치
pip install -r requirements.txt

:: 메인 파이썬 스크립트 실행
python "C:\code\AnalyticsLog\main.py"

pause