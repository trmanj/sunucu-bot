import discord
from discord.ext import commands
import os
import asyncio
from playwright.async_api import async_playwright
from flask import Flask
from threading import Thread

# 1. Render'ın kapatmaması için Web Sunucusu
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif!"
def run_web():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
Thread(target=run_web).start()

# 2. Discord Botu
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def start_server():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        
        # Siteye git ve tam yüklenmesini bekle
        await page.goto("https://seedloaf.com", wait_until="networkidle")
        await page.wait_for_selector("a.btn-primary.btn-lg", timeout=60000)
        await page.click("a.btn-primary.btn-lg")
        
        # Giriş sayfasına geç
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("a.cl-footerActionLink", timeout=60000)
        await page.click("a.cl-footerActionLink")
        
        # E-posta gir
        await page.wait_for_selector("input[name='identifier']", timeout=60000)
        await page.fill("input[name='identifier']", os.environ['EMAIL'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        
        # Şifre gir
        await page.wait_for_selector("input[name='password']", timeout=60000)
        await page.fill("input[name='password']", os.environ['SIFRE'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        
        # Konsola git ve başlat
        await page.wait_for_load_state("networkidle")
        await page.goto("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console", wait_until="networkidle")
        await page.wait_for_selector("button.btn-primary", timeout=60000)
        await page.get_by_role("button", name="Start World").click()
        
        await browser.close()

@bot.command()
async def ac(ctx):
    await ctx.send("İşlem başlıyor...")
    try:
        await start_server()
        await ctx.send("Sunucu açıldı!")
    except Exception as e:
        await ctx.send(f"Hata: {str(e)}")

bot.run(os.environ['DISCORD_TOKEN'])
