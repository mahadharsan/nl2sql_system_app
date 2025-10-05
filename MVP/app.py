import streamlit as st
from MVP.csv_agent import get_answer_from_csv 

st.title('AI Powered NL2SQL System')

st.write('Welcome to the CSV Data Query Assistant!')

uploaded_file = st.file_uploader('Upload your CSV file:', type=['csv'])

if uploaded_file:
    st.write('File uploaded successfully!')
    question = st.text_area('Enter your question:', height=150, key="query_box")
    if question:
        if st.button('Get Answer'):
            with st.spinner('Processing...'):
                answer = get_answer_from_csv(uploaded_file, question)
                st.write('Answer:')
                st.write(answer)