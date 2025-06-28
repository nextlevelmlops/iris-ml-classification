import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
def set_page():
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
def inject_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- MAIN CONTENT ---
def input_form() -> pd.DataFrame:
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
                             
        return input_df

# --- PREDICTION BUTTON ---
def display_result(predicted_species:str):
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
def show_footer():
    st.markdown(
        "<div class='footer'>Made with ❤️ using Streamlit & Databricks Free Edition by Mehmet Acikgoz</div>",
        unsafe_allow_html=True
    )
