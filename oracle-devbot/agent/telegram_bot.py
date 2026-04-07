from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncio
from config import TELEGRAM_TOKEN, ADMIN_CHAT_ID

class TelegramInterface:
    """Handles Telegram bot communication."""
    
    def __init__(self):
        self.app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.current_task = None
        self.setup_handlers()

    def setup_handlers(self):
        """Set up command and message handlers."""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("build", self.build_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text("🤖 Oracle DevBot Online. Send /build 'App Idea' to start.")

    async def build_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /build command with app idea."""
        if update.effective_user.id != int(ADMIN_CHAT_ID):
            return
        idea = " ".join(context.args)
        if not idea:
            await update.message.reply_text("Usage: /build [App Idea]")
            return
        
        await update.message.reply_text(f"🚀 Starting build for: '{idea}'... I will send updates shortly.")
        self.current_task = idea
        # Trigger the main loop (handled in main.py)

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        # Forward manual instructions to the agent
        pass 

    def send_update(self, text, image_path=None):
        """Send update message to Telegram, optionally with screenshot."""
        async def _send():
            await self.app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
            if image_path:
                await self.app.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=open(image_path, 'rb'))
        asyncio.run(_send())

    def run(self):
        """Start the Telegram bot polling."""
        self.app.run_polling()
