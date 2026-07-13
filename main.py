import discord
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

@bot.command()
async def ac(ctx):
    await ctx.send("Giriş yapılıyor ve sunucu başlatılıyor, lütfen bekle...")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    
    try:
        # 1. Giriş sayfasına git
        driver.get("https://seedloaf.com/login")
        
        # Giriş bilgilerini doldur
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(os.environ['EMAIL'])
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(os.environ['SIFRE'])
        
        # Giriş yap butonuna tıkla
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # 2. Konsol sayfasına git
        time.sleep(5) 
        driver.get("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console")
        
        # 3. Butonu bul ve tıkla
        # "Start World" butonunu daha kararlı bir XPath ile buluyoruz
        start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start World')]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_btn)
        time.sleep(1)
        start_btn.click()
        
        await ctx.send("İşlem tamam! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"Hata oluştu: {e}")
    finally:
        driver.quit()

bot.run(os.environ['DISCORD_TOKEN'])
