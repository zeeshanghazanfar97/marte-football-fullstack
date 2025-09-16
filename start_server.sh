#!/bin/bash

# Start the Football Chat API server
echo "🚀 Starting Football Chat API..."

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

# Sync dependencies
echo "📦 Syncing dependencies..."
uv sync

# Start the server
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API documentation available at http://localhost:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

python app.py
