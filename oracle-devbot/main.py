import time
import json
import threading
from agent.llm_client import ask_agent
from agent.actions import execute_action, take_screenshot
from agent.telegram_bot import TelegramInterface
from config import MAX_ITERATIONS, PROJECT_DIR

# Initialize
tg_bot = TelegramInterface()
history = []

def run_agent_loop(task_description):
    """
    Main ReAct loop: Reason (Think) -> Act -> Observe -> Repeat
    """
    global history
    history = [{
        "role": "user", 
        "content": f"Task: {task_description}. Start by opening Android Studio or setting up the environment."
    }]
    
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        
        # 1. See - Take screenshot of current screen
        screenshot_path = take_screenshot()
        
        # 2. Think - Ask LLM what to do next
        response = ask_agent(history, screenshot_path)
        thought = response.get('thought', '')
        
        # Log to Telegram occasionally (every 5 iterations)
        if iteration % 5 == 0:
            tg_bot.send_update(f"Iteration {iteration}: {thought}", screenshot_path)
        
        # 3. Act - Execute the action
        result = execute_action(response)
        
        # 4. Feedback Loop - Check if task is complete
        if result == "TASK_COMPLETED":
            tg_bot.send_update("✅ Build Complete! Check the project folder.")
            break
            
        # Add action result to history for context
        if result:
            history.append({"role": "assistant", "content": thought})
            history.append({"role": "user", "content": f"Action Result: {result}"})
        else:
            history.append({"role": "assistant", "content": thought})
            
        time.sleep(2)  # Cool down between iterations

if __name__ == "__main__":
    # Start Telegram bot in a separate thread
    t = threading.Thread(target=tg_bot.run)
    t.daemon = True
    t.start()
    
    print("Waiting for /build command via Telegram...")
    # In a real app, use a queue or event listener triggered by Telegram callback
    # For demo, we simulate a trigger:
    while True:
        if tg_bot.current_task:
            task = tg_bot.current_task
            tg_bot.current_task = None
            run_agent_loop(task)
        time.sleep(1)
