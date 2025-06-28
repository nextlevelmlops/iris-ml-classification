import os
from requests.auth import HTTPBasicAuth
from typing import Any
import requests
import pandas as pd

def get_databricks_token(
    host: str,
    client_id: str = None,
    client_secret: str = None,
    grant_type: str = "client_credentials",
    scope: str = "all-apis"
) -> str:
    """
    Retrieves an OAuth access token from a Databricks host using client credentials.
    
    If client_id or client_secret are not provided, the function will attempt to read them from environment variables.
    
    :param host: The Databricks workspace host URL.
    :param client_id: The OAuth client ID. If not provided, uses the DATABRICKS_CLIENT_ID environment variable.
    :param client_secret: The OAuth client secret. If not provided, uses the DATABRICKS_CLIENT_SECRET environment variable.
    :param grant_type: The OAuth grant type, defaulting to "client_credentials".
    :param scope: The OAuth scope, defaulting to "all-apis".
    :return: The OAuth access token as a string.
    """
    if client_id is None:
        client_id = os.environ["DATABRICKS_CLIENT_ID"]
    if client_secret is None:
        client_secret = os.environ["DATABRICKS_CLIENT_SECRET"]

    response = requests.post(
        f"{host}/oidc/v1/token",
        auth=HTTPBasicAuth(client_id, client_secret),
        data={
            'grant_type': grant_type,
            'scope': scope
        }
    )
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()["access_token"]


def call_serving_endpoint(
    serving_endpoint: str,
    token: str,
    input_df: pd.DataFrame,
    data_key: str = "dataframe_split"
) -> dict[str, Any]:
    """
    Calls a model serving endpoint with a DataFrame payload and returns the JSON response.

    Sends the input DataFrame as a JSON payload using the specified key and authenticates using a bearer token.

    :param serving_endpoint: The URL of the serving endpoint.
    :param token: Bearer token for authentication.
    :param input_df: Input DataFrame to send as JSON.
    :param data_key: Key for the JSON payload (default: 'dataframe_split').
    :return: The JSON response from the endpoint.
    """
    headers = {"Authorization": f"Bearer {token}"}
    payload = {data_key: input_df.to_dict(orient="split")}
    response = requests.post(serving_endpoint, headers=headers, json=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()
