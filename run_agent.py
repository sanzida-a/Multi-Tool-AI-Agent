import os
from dotenv import load_dotenv
from src.agents.main_agent import MultiToolAgent

load_dotenv()

heart_db = os.environ.get("HEART_DB_PATH", "data/databases/heart_disease.db")
cancer_db = os.environ.get("CANCER_DB_PATH", "data/databases/cancer.db")
diabetes_db = os.environ.get("DIABETES_DB_PATH", "data/databases/diabetes.db")
serp_key = os.environ.get("SERPAPI_API_KEY")

def interactive_shell():
    print("Multi-Tool Medical Agent (type 'exit' to quit)\n")
    agent = MultiToolAgent(heart_db, cancer_db, diabetes_db, serp_key)
    while True:
        q = input("\nAsk a question: ")
        if q.strip().lower() in ("exit", "quit"):
            break
        resp = agent.answer(q)
        print("\n--- Agent response ---")
        print(resp)

if __name__ == "__main__":
    interactive_shell()
