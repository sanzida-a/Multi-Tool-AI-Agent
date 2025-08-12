import os
from typing import Optional
from .db_tools import HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
from .web_tool import MedicalWebSearchTool

class MultiToolAgent:
    def __init__(self, heart_db_path, cancer_db_path, diabetes_db_path, serpapi_key=None):
        self.heart_tool = HeartDiseaseDBTool(heart_db_path)
        self.cancer_tool = CancerDBTool(cancer_db_path)
        self.diabetes_tool = DiabetesDBTool(diabetes_db_path)
        self.web_tool = MedicalWebSearchTool(serpapi_key)

        self.db_keywords = [
            "average", "mean", "median", "count", "how many", "percentage", "percent",
            "correlation", "correlate", "trend", "incidence", "prevalence", "rate",
            "age", "sex", "gender", "bmi", "cholesterol", "glucose", "blood", "bp", "pressure"
        ]
        self.web_keywords = [
            "what is", "definition", "symptom", "treatment", "cure",
            "causes", "side effect", "diagnosis"
        ]

    def _likely_db_question(self, q: str) -> Optional[str]:
        ql = q.lower()
        if "heart" in ql or "cardio" in ql:
            return "heart"
        if "cancer" in ql or "tumor" in ql or "tumour" in ql:
            return "cancer"
        if "diabetes" in ql or "glucose" in ql or "insulin" in ql:
            return "diabetes"
        if any(k in ql for k in self.db_keywords):
            if any(t in ql for t in ["cholesterol", "heart", "bp"]):
                return "heart"
            if any(t in ql for t in ["tumor", "malignant"]):
                return "cancer"
            if any(t in ql for t in ["glucose", "insulin"]):
                return "diabetes"
            return "heart"
        if any(k in ql for k in self.web_keywords):
            return None
        return "heart"

    def answer(self, question: str) -> str:
        route = self._likely_db_question(question)
        if route == "heart":
            return self.heart_tool.answer_question(question)
        if route == "cancer":
            return self.cancer_tool.answer_question(question)
        if route == "diabetes":
            return self.diabetes_tool.answer_question(question)
        return self.web_tool.search(question)
