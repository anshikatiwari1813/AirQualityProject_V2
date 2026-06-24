import streamlit as st
import pandas as pd

def show_upload():

    st.title("Dataset Upload")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.success("Dataset Uploaded Successfully")

        st.write("Shape:", df.shape)

        st.dataframe(df.head())