import os
import pandas as pd
import requests
import streamlit as st
from requests.auth import HTTPBasicAuth
from typing import Any

from config import config
from api import get_databricks_token, call_serving_endpoint
from ui import set_page, inject_css, input_form, display_result, show_footer

      
def main() -> None:
    inject_css()
    input_df = input_form()
    if st.button("🔮 Predict Species"):
        try:
            token = get_databricks_token(host=config.HOST)
            response = call_serving_endpoint(serving_endpoint=config.SERVING_ENDPOINT, token=token, input_df=input_df)
            predicted_species = response['predictions'][0]
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