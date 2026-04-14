import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
COOKIE_FILE = BASE_DIR / "cookies.json"

async def main():
    print("=" * 50)
    print("B站登录 - 请扫码")
    print("=" * 50)
    
    async with async_playwright() as p:
        # 使用系统Edge（Windows自带）
        edge_paths = [
            "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
            "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
        ]
        
        browser = None
        for path in edge_paths:
            if Path(path).exists():
                try:
                    browser = await p.chromium.launch(
                        headless=False,
                        executable_path=path
                    )
                    print("✅ 使用系统Edge浏览器")
                    break
                except:
                    continue
        
        if not browser:
            print("❌ 未找到Edge浏览器")
            print("Windows 10/11自带Edge，请检查系统")
            input("按回车退出...")
            return
        
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            await page.goto("https://passport.bilibili.com/login")
            print("📱 请在弹出的浏览器窗口中扫码")
            print("⏳ 等待登录...")
            
            await page.wait_for_url(lambda url: "passport" not in url, timeout=120000)
            
            cookies = await context.cookies()
            with open(COOKIE_FILE, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            print("✅ 登录成功！")
            
        except Exception as e:
            print(f"❌ {e}")
        finally:
            input("按回车退出...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
