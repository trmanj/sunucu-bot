async def start_server():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page()
        
        # 1. Sayfaya git ve YÜKLENMESİNİ BEKLE (networkidle: tüm işlemler bitene kadar bekle)
        await page.goto("https://seedloaf.com", wait_until="networkidle")
        
        # 2. Butona tıklamadan önce var mı diye kontrol et
        await page.wait_for_selector("a.btn-primary.btn-lg", timeout=60000)
        await page.click("a.btn-primary.btn-lg")
        
        # 3. Yönlendirmeyi bekle
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("a.cl-footerActionLink", timeout=60000)
        await page.click("a.cl-footerActionLink")
        
        # 4. Giriş alanını bekle
        await page.wait_for_selector("input[name='identifier']", timeout=60000)
        await page.fill("input[name='identifier']", os.environ['EMAIL'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        
        # 5. Şifre alanı gelene kadar bekle
        await page.wait_for_selector("input[name='password']", timeout=60000)
        await page.fill("input[name='password']", os.environ['SIFRE'])
        await page.click("button[data-localization-key='formButtonPrimary']")
        
        # 6. Dashboard'a git
        await page.wait_for_load_state("networkidle")
        await page.goto("https://seedloaf.com/dashboard/e1410ed9-466f-4a54-a29c-228284783d32/console", wait_until="networkidle")
        
        # 7. Son olarak Start butonunu bekle ve tıkla
        await page.wait_for_selector("button.btn-primary", timeout=60000)
        await page.get_by_role("button", name="Start World").click()
        
        await browser.close()
