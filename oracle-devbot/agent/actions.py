import pyautogui
import subprocess
import time
from config import SCREENSHOT_PATH

def take_screenshot():
    """Capture screenshot using pyautogui."""
    pyautogui.screenshot(SCREENSHOT_PATH)
    return SCREENSHOT_PATH

def execute_action(action_data):
    """
    Execute the action returned by the LLM.
    Returns command output for terminal actions, or None otherwise.
    """
    action = action_data.get('action')
    params = action_data.get('params', {})
    thought = action_data.get('thought', '')
    
    print(f"[AGENT THOUGHT]: {thought}")
    
    if action == 'click':
        x, y = params.get('x'), params.get('y')
        print(f"🖱️ Clicking at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(1)
        
    elif action == 'type':
        text = params.get('text', '')
        print(f"⌨️ Typing: {text}")
        pyautogui.write(text)
        time.sleep(0.5)
        
    elif action == 'terminal':
        cmd = params.get('text', '')
        print(f"💻 Executing Terminal: {cmd}")
        try:
            # Run command and capture output for the next loop
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)
            
    elif action == 'wait':
        duration = params.get('duration', 2)
        print(f"⏳ Waiting {duration}s...")
        time.sleep(duration)
        
    elif action == 'finish':
        return "TASK_COMPLETED"
    
    return None
