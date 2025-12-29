import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Data Explorer", layout="wide")

st.title("📊 CSV Data Explorer")

st.write(
    "Upload a CSV file to explore, visualize, "
    "filter, and download your data."
)

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Info")
    st.write(
        f"Rows: {df.shape[0]} | Columns: {df.shape[1]}"
    )
    st.write("Column types:")
    st.write(df.dtypes)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("Summary Statistics")
    st.write(df.describe())

    st.subheader("Filter Data")
    column = st.selectbox("Select column to filter", df.columns)
    unique_vals = df[column].unique()
    value = st.selectbox("Select value", unique_vals)
    filtered_df = df[df[column] == value]
    st.write(filtered_df)

    st.subheader("Visualization")
    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    if len(numeric_cols) > 0:
        chart_type = st.selectbox(
            "Chart type",
            ["Histogram", "Line Chart", "Bar Chart"],
        )

        selected_col = st.selectbox(
            "Select numeric column",
            numeric_cols,
        )

        if chart_type == "Histogram":
            fig, ax = plt.subplots()
            ax.hist(df[selected_col].dropna())
            st.pyplot(fig)

        elif chart_type == "Line Chart":
            st.line_chart(df[selected_col])

        elif chart_type == "Bar Chart":
            st.bar_chart(df[selected_col])

    else:
        st.write("No numeric columns available to visualize.")

    st.subheader("Download Cleaned Data")
    cleaned_csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to get started.")
