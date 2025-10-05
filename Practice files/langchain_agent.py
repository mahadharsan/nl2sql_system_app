import pandas as pd
from langchain_experimental.agents import create_csv_agent
from langchain_community.llms import Ollama

def preprocess_csv(file_path: str):
    df = pd.read_csv(file_path)

    for col in df.columns:
        if df[col].dropna().astype(str).str.replace('.', '', 1).str.isdigit().all():
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif set(df[col].dropna().astype(str).str.upper().unique()) <= {"TRUE", "FALSE"}:
            df[col] = df[col].astype(str).str.upper().map({"TRUE": True, "FALSE": False})
        elif "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
        else:
            df[col] = df[col].astype(str)

    print("\n✅ Updated column datatypes:")
    print(df.dtypes)

    cleaned_file = "cleaned.csv"
    df.to_csv(cleaned_file, index=False)
    return cleaned_file

# --- Run agent ---
csv_file = preprocess_csv("sample_users.csv")
llm = Ollama(model="llama3.2:3b")
agent = create_csv_agent(llm, csv_file, verbose=True, handle_parsing_errors=True)

response = agent.invoke({"input": "How many premium users are there per country?"})
print("Answer:", response["output"])
