import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Environment Variables
# -------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables")

# -------------------------------------------------
# In-memory session state (simple & safe)
# -------------------------------------------------
STATE = {
    "session": False,
    "ce_running": False,
    "pe_running": False,
    "sl": None,
    "trail": False,
}

# -------------------------------------------------
# Command Handlers
# -------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Neo Trading Bot Online*\n\n"
        "Available Commands:\n"
        "/login – Login to Kotak Neo\n"
        "/status – Show current status\n"
        "/exitall – Exit all running trades\n\n"
        "⚠️ Orders & SL will be enabled after login.",
        parse_mode="Markdown",
    )


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Placeholder login.
    Real Kotak Neo login (OTP/TOTP/MPIN) must be
    done using official SDK flow (not via Telegram input).
    """
    STATE["session"] = True

    await update.message.reply_text(
        "✅ *Login successful (placeholder)*\n\n"
        "Kotak Neo API session marked as active.\n"
        "You can now place orders.",
        parse_mode="Markdown",
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"📊 *BOT STATUS*\n\n"
        f"SESSION: `{STATE['session']}`\n"
        f"CE RUNNING: `{STATE['ce_running']}`\n"
        f"PE RUNNING: `{STATE['pe_running']}`\n"
        f"SL: `{STATE['sl']}`\n"
        f"TRAIL ACTIVE: `{STATE['trail']}`"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def exit_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not STATE["ce_running"] and not STATE["pe_running"]:
        await update.message.reply_text("ℹ️ No active positions to exit.")
        return

    STATE["ce_running"] = False
    STATE["pe_running"] = False
    STATE["sl"] = None
    STATE["trail"] = False

    await update.message.reply_text(
        "🛑 *EXIT ALL EXECUTED*\n\n"
        "All CE & PE baskets stopped.\n"
        "You can start fresh with new strikes/expiry.",
        parse_mode="Markdown",
    )


# -------------------------------------------------
# Unknown command handler
# -------------------------------------------------
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Unknown command. Type /start")

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Core commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("exitall", exit_all))

    # Fallback
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Bot started successfully")

    # IMPORTANT: do NOT wrap in asyncio.run()
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
