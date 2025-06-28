import os
# After (centralized config)
class Config:
    ENDPOINT_NAME = os.getenv("ENDPOINT_NAME", "iris-classification-model-serving")
    HOST = os.getenv("DATABRICKS_HOST", "")
    HOST = HOST if HOST.startswith("https://") else f"https://{HOST}"
    SERVING_ENDPOINT = f"{HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations"

config = Config()