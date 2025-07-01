"""main app module."""

import os

import requests
import streamlit as st

if os.getenv("DATABRICKS_WORKSPACE_ID", None):
    from api import call_serving_endpoint, get_databricks_token
    from config import config
    from ui import display_result, inject_css, input_form, set_page, show_footer
else:
    from iris_ml_classification.api import call_serving_endpoint, get_databricks_token
    from iris_ml_classification.config import config
    from iris_ml_classification.ui import display_result, inject_css, input_form, set_page, show_footer


def main() -> None:
    """Run the Iris Species Predictor Streamlit app.

    This function handles CSS injection, user input, prediction requests, and result display.
    """
    inject_css()
    input_df = input_form()
    if st.button("🔮 Predict Species"):
        try:
            token = get_databricks_token(host=config.HOST)
            response = call_serving_endpoint(serving_endpoint=config.SERVING_ENDPOINT, token=token, input_df=input_df)
            predicted_species = response["predictions"][0]
            display_result(predicted_species)
        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
    show_footer()


if __name__ == "__main__":
    # This must be the first Streamlit command  whenever the app runs
    set_page()
    main()
