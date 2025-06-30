"""ui module."""

import pandas as pd
import streamlit as st


# --- PAGE CONFIGURATION ---
def set_page() -> None:
    """Set the Streamlit page configuration for the Iris Flower Species Inference app.

    This function configures the page title, icon, layout, sidebar state, and menu items.
    """
    st.set_page_config(
        page_title="Iris Flower Species Inference",
        page_icon="🌸",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html",
            "About": "#### Iris Species Prediction App\nThis app predicts iris species from flower measurements.\n\nCreated by: Mehmet Acikgoz",
        },
    )


# --- CUSTOM CSS FOR STYLE ---
def inject_css() -> None:
    """Inject custom CSS styles into the Streamlit app.

    This function reads the 'styles.css' file and applies its styles to the app using markdown.
    """
    with open("styles.css") as f:
        # css_path = os.path.join(os.path.dirname(__file__), 'styles.css')
        # with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- MAIN CONTENT ---
def input_form() -> pd.DataFrame:
    """Render an input form for iris flower measurements and return the input as a DataFrame.

    This function displays sliders for sepal and petal dimensions and compiles the results into a pandas DataFrame.

    :return: DataFrame containing the user's input measurements for the iris flower.
    """
    with st.container():
        st.markdown("<h1 class='iris-header'>🌸 Iris Species Predictor 🌸</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: #555; font-size: 1.3em; margin-top:0.6em;'>Enter the flower's measurements below and get its species!</p>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            sepal_length = st.slider("🌱 Sepal length (cm)", 4.30, 7.90)
            petal_length = st.slider("🌸 Petal length (cm)", 1.00, 6.90)
        with col2:
            sepal_width = st.slider("🌿 Sepal width (cm)", 2.0, 4.40)
            petal_width = st.slider("💮 Petal width (cm)", 0.10, 2.50)

        input_df = pd.DataFrame(
            [[sepal_length, sepal_width, petal_length, petal_width]],
            columns=["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"],
        )

        return input_df


# --- PREDICTION BUTTON ---
def display_result(predicted_species: str) -> None:
    """Display the predicted iris species with a corresponding emoji and style.

    This function shows the prediction result in a styled card using markdown and HTML.

    :param predicted_species: The predicted iris species as a string.
    """
    species_emoji = {"setosa": "🌱", "versicolor": "🌿", "virginica": "💐"}
    species_class = {"setosa": "species-setosa", "versicolor": "species-versicolor", "virginica": "species-virginica"}
    st.markdown(
        f"<div class='result-card'>"
        f"<span class='{species_class[predicted_species]}' style='font-size: 1.5em;'>"
        f"{species_emoji[predicted_species]} Predicted species: <b>{predicted_species.capitalize()}</b>"
        f"</span></div>",
        unsafe_allow_html=True,
    )


# --- FOOTER ---
def show_footer() -> None:
    """Display a footer message crediting the app creator and technologies used.

    This function renders a styled footer using markdown and HTML.
    """
    st.markdown(
        "<div class='footer'>Made with ❤️ using Streamlit & Databricks Free Edition by Mehmet Acikgoz</div>",
        unsafe_allow_html=True,
    )
