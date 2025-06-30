import pytest
import pandas as pd
from unittest.mock import patch
from src.iris_ml_classification.api import get_databricks_token, call_serving_endpoint


# ---------- Tests for get_databricks_token ----------

@patch("src.iris_ml_classification.api.requests.post")
def test_get_databricks_token_success(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"access_token": "mocked_token"}

    token = get_databricks_token(
        host="https://test-host",
        client_id="test_client_id",
        client_secret="test_client_secret"
    )

    assert token == "mocked_token"
    mock_post.assert_called_once()
    assert mock_post.call_args[1]["auth"].username == "test_client_id"


@patch.dict("os.environ", {
    "DATABRICKS_CLIENT_ID": "env_client_id",
    "DATABRICKS_CLIENT_SECRET": "env_client_secret"
})
@patch("src.iris_ml_classification.api.requests.post")
def test_get_databricks_token_with_env(mock_post):
    mock_response = mock_post.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"access_token": "env_token"}

    token = get_databricks_token(host="https://test-host")
    assert token == "env_token"
    mock_post.assert_called_once()


@patch("src.iris_ml_classification.api.requests.post")
def test_get_databricks_token_failure(mock_post):
    mock_post.return_value.raise_for_status.side_effect = Exception("HTTP error")

    with pytest.raises(Exception, match="HTTP error"):
        get_databricks_token("https://test-host", "id", "secret")


# ---------- Tests for call_serving_endpoint ----------

@patch("src.iris_ml_classification.api.requests.post")
def test_call_serving_endpoint_success(mock_post):
    df = pd.DataFrame([[1, 2, 3, 4]], columns=["a", "b", "c", "d"])

    mock_response = mock_post.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"predictions": ["setosa"]}

    result = call_serving_endpoint("https://endpoint", "fake_token", df)

    assert result == {"predictions": ["setosa"]}
    mock_post.assert_called_once()
    assert mock_post.call_args[1]["headers"]["Authorization"] == "Bearer fake_token"


@patch("src.iris_ml_classification.api.requests.post")
def test_call_serving_endpoint_failure(mock_post):
    df = pd.DataFrame([[1, 2, 3, 4]], columns=["a", "b", "c", "d"])

    mock_post.return_value.raise_for_status.side_effect = Exception("Bad Request")

    with pytest.raises(Exception, match="Bad Request"):
        call_serving_endpoint("https://endpoint", "fake_token", df)
