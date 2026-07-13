import discord
from discord.ext import commands
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # Render'da yüklediğimiz Chromium'un yolu
    options.binary_location = "/usr/bin/chromium" 
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

@bot.command()
async def ac(ctx):
    await ctx.send("İşlem başlatıldı, tarayıcı hazırlanıyor...")
    try:
        driver = get_driver()
        wait = WebDriverWait(driver, 30)
        
        driver.get("https://seedloaf.com/")
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Play now')]").click()
            time.sleep(3)
        except: pass
        
        driver.get("https://seedloaf.com/login")
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(os.environ['EMAIL'])
        driver.find_element(By.NAME, "password").send_keys(os.environ['SIFRE'])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(5)
        driver.get("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console")
        
        start_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start World')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", start_btn)
        start_btn.click()
        
        await ctx.send("İşlem tamam! Sunucu açılıyor.")
        driver.quit()
    except Exception as e:
        await ctx.send(f"Hata: {str(e)[:100]}")

bot.run(os.environ['DISCORD_TOKEN'])
