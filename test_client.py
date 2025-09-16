#!/usr/bin/env python3
"""
Test client for the Football Chat API
"""

import requests
import json
import uuid

API_BASE_URL = "http://localhost:8000"

def test_chat_with_session():
    """Test chat with browser signature (session tracking)"""
    browser_id = f"browser-{uuid.uuid4().hex[:8]}"
    
    print(f"🔄 Testing with browser signature: {browser_id}")
    
    # First message
    response1 = requests.post(
        f"{API_BASE_URL}/chat",
        json={"message": "Premier League standings"},
        headers={"BROWSER_SIGNATURE": browser_id}
    )
    
    print("📤 First message: 'Premier League standings'")
    print("📥 Response:", response1.json()["response"][:200] + "..." if len(response1.json()["response"]) > 200 else response1.json()["response"])
    
    # Follow-up message (should maintain context)
    response2 = requests.post(
        f"{API_BASE_URL}/chat",
        json={"message": "What about La Liga?"},
        headers={"BROWSER_SIGNATURE": browser_id}
    )
    
    print("\n📤 Follow-up message: 'What about La Liga?'")
    print("📥 Response:", response2.json()["response"][:200] + "..." if len(response2.json()["response"]) > 200 else response2.json()["response"])

def test_chat_without_session():
    """Test chat without browser signature (no session tracking)"""
    print("\n🔄 Testing without browser signature (no session tracking)")
    
    # First message
    response1 = requests.post(
        f"{API_BASE_URL}/chat",
        json={"message": "Champions League results"}
    )
    
    print("📤 First message: 'Champions League results'")
    print("📥 Response:", response1.json()["response"][:200] + "..." if len(response1.json()["response"]) > 200 else response1.json()["response"])
    
    # Second message (should be treated as new conversation)
    response2 = requests.post(
        f"{API_BASE_URL}/chat",
        json={"message": "What about the previous results I asked about?"}
    )
    
    print("\n📤 Second message: 'What about the previous results I asked about?'")
    print("📥 Response:", response2.json()["response"][:200] + "..." if len(response2.json()["response"]) > 200 else response2.json()["response"])

def test_health_check():
    """Test health endpoint"""
    print("\n🔄 Testing health endpoint")
    response = requests.get(f"{API_BASE_URL}/health")
    print("📥 Health check:", response.json())

def test_sessions_endpoint():
    """Test sessions management endpoints"""
    print("\n🔄 Testing sessions endpoint")
    
    # Get active sessions
    response = requests.get(f"{API_BASE_URL}/sessions")
    print("📥 Active sessions:", response.json())

if __name__ == "__main__":
    try:
        print("🚀 Football Chat API Test Client")
        print("=" * 50)
        
        # Test health check first
        test_health_check()
        
        # Test chat with session tracking
        test_chat_with_session()
        
        # Test chat without session tracking
        test_chat_without_session()
        
        # Check sessions
        test_sessions_endpoint()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
