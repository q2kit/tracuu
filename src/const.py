import os

import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

LOCAL_ENV = "local"
DEVELOPMENT_ENV = "development"
PRODUCTION_ENV = "production"

ENV = os.getenv("ENV", LOCAL_ENV)
if ENV not in {LOCAL_ENV, DEVELOPMENT_ENV, PRODUCTION_ENV}:
    raise ValueError(  # noqa: TRY003
        f"Invalid environment: {ENV}. Expected {LOCAL_ENV}, {DEVELOPMENT_ENV} or {PRODUCTION_ENV}.",  # noqa: E501, EM102
    )

SERVER_HOST = os.getenv("SERVER_HOST", "localhost")

CODE_MAX_LENGTH = 100
IMAGE_MAX_SIZE_MB = 15
IMAGE_ALLOWED_TYPES = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/webp"]

NORMAL_IMAGE_EXPIRY_SECONDS = 24 * 60 * 60  # 1 day
SEARCH_API_IMAGE_EXPIRY_SECONDS = 3 * 60  # 3 minutes
