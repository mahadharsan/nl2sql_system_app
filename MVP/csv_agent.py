import re
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

def extract_sql(query_text: str) -> str:
    # Extracts the part after "SQLQuery:" if present
    match = re.search(r"SQLQuery:\s*(.*)", query_text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return query_text.strip()

def get_answer_from_csv(file_path, question: str) -> str:
    engine = load_csv_into_sqlite(file_path)
    db = SQLDatabase(engine)

    llm = Ollama(model="llama3.2:3b")
    sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

    # Generate SQL using LLM
    sql_query = sql_chain.run(question)
    sql_query = extract_sql(sql_query)
    # Keep only first statement (remove extra queries)
    sql_query_clean = sql_query.split(";")[0]

    sql_query_clean = (
        sql_query_clean.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("`", '"')
    )

    # Execute safely
    try:
        result = db.run(sql_query_clean)
    except Exception as e:
        return f"Error executing SQL: {e}\nSQL Tried: {sql_query_clean}"

    # Auto-format the result
    if not result:  # No rows returned
        return "✅ Query executed successfully, but no rows matched."

    # If result is a single scalar, return it cleanly
    if len(result) == 1 and len(result[0]) == 1:
        return result[0][0]

    # Otherwise, try to get column names and return as a DataFrame
    try:
        # Fetch column names for better readability
        with engine.connect() as conn:
            df = pd.read_sql_query(sql_query_clean, conn)
        return df
    except Exception:
        # Fallback: if can't convert to DataFrame, just show tuples
        return result
