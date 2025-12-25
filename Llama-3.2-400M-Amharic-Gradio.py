#!/usr/bin/env python3
import os
import sys
from threading import Thread
import time

# Automatic installation of dependencies
try:
    import gradio as gr
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, pipeline
    from gtts import gTTS 
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers", "torch", "accelerate", "gTTS", "gradio"])
    import gradio as gr
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, pipeline
    from gtts import gTTS

# Model configuration
MODEL_ID = "rasyosef/Llama-3.2-400M-Amharic-Instruct-Poems-Stories-Wikipedia"
AUDIO_DIR = "./audio_responses"
os.makedirs(AUDIO_DIR, exist_ok=True)
audio_counter = 0

# High-Quality Profile Pictures
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/3702/3702165.png"
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/17701/17701286.png"

# Load model and tokenizer
print(f"Loading model: {MODEL_ID}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    device_map="auto"
)

llama3_am = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    eos_token_id=tokenizer.eos_token_id,
)

def text_to_speech_free(text, audio_count):
    """Free Amharic TTS using gTTS"""
    try:
        audio_file = os.path.join(AUDIO_DIR, f"response_{audio_count}.mp3")
        tts = gTTS(text=text, lang='am')
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"TTS Error: {e}")
        return None

# Custom CSS for clean chat interface
custom_css = """
/* Full-width container with clean padding */
#main-container { max-width: 1200px; margin: 0 auto; padding: 1rem; }

/* Chatbot styling: Larger, no heavy borders, clean shadow */
#chatbot-container { 
    border: none !important; 
    background: transparent !important;
}

/* Make chat bubbles feel more like modern AI apps */
.message-wrap { font-size: 1.1rem !important; }

.footer-section { text-align: center; margin-top: 3rem; padding: 1rem; color: #6c757d; font-size: 0.9rem; }
.footer-section a { text-decoration: none; font-weight: bold; color: inherit; }

* { font-family: 'Noto Sans Ethiopic', sans-serif; }

#minimal-audio { margin: 10px auto; max-width: 600px; border: none; background: transparent; }

/* Floating input look */
#input-row { 
    padding: 1rem;
    background: white;
    border-radius: 15px;
    box-shadow: 0 -5px 25px rgba(0,0,0,0.05);
}

/* Settings panel styling */
#settings-panel {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 15px;
    margin-top: 2rem;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="Amharic AI Chat") as demo:
    with gr.Column(elem_id="main-container"):
        # Main Chat Area
        chatbot = gr.Chatbot(
            height=700,
            elem_id="chatbot-container", 
            show_label=False, 
            avatar_images=(USER_AVATAR, BOT_AVATAR), 
            bubble_full_width=False,
            type="messages"
        )
        
        with gr.Group(visible=False, elem_id="minimal-audio") as audio_group:
            audio_output = gr.Audio(label=None, interactive=False, autoplay=True, show_label=False, container=False)
        
        with gr.Row(elem_id="input-row"):
            msg = gr.Textbox(
                placeholder="መልእክትዎን እዚህ ይጻፉ...", 
                show_label=False, 
                container=False, 
                scale=10,
                autofocus=True
            )
            send_btn = gr.Button("ላክ", variant="primary", scale=1)
        
        gr.Markdown("### 💡 የጥያቄ መነሻዎች")
        gr.Examples(
            examples=[
                ["ሰላም"],
                ["ሰላም፣ እንዴት ነህ?"],
                ["አንተ ማንህ?"],
                ["ስለ ኢትዮጵያ የዘመን አቆጣጠር ንገረኝ?"],
                ["የአባይ ወንዝ መነሻና መደረሻ የት ነው?"],
                ["ስለ አቡሸከር (የዘመን ስሌት) ምን ይታወቃል?"],
                ["ለእናቴ የሚሆን አጭር የፍቅር ግጥም ጻፍልኝ?"],
                ["ሰው ሰራሽ አስተውሎት (AI) ምንድን ነው?"],
                ["ስለ አክሱም ሥልጣን ታሪካዊ ውይይታ አብራራልኝ?"],
                ["ጥሩ የጤና አጠባበቅ ምክሮችን ንገረኝ?"],
                ["አጭርና አስቂኝ ቀልድ ንገረኝ?"],
                ["ግጥም ጻፍልኝ"],
                ["ስለ ይቅርታ ግጥም ጻፍልኝ"],
                ["አንድ ተረት አጫውተኝ"],
                ["ስለ ጽጉብና አንበሳ ተረት ንገረኝ"],
                ["ቀልድ ንገረኝ"],
                ["ስለ ስራ አጥነት አንድ ቀልድ ንገረኝ"],
                ["ዳግማዊ ቴዎድሮስ ማን ነው?"],
                ["ዳግማዊ ምኒልክ ማን ነው?"],
                ["ስለ አዲስ አበባ ዩኒቨርስቲ ጥቂት እውነታዎችን አጫውተኝ"],
                ["ስለ ጃፓን ጥቂት እውነታዎችን ንገረኝ"],
                ["ስለ ማይክሮሶፍት ጥቂት እውነታዎችን ንገረኝ"],
                ["ጉጉል ምንድን ነው?"],
                ["ቢትኮይን ምንድን ነው?"]
            ],
            inputs=msg,
            examples_per_page=12
        )
        
        # Settings at the bottom
        with gr.Accordion("⚙️ ማስተካከያ", open=False, elem_id="settings-panel") as settings:
            with gr.Row():
                max_tokens = gr.Slider(32, 1024, 256, step=32, label="የመልስ ርዝመት")
                voice_enabled = gr.Checkbox(label="ድምጽ ይበራ", value=True)
                clear_btn = gr.Button("ታሪክ አጽዳ", variant="stop")
        
        gr.HTML("""
        <div class="footer-section">
            <p>በ Llama 3.2 Amharic እና gTTS የተገነባ</p>
            <p>Credits: <a href="#">@rasyosef</a> & <a href="#">@ababiya</a></p>
        </div>
        """)

    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": ""}]

    def bot(history, max_tokens, voice_enabled):
        global audio_counter
        
        user_message = history[-2]["content"]
        
        recent_history = history[:-2][-6:]
        formatted_history = []
        for msg in recent_history:
            formatted_history.append(msg)
        formatted_history.append({"role": "user", "content": user_message})
        
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        thread = Thread(target=llama3_am, kwargs={
            "text_inputs": formatted_history,
            "max_new_tokens": max_tokens,
            "repetition_penalty": 1.1,
            "streamer": streamer
        })
        thread.start()
        
        generated_text = ""
        for word in streamer:
            generated_text += word
            history[-1]["content"] = generated_text.strip()
            yield history, None, gr.update(visible=False)
        
        audio_file = None
        if voice_enabled and generated_text.strip():
            audio_counter += 1
            audio_file = text_to_speech_free(generated_text.strip(), audio_counter)
        
        yield history, audio_file, gr.update(visible=(audio_file is not None))

    # Event handlers
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, max_tokens, voice_enabled], [chatbot, audio_output, audio_group]
    )
    send_btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, max_tokens, voice_enabled], [chatbot, audio_output, audio_group]
    )
    clear_btn.click(fn=lambda: ([], None, gr.update(visible=False)), outputs=[chatbot, audio_output, audio_group])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, favicon_path=BOT_AVATAR)