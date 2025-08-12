import os
from serpapi import GoogleSearch

class MedicalWebSearchTool:
    def __init__(self, serpapi_key=None):
        self.api_key = serpapi_key or os.environ.get("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not set")
    def search(self, query, num_results=3):
        params = {"engine": "google", "q": query, "api_key": self.api_key, "num": num_results}
        client = GoogleSearch(params)
        res = client.get_dict()
        # A simple summary: combine top organic results titles/snippets
        items = res.get("organic_results", [])[:num_results]
        out = []
        for it in items:
            title = it.get("title")
            snippet = it.get("snippet") or it.get("snippet_highlighted_words")
            out.append(f"- {title}\n  {snippet}")
        return "Search results:\n" + "\n\n".join(out) if out else "No results found."
