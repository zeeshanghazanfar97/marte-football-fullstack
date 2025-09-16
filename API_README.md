# Football Chat API

A FastAPI-based chatbot specialized in football (soccer) that uses OpenAI's GPT-4o with web search capabilities.

## Features

- Real-time football data fetching via web search
- Conversation tracking using browser signatures
- Clean, structured responses without disclaimers or source links
- Session management for multiple clients

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

## Running the API

### Option 1: Using the app.py file directly
```bash
python app.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Endpoints

### `POST /chat`
Main chat endpoint.

**Request:**
```json
{
  "message": "Premier League standings"
}
```

**Headers:**
- `BROWSER_SIGNATURE` (optional): Unique identifier to track conversation sessions

**Response:**
```json
{
  "response": "Premier League Standings:\n\n1. Manchester City - 28 pts\n2. Arsenal - 27 pts\n...",
  "session_id": "browser-123"
}
```

### `GET /health`
Health check endpoint.

### `GET /sessions`
View active conversation sessions (for debugging).

### `DELETE /sessions/{browser_signature}`
Clear a specific conversation session.

## Usage Examples

### With conversation tracking (browser signature):
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -H "BROWSER_SIGNATURE: browser-123" \
  -d '{"message": "Premier League standings"}'
```

### Without conversation tracking:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Champions League results today"}'
```

## Session Management

- **With BROWSER_SIGNATURE header**: Conversations are tracked per browser. Each subsequent request with the same signature continues the conversation.
- **Without BROWSER_SIGNATURE header**: Each request is treated as a new conversation (`previous_response_id` is always `None`).
