import re

def extract_sql(query_text: str) -> str:
    """Extract SQL from LLM output, handling 'SQLQuery:' or code blocks"""
    query_text = query_text.strip("```sql").strip("```").strip()
    match = re.search(r"SQLQuery:\s*(.*)", query_text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return query_text

def clean_sql(sql_query: str) -> str:
    """Standardize quotes and remove extra characters"""
    sql_query_clean = sql_query.split(";")[0]  # Keep only first statement
    sql_query_clean = (
        sql_query_clean.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("`", '"')
    )
    return sql_query_clean
