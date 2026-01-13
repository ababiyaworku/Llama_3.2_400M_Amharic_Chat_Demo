import asyncio
import edge_tts
import os
import re
import torch
from ctransformers import AutoModelForCausalLM as CTransformersAutoModel
from transformers import AutoModelForCausalLM as HFModel, AutoTokenizer

async def text_to_speech(text, output_file):
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def chat_with_model(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors='pt').to('cuda' if torch.cuda.is_available() else 'cpu')
    outputs = model.generate(inputs['input_ids'], max_new_tokens=200)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def sanitize_filename(filename):
    return re.sub(r'[^\w\s]', '', filename).replace(' ', '_')

def load_model(model_path, model_file):
    ext = os.path.splitext(model_file)[1]
    model = None
    tokenizer = None

    if ext in ['.bin', '.tar.gz']:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = HFModel.from_pretrained(model_path)
            model.to('cuda' if torch.cuda.is_available() else 'cpu')
            print(f"Loaded Hugging Face model: {model_path}")
        except Exception as e:
            print(f"Error loading Hugging Face model: {e}")
    elif ext in ['.gguf', '.ggml']:
        try:
            model = CTransformersAutoModel.from_pretrained(model_path)
            print(f"Loaded CTransformers model: {model_path}")
        except Exception as e:
            print(f"Error loading CTransformers model: {e}")
    
    return model, tokenizer

def main():
    model_dir = input("Please enter the full path to the directory containing your AI model: ")
    
    model_extensions = ['.gguf', '.bin', '.ggml', '.tar.gz']
    model_files = [f for f in os.listdir(model_dir) if any(f.endswith(ext) for ext in model_extensions)]
    
    if not model_files:
        print("No compatible model files found in the specified directory.")
        return

    if len(model_files) > 1:
        print("Multiple model files found. Please choose one:")
        for i, file in enumerate(model_files):
            print(f"{i + 1}. {file}")
        choice = int(input("Enter the number of your choice: ")) - 1
        model_file = model_files[choice]
    else:
        model_file = model_files[0]

    model_path = os.path.join(model_dir, model_file)
    model, tokenizer = load_model(model_path, model_file)

    if model is None:
        print("Failed to load the model.")
        return

    while True:
        prompt = input("Enter your prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break

        response = chat_with_model(model, tokenizer, prompt) if tokenizer else model(prompt, max_new_tokens=200)
        print(f"Response: {response}")
        
        sanitized_prompt = sanitize_filename(prompt)
        output_file = f"{sanitized_prompt[:50]}.mp3"
        asyncio.run(text_to_speech(response, output_file))
        print(f"Audio saved as {output_file}")

if __name__ == "__main__":
    main()
