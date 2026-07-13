import discord
from discord.ext import commands
import os
import requests

# Bot kurulumu
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ac(ctx):
    await ctx.send("İşlem başlatılıyor...")
    
    # Giriş URL ve verileri
    login_url = "https://seedloaf.com/login"
    payload = {
        'email': os.environ['EMAIL'],
        'password': os.environ['SIFRE']
    }
    
    # Sunucuyu açacak URL (Console dashboard linkin)
    # Eğer bu link çalışmazsa, tarayıcıda butona basınca gelen network isteğini bulmamız gerekir
    start_url = "https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/start"
    
    try:
        # Session ile giriş yap ve sunucuyu aç
        with requests.Session() as s:
            s.post(login_url, data=payload)
            response = s.post(start_url)
            
            if response.status_code == 200:
                await ctx.send("İşlem başarılı! Sunucu açılıyor.")
            else:
                await ctx.send(f"Sunucu isteğe yanıt verdi ancak hata kodu: {response.status_code}")
                
    except Exception as e:
        await ctx.send(f"Hata: {str(e)[:50]}")

bot.run(os.environ['DISCORD_TOKEN'])
