# File: main.py
import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 1. Tạo trang Web siêu nhẹ để giữ bot luôn sống trên Render
app = Flask('')

@app.route('/')
def home():
    return "Bot bypass link của Sếp đang hoạt động cực kỳ mượt mà nha! ✨🌸"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# 2. Cấu hình Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Hàm xử lý bypass cuty.io / cuttty.com
def bypass_short_link(url):
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
        
        session = requests.Session()
        # Gửi request lần đầu để lấy cookie và trang chuyển hướng
        response = session.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        # Nếu link tự động redirect thẳng tới đích thì trả về luôn
        if "cuty.io" not in response.url and "cuttty.com" not in response.url:
            return response.url
            
        # Nếu trang web dùng form JavaScript phức tạp hơn, ta phân tích HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}
        
        # Lấy các input ẩn (hidden inputs) mà trang web yêu cầu gửi đi
        for input_tag in soup.find_all('input'):
            if input_tag.get('name'):
                data[input_tag.get('name')] = input_tag.get('value', '')
                
        # Lấy action của form
        form = soup.find('form')
        if form and form.get('action'):
            post_url = form.get('action')
            if not post_url.startswith('http'):
                # Ghép domain nếu action là đường dẫn tương đối
                from urllib.parse import urlparse
                parsed_uri = urlparse(url)
                post_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}{post_url}"
                
            # Gửi POST request để lấy link cuối cùng
            post_response = session.post(post_url, data=data, headers=headers, allow_redirects=True, timeout=10)
            return post_response.url
            
        return response.url
    except Exception as e:
        print(f"Lỗi bypass: {e}")
        return None

@bot.event
async def on_ready():
    print(f"🌸 Bot {bot.user} đã sẵn sàng bypass link cho Sếp rồi nè!")

# Lệnh Discord: !bypass <link_rút_gọn>
@bot.command(name="bypass")
async def bypass_cmd(ctx, *, url: str):
    await ctx.send(f"⏳ Sếp chờ em xíu nha, em đang mổ xẻ link cuty/cuttty này... 🎀")
    
    # Gọi hàm xử lý bypass
    final_url = bypass_short_link(url)
    
    if final_url:
        await ctx.send(f"✨ Thành công rồi nè Sếp ơi!\nLink gốc của Sếp đây ạ: {final_url}")
    else:
        await ctx.send(f"❌ Hức hức... Link này khó quá hoặc bị lỗi mất rồi Sếp ơi, em không lấy được link gốc! 😢")

# 3. Khởi chạy bot
if __name__ == "__main__":
    keep_alive()  # Chạy web server ngầm
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Lỗi: Chưa tìm thấy DISCORD_TOKEN trong phần Cài đặt của Render!")