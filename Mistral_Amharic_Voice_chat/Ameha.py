import os
from PIL import Image
import torch
from transformers import AutoProcessor, AutoTokenizer
from ctransformers import AutoModelForCausalLM

def find_model(model_dir):
    gguf_files = [f for f in os.listdir(model_dir) if f.endswith('.gguf')]
    if not gguf_files:
        print(f"No .gguf model files found in {model_dir}")
        return None
    if len(gguf_files) > 1:
        print(f"Multiple .gguf files found. Using the first one: {gguf_files[0]}")
    return os.path.join(model_dir, gguf_files[0])

def load_vision_model(model_path):
    try:
        model = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama")
        processor = AutoProcessor.from_pretrained("NousResearch/Nous-Hermes-2-Vision")
        tokenizer = AutoTokenizer.from_pretrained("NousResearch/Nous-Hermes-2-Vision")
        return model, processor, tokenizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None, None

def caption_image(image_path, model, processor, tokenizer):
    try:
        image = Image.open(image_path)
        inputs = processor(images=image, return_tensors="pt")
        
        pixel_values = inputs.pixel_values
        prompt = "Describe this image in detail:"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        outputs = model.generate(
            input_ids=input_ids,
            pixel_values=pixel_values,
            max_new_tokens=100,
            num_return_sequences=1,
        )
        
        caption = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def main():
    model_dir = input("Please enter the full path to the directory containing the vision model: ")

    model_path = find_model(model_dir)
    if not model_path:
        return

    model, processor, tokenizer = load_vision_model(model_path)
    if model is None or processor is None or tokenizer is None:
        return

    current_dir = os.getcwd()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_files = [f for f in os.listdir(current_dir) if any(f.lower().endswith(ext) for ext in image_extensions)]

    if not image_files:
        print("No images found in the current directory.")
        return

    for image_file in image_files:
        image_path = os.path.join(current_dir, image_file)
        caption = caption_image(image_path, model, processor, tokenizer)
        
        if caption:
            txt_file = os.path.splitext(image_file)[0] + ".txt"
            txt_path = os.path.join(current_dir, txt_file)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"Image: {image_file}\n")
                f.write(f"Caption: {caption}\n")
            
            print(f"Processed: {image_file}")
            print(f"Caption saved to: {txt_file}")
        else:
            print(f"Failed to process: {image_file}")

    print("All images processed.")

if __name__ == "__main__":
    main()