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
        # Chromium'u headless (arayüzsüz) başlat
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto("https://seedloaf.com/login")
        await page.fill("input[name='email']", os.environ['EMAIL'])
        await page.fill("input[name='password']", os.environ['SIFRE'])
        await page.click("button[type='submit']")
        
        # Sayfanın yüklenmesini bekle
        await page.wait_for_timeout(5000)
        await page.goto("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console")
        
        # O gördüğün "Start World" butonuna tıklat
        # Button text'ine göre bulur
        await page.get_by_role("button", name="Start World").click()
        
        await browser.close()

@bot.command()
async def ac(ctx):
    await ctx.send("İşlem başlatılıyor...")
    try:
        await start_server()
        await ctx.send("İşlem başarılı! Sunucu açılıyor.")
    except Exception as e:
        await ctx.send(f"Hata oluştu: {str(e)[:50]}")

bot.run(os.environ['DISCORD_TOKEN'])
