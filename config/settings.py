import os

SECRET_KEY = os.getenv("SECRET_KEY", "LoremIpsum123")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "8000"))
)
