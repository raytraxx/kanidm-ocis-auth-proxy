import os

SECRET_KEY = os.getenv("SECRET_KEY", "LoremIpsum123")
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "8000"))
)

SCHEME = os.getenv("SCHEME", "http" if SERVER_NAME.startswith("localhost") else "https")
BASE_URL = f"{SCHEME}://{SERVER_NAME}"
IDM_BASE_URL = os.getenv("IDM_BASE_URL", "http://localhost:{0}".format(os.getenv("PORT", "8000")))
