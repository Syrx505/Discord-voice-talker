import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktivdir!"

def run_web_server(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

class RenderBot(commands.Bot):
    def __init__(self, token):
        super().__init__(command_prefix="!", self_bot=True)
        self.token = token

    async def on_ready(self):
        print(f"Logged in: {self.user}")
        channel = self.get_channel(int(os.environ.get("CHANNEL_ID")))
        if channel:
            try:
                vc = await channel.connect()
                print(f"Kanalda çalınır: {channel.name}")
                self.play_audio(vc)
            except Exception as e:
                print(f"Bağlantı xətası: {e}")

    def play_audio(self, vc):
        # Faylın tam yolu və düzgün ffmpeg parametrləri
        audio_source = discord.FFmpegPCMAudio(
            "ses.mp3", 
            executable="ffmpeg",
            options="-re -stream_loop -1" # -re: real-time, -stream_loop: sonsuz döngü
        )
        vc.play(audio_source, after=lambda e: print(f"Səs dayandı: {e}") if e else None)

async def main():
    Thread(target=run_web_server).start()
    tokens = os.environ.get("TOKENS").split(",")
    # Tokenları ardıcıl başlatmaq bağlantı xətalarını azaldır
    for t in tokens:
        bot = RenderBot(t)
        asyncio.create_task(bot.start(t))
        await asyncio.sleep(2) # Hər bot arasına gecikmə qoy
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
