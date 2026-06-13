import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Data Visualizer", layout="wide")

st.title("📊 AI Data Visualization Dashboard")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📈 Line Chart")
        st.line_chart(df[numeric_cols])

        st.subheader("📊 Bar Chart")
        st.bar_chart(df[numeric_cols])

        st.subheader("📉 Correlation Matrix")
        st.dataframe(df[numeric_cols].corr())

        column = st.selectbox(
            "Choose column for histogram",
            numeric_cols
        )

        st.subheader("Histogram")
        st.histogram = st.bar_chart(
            df[column].value_counts().head(20)
        )

    else:
        st.warning("No numeric columns found.")

else:
    st.info("Upload a CSV file to begin.")