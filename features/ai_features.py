# features/ai_features.py

def ai_assistant_query(query):
    """
    Simulate an AI assistant responding to a user's query.

    Parameters:
        query (str): The user's query.

    Returns:
        str: AI's response to the query.
    """
    # Simple keyword-based responses for demonstration
    responses = {
        "hello": "Hello! How can I assist you today?",
        "help": "Sure! What do you need help with?",
        "bye": "Goodbye! Have a great day!",
        "what is your name": "I am your AI assistant.",
        "how are you": "I'm just a program, but I'm here to help you!",
    }

    # Generate response based on query
    response = responses.get(query.lower(), "I'm sorry, I didn't understand that.")
    return response

# Example usage
if __name__ == "__main__":
    user_query = input("Ask the AI assistant: ")
    ai_response = ai_assistant_query(user_query)
    print(ai_response)
