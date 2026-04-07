# 🤖 The Oracle DevBot

An autonomous Android Developer Agent that connects **Telegram**, a **Local Qwen Coder/Vision Model** (via LM Studio), and an **Ubuntu VM** running Android Studio.

## Architecture

The agent uses a **ReAct (Reasoning + Acting)** loop:
1. **See**: Takes screenshots of the screen
2. **Think**: Analyzes the screen using Qwen-VL vision model
3. **Act**: Executes commands (click, type, terminal)
4. **Repeat**: Continues until the app is built

## Project Structure

```
oracle-devbot/
├── config.py                # Configuration (API keys, paths, model settings)
├── requirements.txt         # Python dependencies
├── main.py                  # The main orchestration loop (LangGraph style)
├── agent/
│   ├── __init__.py
│   ├── llm_client.py        # Connects to LM Studio (Qwen)
│   ├── actions.py           # PyAutoGUI, ADB, Terminal execution
│   └── telegram_bot.py      # Handles Telegram commands & uploads
├── skills/                  # Memory store for learned solutions (JSON/Vector)
└── logs/                    # Execution logs
```

## Prerequisites

### A. VirtualBox VM Setup (Ubuntu 24.04)

1. **Install Ubuntu:** Allocate 8GB+ RAM, 4+ CPU cores, 50GB Disk.
2. **Install Android Studio & SDK:**
   ```bash
   sudo apt update
   sudo apt install openjdk-17-jdk wget unzip
   # Download Android Studio Command Line Tools from Google, extract to ~/android-sdk
   # Set ANDROID_HOME and PATH in ~/.bashrc
   sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
   ```
3. **Install Dependencies:**
   ```bash
   sudo apt install python3-pip python3-venv xvfb scrot adb
   pip3 install virtualenv
   python3 -m venv venv
   source venv/bin/activate
   ```

### B. Host Machine (LM Studio)

1. **Download Models:**
   - `Qwen2.5-Coder-7B-Instruct-GGUF` (for code logic)
   - `Qwen2-VL-7B-Instruct-GGUF` (for screen vision) ⭐ Required!

2. **Start Server:**
   - Load the Vision model in LM Studio
   - Go to "Server" tab
   - Enable CORS
   - Port: `1234`
   - Note the Local IP of your host (e.g., `192.168.1.50`)

## Installation

1. **Install Python dependencies:**
   ```bash
   cd oracle-devbot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure settings:**
   Edit `config.py`:
   ```python
   LM_STUDIO_URL = "http://YOUR_HOST_IP:1234/v1"
   MODEL_NAME = "qwen2-vl-7b-instruct"
   TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
   ADMIN_CHAT_ID = "YOUR_TELEGRAM_USER_ID"
   ```

## Usage

1. **Start LM Studio:** Load `Qwen2-VL-7B`, start server on port `1234`.

2. **Ensure Android Emulator is running:**
   ```bash
   adb devices  # Should show connected emulator
   ```

3. **Run the Bot:**
   ```bash
   cd oracle-devbot
   source venv/bin/activate
   python3 main.py
   ```

4. **Interact via Telegram:**
   - Open Telegram on your phone
   - Send: `/build A simple To-Do list app with dark mode`
   - Watch the magic: The VM will wake up, take screenshots, analyze them, open terminals, type code, and send you progress photos.

## Commands

- `/start` - Check bot status
- `/build [App Idea]` - Start building an Android app

## Critical Success Factors

- **Screen Resolution:** Set your VM resolution to a fixed size (e.g., 1920x1080) so `pyautogui` coordinates are predictable.
- **Unrestricted Model:** Ensure you are using a version of Qwen that allows tool use. If it refuses to run terminal commands, switch to `Dolphin-Qwen` or disable safety filters in LM Studio's server settings.
- **ADB Permissions:** Ensure the Android Emulator is running and `adb devices` shows it as connected before starting.
- **Error Handling:** The agent will fail initially. The power of this system is the **loop**. When it fails (e.g., "SDK not found"), it sends the error to the LLM, which then searches for "how to install SDK ubuntu" and tries again.

## Action Types

The LLM can output these actions:

| Action | Parameters | Description |
|--------|-----------|-------------|
| `click` | `x`, `y` | Click at screen coordinates |
| `type` | `text` | Type text using keyboard |
| `terminal` | `text` | Execute shell command |
| `wait` | `duration` | Wait for specified seconds |
| `finish` | - | Mark task as complete |

## Example LLM Response

```json
{
    "thought": "I see Android Studio is open but no project exists. I need to create a new project.",
    "action": "click",
    "params": {
        "x": 450,
        "y": 300
    }
}
```

## License

MIT License - Build your own autonomous dev bot!
