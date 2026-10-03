import ollama

def ask_llama(prompt_text):
    print("Thinking...")
    
    # Call the local Ollama engine
    response = ollama.chat(
        model='qwen2.5:3b', 
        messages=[
            {
                'role': 'user',
                'content': prompt_text,
            },
        ]
    )
    
    # Extract and return the text response
    return response['message']['content']

# Example usage
if __name__ == "__main__":
    user_prompt = "Give me 3 quick tips for studying programming efficiently."
    ai_response = ask_llama(user_prompt)

    print("\n--- AI Response ---")
    print(ai_response)