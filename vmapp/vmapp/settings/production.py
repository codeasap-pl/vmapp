import os
from .defaults import *  # noqa: 401


DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1"]
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this")
