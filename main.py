import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
import requests

from playwright.async_api import async_playwright

BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
COOKIE_FILE = BASE_DIR / "cookies.json"
HISTORY_FILE = BASE_DIR / "order_history.json"

def check_and_create_config():
    """检查配置文件，不存在则自动创建"""
    if CONFIG_FILE.exists():
        return True
    
    print("=" * 50)
    print("⚠️ 未找到配置文件 config.json")
    print("=" * 50)
    
    default_config = {
        "monitor": {"interval": 60},
        "push": {
            "bark_key": "",
            "bark_server": "https://api.day.app"
        }
    }
    
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ 已创建配置文件: {CONFIG_FILE}")
        print("\n请编辑配置文件填写 Bark 推送密钥：")
        print(f"   notepad {CONFIG_FILE}")
        print("\n如果不需要推送，留空即可继续运行")
        print("=" * 50)
        
        input("\n按回车键继续...")
        return True
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False

def check_and_create_history():
    """检查历史记录文件，不存在则创建"""
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        print(f"✅ 已创建历史记录文件: {HISTORY_FILE}")

class Monitor:
    def __init__(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            sys.exit(1)
        
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except Exception:
            self.history = {}
        
        bark_key = self.config.get("push", {}).get("bark_key", "")
        if bark_key:
            print(f"📱 已启用 Bark 推送")
        else:
            print(f"⚠️ 未配置 Bark 推送，将不会收到通知")
        
    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        
    def push(self, title, body, url=None):
        cfg = self.config.get("push", {})
        bark_key = cfg.get("bark_key", "").strip()
        
        if bark_key:
            try:
                server = cfg.get("bark_server", "https://api.day.app")
                push_url = f"{server}/{bark_key}/{requests.utils.quote(title)}/{requests.utils.quote(body)}"
                if url:
                    push_url += f"?url={requests.utils.quote(url)}"
                requests.get(push_url, timeout=10)
                self.log("✅ 推送成功")
                return True
            except Exception as e:
                self.log(f"❌ 推送失败: {e}")
        return False
        
    async def check(self):
        if not COOKIE_FILE.exists():
            self.log("❌ 未登录，请先运行 BiliLogin.exe 进行登录")
            return False
            
        try:
            with open(COOKIE_FILE, "r", encoding="utf-8") as f:
                cookies = json.load(f)
        except Exception as e:
            self.log(f"❌ 读取 cookies 失败: {e}")
            return False
            
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            await context.add_cookies(cookies)
            page = await context.new_page()
            
            try:
                await page.goto("https://mall.bilibili.com/mall-c/order/list.html?tab=1", 
                              wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)
                
                orders = await page.evaluate("""
                    () => {
                        const orders = [];
                        const orderItems = document.querySelectorAll('.order-item, [data-order-id], .order-card');
                        orderItems.forEach(el => {
                            const statusText = el.innerText || '';
                            if (statusText.includes('待付款') || statusText.includes('待支付')) {
                                let orderId = el.getAttribute('data-order-id');
                                if (!orderId) {
                                    const idMatch = statusText.match(/订单号[：:]\\s*(\\d+)/);
                                    if (idMatch) orderId = idMatch[1];
                                }
                                if (orderId) {
                                    orders.push({
                                        id: orderId,
                                        name: el.querySelector('.goods-name, .item-name, .product-name')?.innerText?.trim() || '未知商品',
                                        price: el.querySelector('.price, .total-price, .amount')?.innerText?.trim() || '未知'
                                    });
                                }
                            }
                        });
                        return orders;
                    }
                """)
                
                await browser.close()
                
                if not orders:
                    self.log("ℹ️ 暂无待支付订单")
                    return True
                    
                self.log(f"🔍 发现 {len(orders)} 个待支付订单")
                
                new_count = 0
                for order in orders:
                    oid = str(order["id"])
                    if oid not in self.history:
                        title = "🔔 B站会员购待支付"
                        body = f"商品: {order['name']}\\n金额: {order['price']}\\n\\n请及时付款！"
                        pay_url = f"https://mall.bilibili.com/mall-c/order/detail.html?orderId={oid}"
                        
                        if self.push(title, body, pay_url):
                            self.history[oid] = datetime.now().isoformat()
                            new_count += 1
                            self.log(f"✅ 已提醒: {oid[:8]}...")
                
                if new_count > 0:
                    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                        json.dump(self.history, f, ensure_ascii=False, indent=2)
                    self.log(f"💾 已保存 {new_count} 条新订单记录")
                        
                return True
                
            except Exception as e:
                self.log(f"❌ 检查失败: {e}")
                await browser.close()
                return False
    
    async def run(self):
        interval = self.config.get("monitor", {}).get("interval", 60)
        self.log(f"🚀 监控已启动，检查间隔: {interval} 秒")
        
        while True:
            try:
                await self.check()
            except Exception as e:
                self.log(f"❌ 运行异常: {e}")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    print("=" * 50)
    print("   B站会员购订单监控")
    print("=" * 50)
    
    if not check_and_create_config():
        print("❌ 配置文件初始化失败")
        sys.exit(1)
    
    check_and_create_history()
    
    try:
        asyncio.run(Monitor().run())
    except KeyboardInterrupt:
        print("\n👋 已停止监控")
