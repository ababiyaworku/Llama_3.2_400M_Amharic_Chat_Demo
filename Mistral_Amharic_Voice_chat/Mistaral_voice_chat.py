import asyncio
import edge_tts
import os
from ctransformers import AutoModelForCausalLM

async def text_to_speech(text, output_file):
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def chat_with_model(model, prompt):
    response = model(prompt, max_new_tokens=200)
    return response

def main():
    # Ask user for model directory
    model_dir = input("Please enter the full path to the directory containing your AI model: ")
    
    # List all potential model files in the directory
    model_extensions = ['.gguf', '.bin', '.ggml']  # Add more extensions if needed
    model_files = [f for f in os.listdir(model_dir) if any(f.endswith(ext) for ext in model_extensions)]
    
    if not model_files:
        print("No compatible model files found in the specified directory.")
        return

    # If multiple models found, let user choose
    if len(model_files) > 1:
        print("Multiple model files found. Please choose one:")
        for i, file in enumerate(model_files):
            print(f"{i+1}. {file}")
        choice = int(input("Enter the number of your choice: ")) - 1
        model_file = model_files[choice]
    else:
        model_file = model_files[0]

    model_path = os.path.join(model_dir, model_file)

    # Initialize model
    try:
        # Try to automatically determine the model type
        model = AutoModelForCausalLM.from_pretrained(model_path)
        print(f"Model loaded successfully: {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Trying to load with specific model types...")
        
        # If automatic loading fails, try specific model types
        model_types = ["llama", "gpt2", "gptj", "gpt_neox", "mpt", "falcon", "starcoder"]
        for model_type in model_types:
            try:
                model = AutoModelForCausalLM.from_pretrained(model_path, model_type=model_type)
                print(f"Model loaded successfully as {model_type}: {model_path}")
                break
            except Exception:
                continue
        else:
            print("Failed to load the model with any known type. Please ensure it's a compatible model.")
            return

    # Get the current directory for saving audio files
    current_dir = os.getcwd()

    conversation_count = 0

    print("Chatbot initialized. Type 'quit' to exit.")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Chat with model
        prompt = f"Human: {user_input}\nAssistant:"  # Generic prompt format
        response = chat_with_model(model, prompt)
        print("Assistant:", response)

        # Generate speech
        conversation_count += 1
        output_file = f"conversation_{conversation_count}.mp3"
        output_path = os.path.join(current_dir, output_file)
        asyncio.run(text_to_speech(response, output_path))
        print(f"Speech saved to: {output_path}")

if __name__ == "__main__":
    main()