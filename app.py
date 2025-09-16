import os
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

app = FastAPI(title="Football Chat API", version="1.0.0")

# Mount static files for assets
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for conversation tracking
# In production, you might want to use Redis or a database
conversation_store: Dict[str, Optional[str]] = {}

prompt = """
You are an AI assistant specialized in football (soccer). When answering a user's query:

1. **Always use the web search tool** to fetch the most recent football data (fixtures, results, standings, stats, transfers, etc.).
2. **Do not include disclaimers, reference links, or source mentions** in your response.
3. **Return only the factual, up-to-date results** in a clean, structured, and concise format (tables for standings, bullet points for matches, short lists for stats).
4. If multiple possible answers exist (e.g., multiple leagues or teams), ask the user for clarification before responding.
5. If no current data is found, simply reply: **"No current data available."**

**User Example Queries:**

* "Upcoming La Liga matches this weekend"
* "Champions League results today"
* "Serie A top scorers right now"
* "Premier League standings"

**Expected Output Style (example):**
Upcoming La Liga Matches:

* Real Madrid vs. Valencia — Sept 21, 20:00 CET
* Barcelona vs. Sevilla — Sept 22, 18:30 CET
* Atlético Madrid vs. Villarreal — Sept 23, 21:00 CET
"""

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

def get_openai_client():
    """Get OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    browser_signature: Optional[str] = Header(None, alias="BROWSER_SIGNATURE")
):
    """
    Chat endpoint that maintains conversation context using browser signatures.
    
    - **message**: The user's message
    - **BROWSER_SIGNATURE**: Header to track conversation sessions (optional)
    
    If BROWSER_SIGNATURE header is missing, previous_response_id stays None (new conversation each time).
    If BROWSER_SIGNATURE header is present, conversation context is maintained for that browser.
    """
    try:
        client = get_openai_client()
        
        # Determine previous_response_id based on browser signature
        previous_response_id = None
        if browser_signature:
            # If BROWSER_SIGNATURE exists, get the stored response_id for this browser
            previous_response_id = conversation_store.get(browser_signature)
        
        # Call the OpenAI Responses API
        resp = client.responses.create(
            model="gpt-4o",
            instructions=prompt,
            previous_response_id=previous_response_id,
            input=request.message,
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
        
        # Update conversation store if browser signature exists
        if browser_signature:
            conversation_store[browser_signature] = resp.id
        
        return ChatResponse(
            response=resp.output_text.strip(),
            session_id=browser_signature
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/sessions")
async def get_active_sessions():
    """Get all active conversation sessions (for debugging)"""
    return {
        "active_sessions": len(conversation_store),
        "sessions": list(conversation_store.keys())
    }

@app.delete("/sessions/{browser_signature}")
async def clear_session(browser_signature: str):
    """Clear a specific conversation session"""
    if browser_signature in conversation_store:
        del conversation_store[browser_signature]
        return {"message": f"Session {browser_signature} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML file"""
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8145)
