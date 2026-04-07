import requests
import base64
import json
from config import LM_STUDIO_URL, MODEL_NAME

def encode_image(image_path):
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_agent(history, screenshot_path=None):
    """
    Send conversation history and optional screenshot to LM Studio.
    Returns parsed JSON response with thought, action, and params.
    """
    messages = []
    
    # System Prompt: Define the persona and output format
    system_prompt = """
You are an autonomous Android Developer Agent running in an Ubuntu VM.
Your goal is to build Android apps, debug errors, and navigate Android Studio.

OUTPUT FORMAT: You must respond ONLY with a valid JSON object containing:
{
    "thought": "What you see and what you plan to do next.",
    "action": "one of: ['click', 'type', 'terminal', 'wait', 'finish']",
    "params": {
        "x": int, "y": int,  // For click
        "text": str,         // For type or terminal
        "duration": int      // For wait
    }
}

If you see an error in the IDE, search for the solution in your knowledge or suggest a terminal command to fix it.
"""
    
    messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history (text only for brevity in this example)
    for msg in history:
        messages.append({"role": msg['role'], "content": msg['content']})

    # Add Screenshot if available
    if screenshot_path:
        base64_img = encode_image(screenshot_path)
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": "Here is the current screen. Analyze it and decide the next action."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
            ]
        })
    else:
        messages.append({"role": "user", "content": "Proceed with the next step based on previous context."})

    try:
        response = requests.post(f"{LM_STUDIO_URL}/chat/completions", json={
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.2,  # Low temp for deterministic coding
            "max_tokens": 1000
        })
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Extract JSON from response (handle markdown code blocks if present)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        return json.loads(content.strip())
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"thought": "Error contacting LLM", "action": "wait", "params": {"duration": 5}}
