import os

# LM Studio Settings
LM_STUDIO_URL = "http://192.168.1.50:1234/v1"  # Replace with your Host IP
MODEL_NAME = "qwen2-vl-7b-instruct"  # Must match the loaded model in LM Studio

# Telegram Settings
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
ADMIN_CHAT_ID = "YOUR_TELEGRAM_USER_ID"

# Paths
SCREENSHOT_PATH = "/tmp/screen.png"
PROJECT_DIR = "/home/user/android_projects"
LOG_FILE = "logs/oracle.log"

# Safety Limits
MAX_ITERATIONS = 50  # Prevent infinite loops
