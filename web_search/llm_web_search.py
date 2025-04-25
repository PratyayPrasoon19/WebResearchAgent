import google.generativeai as genai

from config import config

# Initialize Gemini model
genai.configure(api_key=config.gemini_api)
llm_web_search = genai.GenerativeModel(model_name="gemini-1.5-flash")
system_prompt = '''for the user_query, do a mock web search and returns the detailed report related to that query
'''
chat = llm_web_search.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

def search_web_response(questions: list[str]) -> str:
    url_list = ''

    for ques in questions:
        response = chat.send_message([system_prompt,ques])
        url_list = url_list + response.text
    return url_list