export PYTHONPATH=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS=/home/meirlejz/gpt_app/config/sql_credentials.json
uvicorn backend.app.app:app --reload --host 172.21.56.72
