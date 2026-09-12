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

@bot.command(name="bypass")
async def bypass(ctx, *, link: str = None):
    if not link:
        await ctx.send("🌸 Sếp vui lòng nhập kèm link cần bypass nha! Ví dụ: `!bypass https://link...` 🎀")
        return
    
    # Gửi tin nhắn đang xử lý cho Sếp đỡ sốt ruột
    await ctx.send(f"⏳ Đang tiến hành bypass link cho Sếp: `{link}`... Chờ em một chút xíu nha! ✨")
    
    # --- KHU VỰC THÊM THUẬT TOÁN BYPASS CỦA SẾP Ở ĐÂY ---
    # Hiện tại em viết mẫu kết quả trả về, Sếp có thể thay logic thật vào nhé:
    ket_qua = f"✨ Đã bypass thành công link của Sếp:\n||{link}||"
    
    await ctx.send(ket_qua)

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
