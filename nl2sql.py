from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.llms import Ollama
from utils import extract_sql, clean_sql
from loader import df_to_sqlite
import pandas as pd

def get_answer_from_file_or_db(file_or_engine, question: str):
    """
    Main NL2SQL function
    Accepts:
        - pandas DataFrame or file-like object
        - SQLAlchemy engine for database
    """
    if isinstance(file_or_engine, pd.DataFrame):
        engine = df_to_sqlite(file_or_engine)
    elif hasattr(file_or_engine, "execute"):
        # Already a SQLAlchemy engine
        engine = file_or_engine
    else:
        # Load file into DataFrame then SQLite
        from loader import load_file
        df = load_file(file_or_engine)
        engine = df_to_sqlite(df)

    db = SQLDatabase(engine)
    llm = Ollama(model="llama3.2:3b")
    sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

    sql_query = sql_chain.run(question)
    sql_query = extract_sql(sql_query)
    sql_query_clean = clean_sql(sql_query)

    try:
        result = db.run(sql_query_clean)
    except Exception as e:
        return f"Error executing SQL: {e}\nSQL Tried: {sql_query_clean}"

    if not result:
        return "✅ Query executed successfully, but no rows matched."
    if len(result) == 1 and len(result[0]) == 1:
        return result[0][0]

    try:
        with engine.connect() as conn:
            df_result = pd.read_sql_query(sql_query_clean, conn)
        return df_result
    except Exception:
        return result
