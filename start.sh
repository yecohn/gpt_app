<<<<<<< HEAD
export PYTHONPATH=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS=/home/meirlejz/gpt_app/config/sql_credentials.json
uvicorn backend.app.app:app --reload --host 172.21.56.72
=======
export GOOGLE_APPLICATION_CREDENTIALS="/Users/yosh/Desktop/projects/gpt/config/sql_credentials.json"
export PYTHONPATH=${PWD}
uvicorn backend.app.app:app --reload
>>>>>>> 67e19a01f49eaa31c3ee64ccbd75cbcf5ecf5ce9
