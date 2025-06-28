import os
import pandas as pd
import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

# --- ENVIRONMENT SETUP ---
host = host if (host := os.environ.get("DATABRICKS_HOST", "")).startswith("https://") else f"https://{host}"
endpoint_name = "iris-classification-model-serving"
serving_endpoint = f"{host}/serving-endpoints/{endpoint_name}/invocations"

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
) -> dict:
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


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Iris Flower Species Inference",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html',
        'About': "#### Iris Species Prediction App\nThis app predicts iris species from flower measurements.\n\nCreated by: Mehmet Acikgoz"
    }
)

# --- CUSTOM CSS FOR STYLE ---
st.markdown("""
    <style>
        body, .main {
            background-color: #f6f6ff;
        }
        .iris-header {
            text-align: center;
            color: #8e44ad;
            margin-bottom: 0.4em;
            font-size: 1.5em;
            line-height: 1.1;
            word-break: break-word;
            font-weight: 700;
            letter-spacing: 0.02em;
        }
        @media (max-width: 600px) {
            .iris-header {
                font-size: 1.3em;
            }
        }
        .stButton>button {
            background-color: #8e44ad;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 2em;
            font-size: 1.1em;
        }
        .stButton>button:hover {
            background-color: #6c3483;
            color: #ffeb3b;
        }
        .result-card {
            background: linear-gradient(90deg, #f8ffae 0%, #43c6ac 100%);
            border-radius: 15px;
            padding: 1.5em;
            margin-top: 1em;
            box-shadow: 2px 2px 10px #b4b4b4;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
        }
        .species-setosa {color: #27ae60;}
        .species-versicolor {color: #2980b9;}
        .species-virginica {color: #e67e22;}
        .footer {
            position: fixed;
            left: 0; right: 0; bottom: 0;
            width: 100%;
            background: transparent;
            padding: 0.6em 0 0.8em 0;
            text-align: center;
            font-size: 1.15em;
            color: #8e44ad;
            z-index: 100;
            letter-spacing: 0.5px;
        }
        /* Hide Streamlit branding footer */
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
with st.container():
    st.markdown("<h1 class='iris-header'>🌸 Iris Species Predictor 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; font-size: 1.3em; margin-top:0.6em;'>Enter the flower's measurements below and get its species!</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        sepal_length = st.slider('🌱 Sepal length (cm)', 4.30, 7.90)
        petal_length = st.slider('🌸 Petal length (cm)', 1.00, 6.90)
    with col2:
        sepal_width = st.slider('🌿 Sepal width (cm)', 2.0, 4.40)
        petal_width = st.slider('💮 Petal width (cm)', 0.10, 2.50)

input_df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                         columns=["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)"])

# --- PREDICTION BUTTON ---
if st.button("🔮 Predict Species"):
    token = get_databricks_token(host=host)
    response = call_serving_endpoint(serving_endpoint=serving_endpoint, token=token, input_df=input_df)
    predicted_species = response['predictions'][0]
    species_emoji = {
        "setosa": "🌱",
        "versicolor": "🌿",
        "virginica": "💐"
    }
    species_class = {
        "setosa": "species-setosa",
        "versicolor": "species-versicolor",
        "virginica": "species-virginica"
    }
    st.markdown(
        f"<div class='result-card'>"
        f"<span class='{species_class[predicted_species]}' style='font-size: 1.5em;'>"
        f"{species_emoji[predicted_species]} Predicted species: <b>{predicted_species.capitalize()}</b>"
        f"</span></div>",
        unsafe_allow_html=True
    )

# --- FOOTER ---
st.markdown(
    "<div class='footer'>Made with ❤️ using Streamlit & Databricks Free Edition by Mehmet Acikgoz</div>",
    unsafe_allow_html=True
)
