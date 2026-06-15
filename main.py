import discord
from discord.ext import commands
import asyncio
import os
import random
from flask import Flask
from threading import Thread

# Flask serveri (Render üçün vacibdir)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktivdir!"
def run_web_server(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

class RenderBot(commands.Bot):
    def __init__(self, token):
        # Intents silindi, self_bot=True kifayətdir
        super().__init__(command_prefix="!", self_bot=True)
        self.token = token

    async def on_ready(self):
        print(f"Logged in as: {self.user}")
        # İnsan davranışı üçün təsadüfi gecikmə
        delay = random.randint(5, 15)
        await asyncio.sleep(delay)
        
        channel = self.get_channel(int(os.environ.get("CHANNEL_ID")))
        if channel:
            try:
                vc = await channel.connect()
                print(f"Qoşuldu: {channel.name}")
                self.play_audio(vc)
            except Exception as e:
                print(f"Bağlantı xətası: {e}")

    def play_audio(self, vc):
        # Faylı birbaşa səs axını kimi oxuyur
        audio = discord.FFmpegPCMAudio(
            "ses.mp3", 
            executable="ffmpeg",
            options="-re -stream_loop -1 -vn"
        )
        vc.play(audio)

async def main():
    # Web serveri başlat
    Thread(target=run_web_server, daemon=True).start()
    
    tokens = os.environ.get("TOKENS").split(",")
    for t in tokens:
        bot = RenderBot(t)
        asyncio.create_task(bot.start(t))
        await asyncio.sleep(20) # Hər botun girməsi üçün ara qoy

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
