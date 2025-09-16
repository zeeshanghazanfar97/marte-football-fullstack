import os
from openai import OpenAI
from rich.markdown import Markdown
from rich.console import Console

console = Console()

prompt = """
You are an AI assistant specialized in football (soccer). When answering a user’s query:

1. **Always use the web search tool** to fetch the most recent football data (fixtures, results, standings, stats, transfers, etc.).
2. **Do not include disclaimers, reference links, or source mentions** in your response.
3. **Return only the factual, up-to-date results** in a clean, structured, and concise format (tables for standings, bullet points for matches, short lists for stats).
4. If multiple possible answers exist (e.g., multiple leagues or teams), ask the user for clarification before responding.
5. If no current data is found, simply reply: **“No current data available.”**

**User Example Queries:**

* “Upcoming La Liga matches this weekend”
* “Champions League results today”
* “Serie A top scorers right now”
* “Premier League standings”

**Expected Output Style (example):**
Upcoming La Liga Matches:

* Real Madrid vs. Valencia — Sept 21, 20:00 CET
* Barcelona vs. Sevilla — Sept 22, 18:30 CET
* Atlético Madrid vs. Villarreal — Sept 23, 21:00 CET
"""

def chat_loop():
    # Load API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set the OPENAI_API_KEY environment variable")

    client = OpenAI(api_key=api_key)

    print("Chat with assistant (type 'exit' to quit)")

    previous_response_id = None

    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Call the Responses API, with web search tool enabled
        resp = client.responses.create(
            model="gpt-4o",
            instructions=prompt,
            previous_response_id=previous_response_id,
            input=user_input,
            tools=[
                {
                    "type": "web_search_preview",
                    "user_location": {
                        "type": "approximate",
                        "country": "MX"
                    },
                    "search_context_size": "medium"
                }
            ]
        )
        previous_response_id = resp.id

        assistant_message = resp.output_text.strip()
        
        console.print(Markdown(f"**Assistant:** {assistant_message}"))
        

chat_loop()