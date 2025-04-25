from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from web_search.llm_web_search import search_web_response
from config import config

# Initialize Gemini model
llm1 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=config.gemini_api)
llm2 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=config.gemini_api)

# Memory to store user_query and processed response
memory = ConversationBufferMemory(return_messages=True)

def search_query_list(response: str) -> list[str]:
    list = response.split(',')
    return [i for i in list]

system_prompt = '''analyze the user query, and provide a list of questions which should be searched on web related to that query
Provide only list of questions in following format: ques 1, ques 2
Provide at most 5 questions related to query, which covers all portions.
'''

# Core logic function
def handle_user_query(user_query: str) -> str:
    # Save user query in memory
    memory.chat_memory.add_user_message(user_query)

    # Get conversation history
    history_messages = [SystemMessage(content=system_prompt)] + memory.chat_memory.messages

    # LLM1 generates a response
    llm_response = llm1(history_messages).content
    # print('llm: ',llm_response)

    # Preprocess the response
    questions = search_query_list(llm_response)

    web_response = search_web_response(questions)
    # print('url links\n',processed_response)
    
    messages = [
    SystemMessage(content="generate a report from the provided content with proper headings and sub headings"),
    HumanMessage(content=web_response)
]
    # [
    #     {"role": "user", "content": web_response},
    #     {"role": "system", "content": }
    # ]
    processed_web_response = llm2(messages).content
    # print(processed_web_response)

    # Save processed response in memory
    memory.chat_memory.add_ai_message(processed_web_response)

    return processed_web_response

# CLI app
if __name__ == "__main__":
    print("Gemini ChatBot (type 'quit' to exit)")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["quit", "exit"]:
            break
        final_response = handle_user_query(user_query)
        print(f"Bot: {final_response}")

#   write a report on unity in diversity of India