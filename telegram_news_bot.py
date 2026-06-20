import asyncio
from pyrogram import Client, filters

API_ID = 25212165
API_HASH = "9ae84dd5ba1a96779b982d354b7d4ded"

MANBA_KANALLAR = ["@uzbekistan_news", "@kunuz"]
SIZNING_KANALINGIZ = "@bakhronov24"
SILKA_MATNI = "@👉 Telegram | Instagram | You"

app = Client("yangilik_bot", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.channel & filters.chat(MANBA_KANALLAR))
async def yangilik_yuborish(client, message):
    try:
        import re
        matn = message.text or message.caption or ""
        matn = re.sub(r'@\w+', '', matn).strip()
        if matn:
            matn += f"\n\n{SILKA_MATNI}"
        if message.photo:
            foto = await client.download_media(message.photo, in_memory=True)
            await client.send_photo(SIZNING_KANALINGIZ, foto, caption=matn or SILKA_MATNI)
        elif message.video:
            video = await client.download_media(message.video, in_memory=True)
            await client.send_video(SIZNING_KANALINGIZ, video, caption=matn or SILKA_MATNI)
        elif matn:
            await client.send_message(SIZNING_KANALINGIZ, matn)
    except Exception as e:
        print(f"Xato: {e}")

app.run()
