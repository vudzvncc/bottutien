# File: main.py
import os
import re
import aiohttp
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

async def bypass_cuty(url: str) -> str:
    url = url.strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://cuty.io/"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url, allow_redirects=True, timeout=10) as response:
                html_text = await response.text()
                
                # Bóc tách link từ thẻ HTML của cuty.io / cuttty.com
                match = re.search(r'href="(https?://[^"]+)" class="btn', html_text)
                if match:
                    return match.group(1)
                
                redirect_url = re.search(r'location\.href\s*=\s*["\']([^"\']+)["\']', html_text)
                if redirect_url:
                    return redirect_url.group(1)
                    
            # API dự phòng nếu trang yêu cầu captcha
            api_url = f"https://api.bypass.vip/bypass?url={url}"
            async with session.get(api_url, timeout=10) as api_resp:
                if api_resp.status == 200:
                    data = await api_resp.json()
                    if data.get("status") == "success" and data.get("destination"):
                        return data.get("destination")
                        
        except Exception as e:
            return f"Lỗi xử lý: {str(e)}"
            
    return "Không thể bypass được link này ạ 🥺"

@bot.event
async def on_ready():
    print(f"🌸 Bot {bot.user.name} đã sẵn sàng!")
    await bot.change_presence(activity=discord.Game(name="!bypass <link> 🎀"))

@bot.command(name="bypass")
async def bypass_command(ctx, url: str = None):
    if not url:
        await ctx.send("Sếp ơi, hãy nhập link cần bypass nha! Ví dụ: `!bypass https://cuty.io/xxx` 🌸")
        return

    msg = await ctx.send("⏳ Em đang giải mã link giúp Sếp, chờ em một xíu nha... ✨")
    result_url = await bypass_cuty(url)
    
    embed = discord.Embed(
        title="✨ KẾT QUẢ BYPASS LINK ✨",
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.add_field(name="🔗 Link gốc:", value=f"`{url}`", inline=False)
    embed.add_field(name="🎯 Link đích:", value=f"{result_url}", inline=False)
    
    await msg.edit(content="Xong rồi nè Sếp ơi! 🎉", embed=embed)

TOKEN = os.getenv("BOT_TOKEN", "DISCORD_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)