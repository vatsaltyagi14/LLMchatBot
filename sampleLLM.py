import ollama

def chat_with_llama():
    model_name = 'llama3.2:3b'  # You can change this to 'llama3.2:1b' if you downloaded the 1B model
    
    print("Chat with Llama 3.2 (Type 'exit' to end the conversation)")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Ending conversation. Goodbye!")
            break
        
        response = ollama.chat(model=model_name, messages=[
            {
                'role': 'user',
                'content': user_input,
            },
        ])
        
        assistant_response = response['message']['content']
        print("Llama:", assistant_response)

if __name__ == "__main__":
    chat_with_llama()
