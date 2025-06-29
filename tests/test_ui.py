import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.iris_ml_classification.ui import input_form, display_result, inject_css, set_page, show_footer


@patch("src.iris_ml_classification.ui.st.slider")
@patch("src.iris_ml_classification.ui.st.columns")
@patch("src.iris_ml_classification.ui.st.markdown")
def test_input_form(mock_markdown, mock_columns, mock_slider):
    # Mock Streamlit slider return values
    mock_columns.return_value = (MagicMock(), MagicMock())
    mock_slider.side_effect = [5.1, 1.4, 3.5, 0.2]

    df = input_form()

    expected = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],
                            columns=["sepal length (cm)", "sepal width (cm)",
                                     "petal length (cm)", "petal width (cm)"])
    pd.testing.assert_frame_equal(df, expected)


@patch("src.iris_ml_classification.ui.st.markdown")
def test_display_result(mock_markdown):
    display_result("setosa")
    mock_markdown.assert_called_once()
    assert "setosa" in mock_markdown.call_args[0][0]


@patch("src.iris_ml_classification.ui.st.markdown")
def test_show_footer(mock_markdown):
    show_footer()
    mock_markdown.assert_called_once()
    assert "Mehmet Acikgoz" in mock_markdown.call_args[0][0]


@patch("src.iris_ml_classification.ui.st.set_page_config")
def test_set_page(mock_set_config):
    set_page()
    mock_set_config.assert_called_once()
