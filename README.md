## 🤖Llama_3.2_400M_Amharic_Chat_Demo
![llma_amh](https://github.com/user-attachments/assets/33f6c59d-3b7d-4d66-83e6-79cb6a44fa7c)

An local interactive Amharic language chatbot powered by Llama 3.2 with text-to-speech capabilities. This application provides a modern chat interface for conversing in Amharic with AI-powered responses and optional voice output.

## Features ✨

- **Native Amharic Support**: Full conversation support in Amharic language
- **Streaming Responses**: Real-time text generation for smooth user experience
- **Text-to-Speech**: Optional voice output using Google Text-to-Speech (gTTS)
- **Modern UI**: Clean, responsive chat interface inspired by contemporary AI assistants
- **Conversation History**: Maintains context across multiple turns
- **Customizable Settings**: Adjust response length and toggle voice output
- **Pre-loaded Examples**: Quick-start prompts covering various topics

## Model Information 📚

This chatbot uses the **Llama-3.2-400M-Amharic-Instruct** model, specifically trained on:
- Amharic poems
- Stories
- Wikipedia content

Model ID: `rasyosef/Llama-3.2-400M-Amharic-Instruct-Poems-Stories-Wikipedia`

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. Clone this repository:
```bash
git clone https://github.com/ababiyaworku/Llama_3.2_400M_Amharic_Chat_Demo.git
cd Llama_3.2_400M_Amharic_Chat_Demo
```

2. Run the script (dependencies will auto-install):
```bash
python Llama-3.2-400M-Amharic-Gradio.py
```

The script automatically installs required packages:
- `transformers`
- `torch`
- `accelerate`
- `gTTS`
- `gradio`

3. Open your browser and navigate to:
```
http://localhost:7860
```

## Usage 💬

### Starting a Conversation

1. Type your message in Amharic in the text box
2. Press Enter or click the "ላክ" (Send) button
3. Wait for the AI response to stream in
4. Audio will automatically play if voice is enabled

![llama_amh_02](https://github.com/user-attachments/assets/2893e9b5-0a04-4b64-8d97-8262fa728b9f)

### Settings

Access settings by expanding the "⚙️ ማስተካከያ" accordion at the bottom:

- **የመልስ ርዝመት (Response Length)**: Adjust the maximum length of responses (32-1024 tokens)
- **ድምጽ ይበራ (Enable Voice)**: Toggle text-to-speech output
- **ታሪክ አጽዳ (Clear History)**: Reset the conversation

### Example Prompts

The interface includes pre-loaded examples covering:
- Greetings and basic conversation
- Ethiopian history and culture
- Poetry and storytelling
- Educational topics (AI, technology, health)
- Jokes and entertainment

## Configuration ⚙️

### Model Settings

You can modify these constants in the script:

```python
MODEL_ID = "rasyosef/Llama-3.2-400M-Amharic-Instruct-Poems-Stories-Wikipedia"
AUDIO_DIR = "./audio_responses"  # Directory for saved audio files
```

### Server Settings

Customize the launch parameters:

```python
demo.launch(
    server_name="0.0.0.0",  # Listen on all interfaces
    server_port=7860,        # Port number
    favicon_path=BOT_AVATAR
)
```

## Technical Details 🔧

### Architecture

- **Framework**: Gradio for web interface
- **Model**: Llama 3.2 (400M parameters)
- **TTS Engine**: Google Text-to-Speech (gTTS)
- **Context Window**: Last 3 conversation turns (6 messages)

### Features Implementation

- **Streaming**: Uses `TextIteratorStreamer` for real-time response generation
- **Threading**: Separate thread for model inference to prevent UI blocking
- **Audio Caching**: Saves generated audio files to disk
- **Responsive Design**: CSS-styled interface with modern aesthetics

## Requirements 📋

```
gradio>=4.0.0
torch>=2.0.0
transformers>=4.30.0
accelerate>=0.20.0
gTTS>=2.3.0
```

## Troubleshooting 🔍

### Common Issues

**Model Loading Errors**
- Ensure you have sufficient RAM (4GB+ recommended)
- Check internet connection for initial model download

**Audio Not Playing**
- Verify browser audio permissions
- Check that gTTS has internet access

**Slow Performance**
- Reduce max_tokens slider value
- Consider using GPU if available

## Credits 👏

- **Model Training**: [@rasyosef](https://github.com/rasyosef)
- **Development**: [@ababiya](https://github.com/ababiyaworku)
- **Framework**: [Gradio](https://gradio.app/)
- **Model**: [Meta Llama 3.2](https://huggingface.co/meta-llama)
- **TTS**: [gTTS](https://github.com/pndurette/gTTS)

## Acknowledgments 🙏

Special thanks to the Amharic NLP community and all contributors to the open-source tools that made this project possible.

---

**Note**: This is an experimental project. Responses may not always be accurate. Use responsibly and verify important information from reliable sources.
