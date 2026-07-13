import discord
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.command()
async def ac(ctx):
    await ctx.send("Sunucu başlatılıyor, lütfen bekle...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Chrome tarayıcısını arka planda aç
    driver = webdriver.Chrome(options=options)
    
    try:
        # BURAYI KENDİ PANEL LİNKİN İLE DEĞİŞTİR
        driver.get("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console") 
        
        time.sleep(5) # Sayfanın yüklenmesi için 5 saniye bekle
        
        # "Start World" butonunu bul ve tıkla
        start_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Start World')]")
        start_btn.click()
        
        await ctx.send("İşlem tamam! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"Hata oluştu: {e}")
    finally:
        driver.quit()


