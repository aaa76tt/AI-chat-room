import requests
import os

def call_deepseek(user_message, conversation_history=None, api_key="", model="", platform="", url=""):
    """
    Call DeepSeek API for conversation
    
    Parameters:
        user_message: User input message
        conversation_history: Conversation history (optional)
    
    Returns:
        (ai_response, updated_history): AI response and updated conversation history
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add user message
    conversation_history.append({"role": "user", "content": user_message})
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": conversation_history,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Get AI response
        ai_message = result["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": ai_message})
        
        return ai_message, conversation_history
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "Error: API key is invalid or expired, please check your API key", conversation_history
        else:
            return f"HTTP Error: {e}", conversation_history
    except Exception as e:
        return f"Error: {str(e)}", conversation_history


def set_api_key(new_key):
    """Set API key"""
    global api_key
    api_key = new_key


def get_api_key():
    """Get current API key"""
    return api_key
