import os
import json
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from datasets import Dataset

def extract_text(file_path):
    """Basic extraction from various formats."""
    ext = os.path.splitext(file_path)[1].lower()
    text_content = []
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content.append(f.read())
        elif ext == '.csv':
            df = pd.read_csv(file_path)
            text_content.append(df.to_string())
        elif ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                text_content.append(page.extract_text())
        elif ext == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text_content.append(para.text)
    except Exception: pass
    return "\n".join(filter(None, text_content))

def run_conversion():
    supported_extensions = {'.json', '.csv', '.txt', '.docx', '.pdf', '.jsonl'}
    rows = []

    files = [f for f in os.listdir('.') if os.path.splitext(f)[1].lower() in supported_extensions]
    
    for file_name in files:
        raw_text = extract_text(file_name)
        if not raw_text.strip(): continue

        # Break into chunks
        chunks = [raw_text[i:i+2000] for i in range(0, len(raw_text), 2000)]
        
        for chunk in chunks:
            # We create the structure found in Multilingual-Thinking
            rows.append({
                "reasoning_language": "Amharic",
                "developer": "You are a helpful Amharic AI assistant. Reasoning: medium",
                "user": "ተጨማሪ የአማርኛ ጽሑፎችን አቅርብልኝ (Provide me more Amharic text)", # Simulated user request
                "analysis": "", # Leave empty as you have no reasoning traces
                "final": chunk, # Your actual Amharic corpus text
                "messages": [
                    {"role": "system", "content": "You are a helpful Amharic AI assistant. Reasoning: medium"},
                    {"role": "user", "content": "ተጨማሪ የአማርኛ ጽሑፎችን አቅርብልኝ"},
                    {"role": "assistant", "content": chunk, "thinking": ""}
                ]
            })

    dataset = Dataset.from_list(rows)
    
    # Save in your requested formats
    dataset.to_csv("amharic_harmony.csv", index=False)
    dataset.to_json("amharic_harmony.jsonl", orient="records", lines=True, force_ascii=False)
    dataset.to_parquet("amharic_harmony.parquet")
    print(f"Success! Created {len(rows)} rows with reasoning/developer columns.")

if __name__ == "__main__":
    run_conversion()