import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

# Flask (Web Server - Render'ın botu uyutmaması için)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot ve Render hizmeti aktif!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# Render için FFmpeg yolu
FFMPEG_PATH = "ffmpeg" 
CHANNEL_ID = int(os.environ.get("CHANNEL_ID")) # Render Environment Variable'dan al

class RenderBot(commands.Bot):
    def __init__(self, token):
        super().__init__(command_prefix="!", self_bot=True)
        self.token = token

    async def on_ready(self):
        print(f"Giriş yapıldı: {self.user}")
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            try:
                vc = await channel.connect()
                self.play_loop(vc)
            except Exception as e:
                print(f"Hata: {e}")

    def play_loop(self, vc):
        if not vc.is_playing():
            # Döngüsel ses oynatma
            audio = discord.FFmpegPCMAudio("ses.mp3", executable=FFMPEG_PATH)
            vc.play(audio, after=lambda e: self.play_loop(vc))

async def main():
    # Web sunucusunu arka planda başlat
    Thread(target=run_web_server).start()
    
    # Tokenları Environment Variable'dan (virgülle ayırarak) al
    tokens = os.environ.get("TOKENS").split(",")
    bots = [RenderBot(t) for t in tokens]
    
    # Tüm botları başlat
    await asyncio.gather(*(b.start(b.token) for b in bots))

if __name__ == "__main__":
    asyncio.run(main())
  
