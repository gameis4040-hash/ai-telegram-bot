from google import genai
from ddgs import DDGS

gemini_client = genai.Client(api_key="GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """You are a helpful assistant.
If the question needs current/recent info, use the provided web search results.
Keep answers concise and friendly."""


def search_web(query):
    try:
        results = DDGS().text(query, max_results=4)
        if not results:
            return "No results found."
        return "\n\n".join(
            f"{r['title']}: {r['body']} ({r['href']})" for r in results
        )
    except Exception:
        return "Search unavailable."


def should_search(text):
    keywords = ["latest", "news", "today", "current", "price", "weather",
                "who is", "what is", "when", "where", "recent"]
    return any(k in text.lower() for k in keywords)


def get_answer(user_message):
    context = ""
    if should_search(user_message):
        context = f"\n\nWeb search results:\n{search_web(user_message)}\n"

    response = client.models.generate_content(
        model=MODEL,
        contents=SYSTEM_PROMPT + context + "\n\nUser: " + user_message,
    )
    return response.text
