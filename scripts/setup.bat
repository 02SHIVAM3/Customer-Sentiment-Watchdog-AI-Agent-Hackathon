\
@echo off
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
echo.
echo Edit .env to add your SLACK_WEBHOOK.
echo Done.
