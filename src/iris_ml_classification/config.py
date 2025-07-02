"""
Configuration utilities for serving endpoint settings.

This module defines the `Config` class, which loads environment variables and constructs
the serving endpoint URL for the Iris ML Classification service.

Classes:
    Config: Loads environment variables and constructs endpoint URLs.

Attributes:
    config (Config): An instance of the Config class for convenience.
"""

import os


class Config:
    """Configuration class for serving endpoint settings.

    This class loads environment variables and constructs the serving endpoint URL.
    """

    # ENDPOINT_NAME = os.getenv("ENDPOINT_NAME", "iris-classification-model-serving")
    ENDPOINT_NAME = os.getenv("ENDPOINT_NAME", "iris-classification-basic-model-serving")
    HOST = os.getenv("DATABRICKS_HOST", "")
    HOST = HOST if HOST.startswith("https://") else f"https://{HOST}"
    SERVING_ENDPOINT = f"{HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations"


config = Config()
