import discord
from discord.ext import commands
import os
import asyncio
from playwright.async_api import async_playwright

# Discord Bot Kurulumu
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Seninle hazırladığımız web sitesini otomatize eden fonksiyon
async def start_server():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        
        await page.goto("https://seedloaf.com")
        await page.click("a.btn-primary.btn-lg")
        await page.wait_for_timeout(3000)
        await page.click("a.cl-footerActionLink")
        await page.wait_for_timeout(3000)
        
        await page.fill("input[name='identifier']", os.environ['EMAIL'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        await page.wait_for_timeout(3000)
        await page.fill("input[name='password']", os.environ['SIFRE'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        await page.wait_for_timeout(6000)
        
        await page.goto("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console")
        await page.wait_for_timeout(4000)
        await page.get_by_role("button", name="Start World").click()
        
        await browser.close()

# Discord komutu: !ac yazınca bot çalışır
@bot.command()
async def ac(ctx):
    await ctx.send("İstek alındı, giriş yapılıyor...")
    try:
        await start_server()
        await ctx.send("Sunucu açma işlemi başarıyla tamamlandı!")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {str(e)}")

# Botu başlat
bot.run(os.environ['DISCORD_TOKEN'])
