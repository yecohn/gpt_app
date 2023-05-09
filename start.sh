export PYTHONPATH=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="${PWD}/config/sql_credentials.json"
echo $GOOGLE_APPLICATION_CREDENTIALS
uvicorn backend.app.app:app --reload
