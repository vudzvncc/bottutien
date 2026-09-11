import os
import asyncio
import threading
import requests
import discord
from discord.ext import commands
from flask import Flask

Khởi động Web Server giả lập để UptimeRobot "báo thức" 24/7
app = Flask('')

@app.route('/')
def home():
    return "🌸 Bot Discord Python của Sếp đang chạy mượt mà 24/7 luôn nè! ✨"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()

Cấu hình Bot Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!bypass ', intents=intents)

@bot.event
async def on_ready():
    print(f'🌸 Bot Python Rikaa đã online thành công: {bot.user} ✨')

@bot.command(name='bypass')
async def bypass_link(ctx, target_url: str = None):
    if not target_url: 
await ctx.reply('Sếp ơi, hãy gửi kèm link cuty.io cần giải mã nha! Ví dụ: !bypass https://cuty.io/xxxx 🌸')
        return

    status_msg = await ctx.reply('⏳ Em đang "đâm xuyên" qua lớp bảo mật cuty.io cho Sếp nè, chờ em xíu siêu nha... ✨')

    try:
        # Gọi API Bypass chuyên dụng để bẻ khóa link cuty.io
        api_url = f"https://api.bypass.vip/bypass?url={target_url}"
        response = requests.get(api_url, timeout=15)
        data = response.json()

        if data.get('status') == 'success' and data.get('destination'):
            final_link = data['destination']

            if final_link == target_url:
                await status_msg.edit('🥺 Link cuty.io này bị khóa hoặc hỏng rồi Sếp ơi!')
            else:
                await status_msg.edit(f'🎉 GIẢI MÃ THÀNH CÔNG RỒI SẾP ƠI! 🌸\n🔗 Link gốc đích thực đây ạ:\n{final_link}')
        else:
            await status_msg.edit('😭 Link cuty.io này bị hỏng hoặc hết hạn rồi Sếp ơi!')

    except Exception as e:
        print(f"Lỗi khi bypass: {e}")
        await status_msg.edit('⚠️ Server bypass đang bận một chút, Sếp thử lại sau vài giây nha! 🌸')

Chạy web server và khởi động Bot Discord
if name == "main":
    keep_alive()
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("⚠️ Lỗi: Chưa cấu hình biến môi trường DISCORD_TOKEN trên Render!")