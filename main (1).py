# File: main.py
import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# 1. Khởi tạo Web Server giả lập để UptimeRobot giữ bot online 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "🌸 Bot Discord dang hoat dong cuc ky on dinh! ✨"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

# 2. Cấu hình Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🌸 Bot da online thanh cong voi ten: {bot.user} ✨")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Do tre hien tai la: {round(bot.latency * 1000)}ms 🎀")

# 3. Chạy Server và Bot
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Loi: Chua tim thay bien DISCORD_TOKEN trong Environment!")