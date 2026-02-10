import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title(" Ohh shit ninja.")

upload_file = st.file_uploader("Choose a File", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.subheader("Data Preview")
    st.write(df.head())

    #st.subheader("summery")
   # st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_columns = st.selectbox("Select Columns", columns)
    unique_values = df[selected_columns].unique()
    selected_value = st.selectbox("Select Value", unique_values)

    filtered_df = df[df[selected_columns] == selected_value]
    st.write(filtered_df)


    st.subheader("Plot Data")
    x_column = st.selectbox("Select X Column", columns)
    y_column = st.selectbox("Select Y Column", columns)

    if st.button("display chart"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("waiting for file upload . . .")
