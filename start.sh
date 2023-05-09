export GOOGLE_APPLICATION_CREDENTIALS="/Users/yosh/Desktop/projects/gpt/config/sql_credentials.json"
export PYTHONPATH=${PWD}
uvicorn backend.app.app:app --reload
