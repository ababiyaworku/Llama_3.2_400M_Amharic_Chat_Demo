import os
import json
import time
import pandas as pd
from pathlib import Path
from datasets import Dataset
from google import genai
from google.genai import types

def setup_client():
    api_key = input("Please enter your Gemini API key: ")
    return genai.Client(api_key=api_key)

def format_harmony_wire(instruction, thought, final_output):
    """Formats into OpenAI Harmony wire format for GPT-OSS 20B."""
    return (
        f"<|start|>system<|message|>You are a helpful assistant that reasons step-by-step in Amharic.<|end|>\n"
        f"<|start|>user<|message|>{instruction}<|end|>\n"
        f"<|start|>assistant<|channel|>analysis<|message|>{thought}<|end|>\n"
        f"<|start|>assistant<|channel|>final<|message|>{final_output}<|end|>"
    )

def generate_dataset(client, total_count=1000):
    dataset_rows = []
    batch_size = 4  # Lower batch size for higher quality per request
    model_id = "gemini-3-pro-preview" 
    
    print(f"🚀 Starting 1000-sample generation with {model_id}...")

    prompt = """
    Generate {batch_size} unique and complex Amharic reasoning tasks.
    Topics: Logic puzzles, Amharic grammar nuances, math word problems, or cultural ethics.
    Return ONLY a JSON list:
    [
      {{"q": "question in Amharic", "t": "step-by-step thinking in Amharic", "a": "answer"}},
      ...
    ]
    """

    while len(dataset_rows) < total_count:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt.format(batch_size=batch_size),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="HIGH")
                )
            )
            
            batch_data = json.loads(response.text)
            for item in batch_data:
                harmony_text = format_harmony_wire(item['q'], item['t'], item['a'])
                dataset_rows.append({
                    "instruction": item['q'],
                    "thought": item['t'],
                    "output": item['a'],
                    "text": harmony_text 
                })
            
            print(f"Progress: {len(dataset_rows)}/{total_count}")
            
            # Rate limit protection: pause briefly between requests
            time.sleep(2) 

        except Exception as e:
            if "429" in str(e):
                print("⚠️ Rate limit hit. Sleeping for 30 seconds...")
                time.sleep(30)
            else:
                print(f"❌ Error: {e}")
                time.sleep(5)
            continue
            
    return dataset_rows[:total_count]

def save_ready_for_hf(data_list):
    folder = "Amharic_reasoning_dataset"
    Path(folder).mkdir(parents=True, exist_ok=True)
    
    # 1. Parquet (Ready for Hugging Face)
    hf_ds = Dataset.from_list(data_list)
    hf_ds.to_parquet(os.path.join(folder, "dataset.parquet"))
    
    # 2. JSONL & CSV
    hf_ds.to_json(os.path.join(folder, "dataset.jsonl"), force_ascii=False)
    pd.DataFrame(data_list).to_csv(os.path.join(folder, "dataset.csv"), index=False, encoding='utf-8-sig')
    
    print(f"\n✅ COMPLETE! 1000 samples saved in: {os.path.abspath(folder)}")

if __name__ == "__main__":
    client = setup_client()
    # Now set to 1000 for the full dataset
    final_data = generate_dataset(client, total_count=1000)
    if final_data:
        save_ready_for_hf(final_data)