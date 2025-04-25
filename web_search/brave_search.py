import requests
from config import config

def search_web_response(questions: list[str]) -> list[list[str]]:
    all_results = []
    base_url = "https://api.search.brave.com/res/v1/web/search"

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": config.BRAVE_API_KEY,
    }

    for query in questions:
        print(f"🔍 Searching: {query}")
        params = {
            "q": query,
            "count": 5
        }

        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        urls = [item["url"] for item in data.get("web", {}).get("results", [])]
        all_results.append(urls)

    return all_results
