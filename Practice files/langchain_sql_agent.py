from click import prompt
from sqlalchemy import create_engine
import pandas as pd
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.llms import Ollama

def load_csv_into_sqlite(file_path: str):
    engine = create_engine("sqlite:///:memory:")
    df = pd.read_csv(file_path)
    df.to_sql("data", engine, index=False, if_exists="replace")
    return engine

file_path = "sample_users.csv"
engine = load_csv_into_sqlite(file_path)
db = SQLDatabase(engine)

llm = Ollama(model="llama3.2:3b")
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

while True:
    question = input("Enter your SQL question (Enter 'exit' to quit): ")
    if question.lower() == "exit":
        break
    response = sql_chain.invoke({"query": question})
    print("Answer:", response)
    print('Only the result of the response:', response['result'])
    # response = sql_chain.run(question)
    # print("Answer:", response)