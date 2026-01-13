import asyncio
import edge_tts
import os

async def text_to_speech(text, output_file):
    voice = "am-ET-MekdesNeural"  # Amharic voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def main():
    # Amharic text to convert to speech
    amharic_text = "ሰላም፣ ይህ የአማርኛ ንግግር ናሙና ነው።"
    
    # Output file name
    output_file = "amharic_speech.mp3"
    
    # Get the current directory
    current_dir = os.getcwd()
    
    # Full path for the output file
    output_path = os.path.join(current_dir, output_file)
    
    # Run the text-to-speech conversion
    asyncio.run(text_to_speech(amharic_text, output_path))
    
    print(f"Speech saved to: {output_path}")

if __name__ == "__main__":
    main()