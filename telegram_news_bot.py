from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
import io
import re
import os

API_ID = 25212165
API_HASH = "9ae84dd5ba1a96779b982d354b7d4ded"

MANBA_KANALLAR = [
    "@uzbekistan_news","@kunuz"
]

SIZNING_KANALINGIZ = "@bakhronov24"
SILKA_MATNI = "@👉 Telegram | Instagram | You tube"
LOGO_FAYL = "logo.png"
BURCHAK_KENGLIK = 200
BURCHAK_BALANDLIK = 60

def burchakni_tozala(rasm):
    w, h = rasm.size
    draw = ImageDraw.Draw(rasm)
    burchaklar = [
        (0, 0, BURCHAK_KENGLIK, BURCHAK_BALANDLIK),
        (w-BURCHAK_KENGLIK, 0, w, BURCHAK_BALANDLIK),
        (0, h-BURCHAK_BALANDLIK, BURCHAK_KENGLIK, h),
        (w-BURCHAK_KENGLIK, h-BURCHAK_BALANDLIK, w, h),
    ]
    for (x1,y1,x2,y2) in burchaklar:
        try:
            rang = rasm.getpixel((min(x2+5,w-1), min(y2+5,h-1)))
            if len(rang)==4: rang=rang[:3]
        except:
            rang=(30,30,30)
        draw.rectangle([x1,y1,x2,y2], fill=rang)
    return rasm

def silka_qoy(rasm):
    w, h = rasm.size
    draw = ImageDraw.Draw(rasm)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), SILKA_MATNI, font=font)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    x = w-tw-12
    y = h-th-12
    draw.text((x+2,y+2), SILKA_MATNI, font=font, fill=(0,0,0,180))
    draw.text((x,y), SILKA_MATNI, font=font, fill=(255,255,255,255))
    return rasm

def rasmga_ishlov(photo_bytes):
    rasm = Image.open(photo_bytes).convert("RGBA")
    rasm = burchakni_tozala(rasm)
    rasm = silka_qoy(rasm)
    chiqish = io.BytesIO()
    rasm.convert("RGB").save(chiqish, format="JPEG", quality=95)
    chiqish.seek(0)
    return chiqish

def matnni_tozala(matn):
    if not matn: return ""
    matn = re.sub(r'@\w+', '', matn)
    matn = re.sub(r'https?://t\.me/\S+', '', matn)
    matn = re.sub(r'\n{3,}', '\n\n', matn)
    return matn.strip()

app = Client("yangilik_bot", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.channel & filters.chat(MANBA_KANALLAR))
async def yangilik_yuborish(client, message):
    try:
        izoh = matnni_tozala(message.caption or "")
        matn = matnni_tozala(message.text or "")
        if izoh: izoh += f"\n\n{SILKA_MATNI}"
        if matn: matn += f"\n\n{SILKA_MATNI}"
        if message.photo:
            foto = await client.download_media(message.photo, in_memory=True)
            rasm = rasmga_ishlov(foto)
            await client.send_photo(SIZNING_KANALINGIZ, rasm, caption=izoh or SILKA_MATNI)
        elif message.video:
            video = await client.download_media(message.video, in_memory=True)
            await client.send_video(SIZNING_KANALINGIZ, video, caption=izoh or SILKA_MATNI)
        elif matn:
            await client.send_message(SIZNING_KANALINGIZ, matn)
    except Exception as e:
        print(f"Xato: {e}")

if __name__ == "__main__":
    app.run()
