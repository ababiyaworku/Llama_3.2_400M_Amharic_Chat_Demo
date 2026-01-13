import asyncio
import edge_tts
import os
import openai
from googletrans import Translator

async def text_to_speech(text, output_file):
    voice = "am-ET-MekdesNeural"  # Amharic voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def translate_to_amharic(text):
    translator = Translator()
    translation = translator.translate(text, dest='am')
    return translation.text

def chat_with_gpt(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def main():
    # Get OpenAI API key
    api_key = input("Please enter your OpenAI API key: ")

    # Get the current directory
    current_dir = os.getcwd()

    conversation_count = 0

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        # Chat with GPT
        response = chat_with_gpt(api_key, user_input)
        print("Assistant (English):", response)

        # Translate to Amharic
        amharic_response = translate_to_amharic(response)
        print("Assistant (Amharic):", amharic_response)

        # Generate speech
        conversation_count += 1
        output_file = f"conversation_{conversation_count}.mp3"
        output_path = os.path.join(current_dir, output_file)
        asyncio.run(text_to_speech(amharic_response, output_path))
        print(f"Speech saved to: {output_path}")

if __name__ == "__main__":
    main()