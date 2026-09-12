-- File: main.py
import os
import threading
import random
from flask import Flask
import discord
from discord.ext import commands

# 1. Khởi tạo Web Server giả lập để UptimeRobot giữ bot online 24/7
app = Flask(__name__)

@app.route('/')
def home():
    print("🌸 Bot Tu Tien VIP dang hoat dong on dinh! ✨")
    return "🌸 Bot Tu Tien VIP Discord Dang Hoat Dong! ✨"

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

# Database RAM tạm thời lưu trữ thông tin đạo hữu
# Cấu trúc: { user_id: {"name": str, "tu_vi": int, "can_cot": str, "linh_thach": int, "canh_gioi_idx": int} }
database_tu_tien = {}

DANH_SACH_CANH_GIOI = [
    "Luyện Khí Kỳ", "Trúc Cơ Kỳ", "Kết Đan Kỳ", 
    "Nguyên Anh Kỳ", "Hóa Thần Kỳ", "Luyện Hư Kỳ", 
    "Hợp Thể Kỳ", "Đại乘 (Đại Thừa) Kỳ", "Độ Kiếp Kỳ", "Phi Thăng Tiên Nhân"
]

@bot.event
async def on_ready():
    print(f"🌸 Bot Tu Tien VIP da online thanh cong voi ten: {bot.user} ✨")

@bot.command(name="nhapmon")
async def nhapmon(ctx):
    user_id = ctx.author.id
    if user_id in database_tu_tien:
        await ctx.send(f"🌸 Đạo hữu **{ctx.author.name}** đã nhập môn từ trước rồi! Gõ `!trangthai` để kiểm tra tu vi nhé! 🎀")
        return
    
    linh_can_list = ["Phàm Phẩm Linh Căn", "Hoàng Phẩm Linh Căn", "Địa Phẩm Linh Căn", "Thiên Phẩm Linh Căn", "Hỗn Độn Thể ✨"]
    can_cot_chon = random.choice(linh_can_list)
    
    database_tu_tien[user_id] = {
        "name": ctx.author.name,
        "tu_vi": 100,
        "can_cot": can_cot_chon,
        "linh_thach": 50,
        "canh_gioi_idx": 0
    }
    
    await ctx.send(f"🎉 Chúc mừng đạo hữu **{ctx.author.name}** đã bái nhập tông môn!\n⚡ Linh căn khai mở: **{can_cot_chon}**\n💰 Phần thưởng nhập môn: `50 Linh Thạch`.\n📖 Gõ `!bequan` để bắt đầu tu luyện ngay nào! 🌸")

@bot.command(name="trangthai")
async def trangthai(ctx):
    user_id = ctx.author.id
    if user_id not in database_tu_tien:
        await ctx.send(f"⚠️ Đạo hữu chưa có tên trong tông môn! Hãy gõ `!nhapmon` trước nha Sếp! 🌸")
        return
    
    info = database_tu_tien[user_id]
    canh_gioi_hien_tai = DANH_SACH_CANH_GIOI[info["canh_gioi_idx"]]
    
    embed = discord.Embed(title=f"📜 Đạo Hộ Sổ - Đạo Hữu: {info['name']}", color=0xFF69B4)
    embed.add_field(name="🌟 Linh Căn", value=info["can_cot"], inline=False)
    embed.add_field(name="⚡ Cảnh Giới", value=canh_gioi_hien_tai, inline=True)
    embed.add_field(name="🔮 Tổng Tu Vi", value=f"{info['tu_vi']} điểm", inline=True)
    embed.add_field(name="💰 Linh Thạch", value=f"{info['linh_thach']} viên", inline=True)
    embed.set_footer(text="🌸 Chúc Sếp sớm ngày đắc đạo phi thăng! ✨")
    
    await ctx.send(embed=embed)

@bot.command(name="bequan")
async def bequan(ctx):
    user_id = ctx.author.id
    if user_id not in database_tu_tien:
        await ctx.send(f"⚠️ Đạo hữu chưa nhập môn! Gõ `!nhapmon` đi nè Sếp! 🌸")
        return
    
    diem_tang = random.randint(80, 350)
    database_tu_tien[user_id]["tu_vi"] += diem_tang
    
    await ctx.send(f"🧘 **{info_name(user_id)}** bế quan hấp thu thiên địa linh khí thành công!\n📈 Tu vi tăng thêm: `+{diem_tang}` điểm. 🌸✨")

@bot.command(name="dotpha")
async def dotpha(ctx):
    user_id = ctx.author.id
    if user_id not in database_tu_tien:
        await ctx.send(f"⚠️ Đạo hữu chưa nhập môn! 🌸")
        return
    
    info = database_tu_tien[user_id]
    current_idx = info["canh_gioi_idx"]
    
    if current_idx >= len(DANH_SACH_CANH_GIOI) - 1:
        await ctx.send(f"👑 Đạo hữu đã đạt đến cảnh giới tối cao **Phi Thăng Tiên Nhân**, vô địch thiên hạ rồi! 🌸✨")
        return
    
    # Yêu cầu tu vi để đột phá mỗi cấp
    tu_vi_can = (current_idx + 1) * 1000
    if info["tu_vi"] < tu_vi_can:
        await ctx.send(f"❌ Tu vi chưa đủ để đột phá!\n⚡ Sếp cần ít nhất **{tu_vi_can}** điểm tu vi (Hiện tại: {info['tu_vi']}). Cố gắng `!bequan` thêm nha! 🌸")
        return
    
    # Tỷ lệ thành công đột phá (70%)
    if random.random() < 0.7:
        info["canh_gioi_idx"] += 1
        moi_canh_gioi = DANH_SACH_CANH_GIOI[info["canh_gioi_idx"]]
        await ctx.send(f"🎉 ⚡ **THÀNH CÔNG ĐỘT PHÁ!** ⚡\nĐạo hữu đã vượt qua thiên kiếp, bước chân vào cảnh giới: **{moi_canh_gioi}**! 🌸🎆")
    else:
        # Phạt nhẹ nếu thất bại
        mat_tu_vi = 150
        info["tu_vi"] = max(0, info["tu_vi"] - mat_tu_vi)
        await ctx.send(f"💥 **ĐỘT PHÁ THẤT BẠI!** Thiên lôi đánh cho tơi tả, tu vi bị hao hụt mất `{mat_tu_vi}` điểm. Đạo hữu hãy tĩnh tâm thử lại sau nhé! 🥺💔")

@bot.command(name="thamhiem")
async def thamhiem(ctx):
    user_id = ctx.author.id
    if user_id not in database_tu_tien:
        await ctx.send(f"⚠️ Đạo hữu chưa nhập môn! 🌸")
        return
    
    su_kien = [
        ("Khám phá Thượng古 Di Tích", 200, 50),
        ("Đánh bại Yêu Thú hoang dã", 150, 30),
        ("Hái được Linh Chi ngàn năm", 300, 100),
        ("Đi nhầm vào cấm địa, suýt mất mạng", -50, 0)
    ]
    
    ten_su_kien, thu_vi_thu, linh_thach_thu = random.choice(su_kien)
    database_tu_tien[user_id]["tu_vi"] += thu_vi_thu
    database_tu_tien[user_id]["linh_thach"] += linh_thach_thu
    
    await ctx.send(f"🗺️ **Kết quả thám hiểm:** {ten_su_kien}!\n📈 Nhận được: `+{thu_vi_thu} Tu Vi` và `+{linh_thach_thu} Linh Thạch` 🌸✨")

@bot.command(name="codep")
def info_name(user_id):
    return database_tu_tien[user_id]["name"]

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! Bot Tu Tiên VIP độ trễ: {round(bot.latency * 1000)}ms 🎀")

# 3. Chạy Server và Bot
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Loi: Chua tim thay bien DISCORD_TOKEN trong Environment!")