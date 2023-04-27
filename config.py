import os
import json

with open("config.json", "r") as f:
    SQL_CONF = json.load(f)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SQL_CONF[
    "GOOGLE_APPLICATION_CREDENTIALS"
]
os.environ["INSTANCE_CONNECTION_NAME"] = SQL_CONF["INSTANCE_CONNECTION_NAME"]
os.environ["DB_PORT"] = SQL_CONF["DB_PORT"]
os.environ["DB_NAME"] = SQL_CONF["DB_NAME"]
os.environ["DB_USER"] = SQL_CONF["DB_USER"]
os.environ["DB_PASS"] = SQL_CONF["DB_PASS"]
