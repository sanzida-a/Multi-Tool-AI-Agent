import os
from typing import Tuple, List
from utils.sql_utils import SQLiteDB
from utils.text_utils import summarize_rows_to_text
from openai import OpenAI

client = OpenAI(
    
    base_url="https://models.github.ai/inference/v1",
    api_key=os.getenv["GITHUB_TOKEN"]
)

class BaseDBTool:
    def __init__(self, db_path: str, table_hint: str):
        self.db = SQLiteDB(db_path)
        self.table_hint = table_hint

    def nl_to_sql(self, question: str, schema_hint: str = "") -> str:
        prompt = f"""
You are a helpful assistant that converts a user question about a medical dataset to a valid SQLite SELECT query.
Only produce the SQL statement and nothing else. Use the table name hint: {self.table_hint}.
If the question cannot be answered with a SQL SELECT, output: --NO_SQL--
User question: {question}
Schema hint: {schema_hint}
"""
        resp = client.chat.completions.create(
            model="openai/gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You convert NL to SQL for SQLite. Output only SQL."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return resp.choices[0].message.content.strip()

    def answer_question(self, question: str) -> str:
        try:
            schema = self.db.get_table_schema(self.table_hint)
            schema_text = ", ".join([f"{c}:{t}" for c, t in schema])
        except Exception:
            schema_text = ""

        sql = self.nl_to_sql(question, schema_text)
        if sql.strip().startswith("--NO_SQL--"):
            return "I could not generate a SQL query for that question."
        if not sql.strip().lower().startswith("select"):
            return "For safety, I will only run SELECT queries."

        try:
            rows = self.db.execute_query(sql)
        except Exception as e:
            return f"Error running SQL: {e}\nSQL: {sql}"

        col_names = [c for c, _ in schema] if schema else []
        return f"SQL used:\n{sql}\n\nResults:\n{summarize_rows_to_text(col_names, rows, max_rows=20)}"

class HeartDiseaseDBTool(BaseDBTool):
    def __init__(self, db_path: str):
        super().__init__(db_path, table_hint="heart_data")

class CancerDBTool(BaseDBTool):
    def __init__(self, db_path: str):
        super().__init__(db_path, table_hint="cancer_data")

class DiabetesDBTool(BaseDBTool):
    def __init__(self, db_path: str):
        super().__init__(db_path, table_hint="diabetes_data")
