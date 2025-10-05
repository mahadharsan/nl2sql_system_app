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
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

while True:
    question = input("Enter your SQL question (Enter 'exit' to quit): ")
    if question.lower() == "exit":
        break
    
    # Let the chain generate the SQL
    sql_query = sql_chain.run(question)  # returns LLM output with the SQL command
    # Extract only the SQL query using a simple heuristic
    if "SQLQuery:" in sql_query:
        sql_query_clean = sql_query.split("SQLQuery:")[-1].strip()
    else:
        sql_query_clean = sql_query.strip()
    
    # Execute SQL directly on the database
    result = db.run(sql_query_clean)
    print("Only SQLResult:", result)
