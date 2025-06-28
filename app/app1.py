import os

import mlflow
import pandas as pd
import requests
import streamlit as st
from mlflow.pyfunc import PyFuncModel
from requests.auth import HTTPBasicAuth

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# --- ENVIRONMENT SETUP ---
# Ensure host (DATABRICKS_HOST) has 'https://' prefix (walrus operator one-liner)
host= host if (host := os.environ.get("DATABRICKS_HOST", "")).startswith("https://") else f"https://{host}"
endpoint_name = "iris-classification-model-serving"
serving_endpoint = f"{host}/serving-endpoints/{endpoint_name}/invocations"

def get_token()-> str:
    """
    Retrieves an OAuth access token from the Databricks workspace.

    :return: The access token string.
    """    
    response = requests.post(
        f"{host}/oidc/v1/token",
        auth=HTTPBasicAuth(
            os.environ["DATABRICKS_CLIENT_ID"], 
            os.environ["DATABRICKS_CLIENT_SECRET"]
            ),
        data={
            'grant_type': 'client_credentials',
             'scope': 'all-apis'
             }
    )

    return response.json()["access_token"]

token = get_token()


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Iris Flower Species Inference",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html',
        'About': "# Iris Flower Classification App\nThis app predicts iris species from flower measurements.\nCreated by: Mehmet Acikgoz"
    }
)

# --- CUSTOM CSS FOR STYLE ---
st.markdown("""
    <style>
        body {background-color: #f6f6ff;}
        .main {background-color: #f6f6ff;}
        .stButton>button {
            background-color: #8e44ad;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 2em;
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
        }
        .species-setosa {color: #27ae60;}
        .species-versicolor {color: #2980b9;}
        .species-virginica {color: #e67e22;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER WITH EMOJI ---
st.markdown("<h1 style='text-align: center; color: #8e44ad;'>🌸 Iris Flower Species Predictor 🌸</h1>", unsafe_allow_html=True)
st.image("./iris_species.png", width=600)
st.markdown("<p style='text-align: center; color: #555; font-size: 2.1em;'>Enter the flower's measurements below and get its species!</p>", unsafe_allow_html=True)

# --- INPUT WIDGETS IN COLUMNS ---
col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider('🌱 Sepal length (cm)', 4.30, 7.90)
    petal_length = st.slider('🌸 Petal length (cm)', 1.00, 6.90)
with col2:
    sepal_width = st.slider('🌿 Sepal width (cm)', 2.0, 4.40)
    petal_width = st.slider('💮 Petal width (cm)', 0.10, 2.50)

input_features = [[sepal_length, sepal_width, petal_length, petal_width]]

input_df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                         columns=["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)"])

# --- PREDICTION BUTTON ---
if st.button("🔮 Predict Species"):

    response = requests.post(
    serving_endpoint,
    headers={"Authorization": f"Bearer {token}"},
    json={"dataframe_split": input_df.to_dict(orient="split")})
    response.raise_for_status()
    predicted_species = response.json()['predictions'][0]


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
    st.balloons()

# --- FOOTER ---
st.markdown(
    "<hr><p style='text-align: center; color: #8e44ad; font-size: 1.9em;'>"
    "Made with ❤️ using Streamlit & Databricks Free Edition"
    "</p>", unsafe_allow_html=True
)