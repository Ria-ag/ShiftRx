from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import json
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_constraints(text):
    system_prompt = open("prompt.txt").read()
    user_prompt = open("extract.txt").read().replace("{USER_INPUT}", text)
    schema = json.load(open("icr.schema.json"))
    full_prompt = f"""{user_prompt}

Return ONLY valid JSON matching this exact schema (no markdown, no explanation):

{json.dumps(schema, indent=2)}

JSON output:"""
    
    print("Calling Groq API...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.1,
        max_tokens=4000,
        top_p=1,
    )
    
    result_text = response.choices[0].message.content
    
    print("\n--- API Response Preview ---")
    print(result_text[:300] + "..." if len(result_text) > 300 else result_text)
    print("--- End Preview ---\n")
    
    result_text = result_text.strip()
    
    if "```json" in result_text:
        result_text = result_text.split("```json")[1].split("```")[0].strip()
    elif "```" in result_text:
        parts = result_text.split("```")
        if len(parts) >= 3:
            result_text = parts[1].strip()
    
    start_idx = result_text.find("{")
    end_idx = result_text.rfind("}") + 1
    
    if start_idx != -1 and end_idx > start_idx:
        result_text = result_text[start_idx:end_idx]
    else:
        raise ValueError("No valid JSON found in API response")
    
    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print("Attempting to fix common issues...")
        
        result_text = result_text.replace("'", '"')
        result_text = result_text.replace(",\n}", "\n}")
        result_text = result_text.replace(",\n]", "\n]")
        
        return json.loads(result_text)