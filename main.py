import discord
from discord.ext import commands
import os
import asyncio
from playwright.async_api import async_playwright

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def start_server():
    async with async_playwright() as p:
        # Render için en kritik ayarlar:
        # 1. args=["--no-sandbox"] -> Tarayıcıyı kısıtlamadan başlatır.
        # 2. headless=True -> Görünmez modda çalıştırır.
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = await browser.new_page()
        
        # Giriş işlemleri
        await page.goto("https://seedloaf.com/login")
        await page.fill("input[name='email']", os.environ['EMAIL'])
        await page.fill("input[name='password']", os.environ['SIFRE'])
        await page.click("button[type='submit']")
        
        # Girişin tamamlanması için bekleme
        await page.wait_for_timeout(6000)
        
        # Dashboard'a git
        await page.goto("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console")
        
        # Butonu tıkla
        await page.get_by_role("button", name="Start World").click()
        await page.wait_for_timeout(2000)
        
        await browser.close()

@bot.command()
async def ac(ctx):
    await ctx.send("İstek gönderildi, sunucu açılıyor...")
    try:
        await start_server()
        await ctx.send("İşlem tamamlandı!")
    except Exception as e:
        await ctx.send(f"Hata: {str(e)[:50]}")

bot.run(os.environ['DISCORD_TOKEN'])
