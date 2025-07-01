from unittest.mock import patch, MagicMock
from src.iris_ml_classification.app import main

@patch("src.iris_ml_classification.app.display_result")
@patch("src.iris_ml_classification.app.st")
@patch("src.iris_ml_classification.app.call_serving_endpoint")
@patch("src.iris_ml_classification.app.get_databricks_token")
@patch("src.iris_ml_classification.app.input_form")
@patch("src.iris_ml_classification.app.inject_css")
@patch("src.iris_ml_classification.app.show_footer")
def test_main_success(mock_footer, mock_css, mock_form, mock_token, mock_call, mock_st, mock_display_result):
    mock_st.button.return_value = True  # simulate button press
    mock_form.return_value = MagicMock()
    mock_token.return_value = "mocked_token"
    mock_call.return_value = {"predictions": ["setosa"]}

    main()

    mock_css.assert_called_once()
    mock_form.assert_called_once()
    mock_token.assert_called_once()
    mock_call.assert_called_once()
    mock_display_result.assert_called_once_with("setosa")
    mock_footer.assert_called_once()




@patch("src.iris_ml_classification.app.st")
@patch("src.iris_ml_classification.app.call_serving_endpoint", side_effect=Exception("Something failed"))
@patch("src.iris_ml_classification.app.get_databricks_token", return_value="token")
@patch("src.iris_ml_classification.app.input_form")
@patch("src.iris_ml_classification.app.inject_css")
@patch("src.iris_ml_classification.app.show_footer")
def test_main_unexpected_exception(mock_footer, mock_css, mock_form, mock_token, mock_call, mock_st):
    mock_st.button.return_value = True
    mock_form.return_value = MagicMock()

    main()

    mock_st.error.assert_called_with("Unexpected error: Something failed")
