import streamlit as st
import pandas as pd
from loader import load_file
from nl2sql import get_answer_from_file_or_db
from db_connector import connect_database

st.title("AI Powered NL2SQL System")
st.write("Welcome to the Data Query Assistant!")

# Toggle: File upload vs Database
mode = st.radio("Choose input mode:", ["Upload File", "Database"])

if mode == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=[
            "csv", "tsv", "xls", "xlsx", "ods",
            "json", "parquet", "feather", "h5",
            "dta", "sas7bdat", "xml", "yaml", "yml",
            "zip", "gz", "bz2", "xz"
        ]
    )
    if uploaded_file:
        if uploaded_file.name.lower().endswith((".xls", ".xlsx", ".ods")):
            xls = pd.ExcelFile(uploaded_file)
            sheet = st.selectbox("Select a sheet:", xls.sheet_names)
        else:
            sheet = None

        df = load_file(uploaded_file, sheet_name=sheet)

        question = st.text_area("Enter your question:", height=150)
        if st.button("Get Answer"):
            with st.spinner("Processing..."):
                answer = get_answer_from_file_or_db(df, question)
                st.write("Answer:")
                st.write(answer)

elif mode == "Database":
    db_type = st.selectbox("Select Database", ["sqlite", "postgresql", "mysql", "mssql"])
    host = st.text_input("Host (for SQLite leave empty)")
    port = st.text_input("Port (leave empty for SQLite)")
    user = st.text_input("User (leave empty for SQLite)")
    password = st.text_input("Password", type="password")
    dbname = st.text_input("Database Name / Path")

    if st.button("Connect"):
        try:
            engine = connect_database(db_type, user, password, host, port, dbname)
            st.success("Connected successfully!")

            question = st.text_area("Enter your question:", height=150)
            if st.button("Get Answer from DB"):
                with st.spinner("Processing..."):
                    answer = get_answer_from_file_or_db(engine, question)
                    st.write("Answer:")
                    st.write(answer)

        except Exception as e:
            st.error(f"Connection failed: {e}")
