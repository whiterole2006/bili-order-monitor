import json
import subprocess
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext

# 路径处理
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

CONFIG_PATH = BASE_DIR / "config.json"
COOKIE_PATH = BASE_DIR / "cookies.json"

def load_cfg():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "bilibili": {"login_method": "qr", "username": "", "password": ""},
        "push": {"bark_key": "", "bark_server": "https://api.day.app", "server_chan_key": "", "pushplus_token": ""},
        "monitor": {"interval": 60, "remind_before_expire": 2}
    }

def save_cfg(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("B站会员购监控 v1.0")
        self.root.geometry("500x450")
        
        # 居中
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 450) // 2
        self.root.geometry(f"+{x}+{y}")
        
        self.cfg = load_cfg()
        self.build_ui()
        
    def build_ui(self):
        tk.Label(self.root, text="🔔 B站会员购订单监控", 
                font=("Microsoft YaHei", 20, "bold"), fg="#ff6b6b").pack(pady=20)
        
        # Bark Key输入
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="Bark Key:", font=("Microsoft YaHei", 12)).pack(side=tk.LEFT)
        self.entry_bark = tk.Entry(frame, width=35, font=("Microsoft YaHei", 11))
        self.entry_bark.pack(side=tk.LEFT, padx=10)
        self.entry_bark.insert(0, self.cfg["push"].get("bark_key", ""))
        
        tk.Label(self.root, text="💡 提示: 安卓下载Bark App获取Key", 
                font=("Microsoft YaHei", 9), fg="gray").pack()
        
        # 按钮区域
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="💾 保存配置", bg="#4caf50", fg="white",
                 font=("Microsoft YaHei", 12), width=12,
                 command=self.on_save).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🔑 扫码登录", bg="#2196f3", fg="white",
                 font=("Microsoft YaHei", 12), width=12,
                 command=self.on_login).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="▶️ 启动监控", bg="#ff9800", fg="white",
                 font=("Microsoft YaHei", 12), width=12,
                 command=self.on_start).pack(side=tk.LEFT, padx=10)
        
        # 日志区域
        self.log = scrolledtext.ScrolledText(self.root, height=10, font=("Consolas", 10))
        self.log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.log_msg("程序已启动，请先保存配置，然后扫码登录")
    
    def log_msg(self, msg):
        import datetime
        t = datetime.datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{t}] {msg}\n")
        self.log.see(tk.END)
        self.root.update()
        
    def on_save(self):
        self.cfg["push"]["bark_key"] = self.entry_bark.get().strip()
        save_cfg(self.cfg)
        self.log_msg("✅ 配置已保存")
        messagebox.showinfo("成功", "配置保存成功！")
    
    def on_login(self):
        self.log_msg("🔄 正在启动扫码登录...")
        
        # 获取BiliLogin.exe路径（同一目录）
        login_exe = BASE_DIR / "BiliLogin.exe"
        
        if not login_exe.exists():
            self.log_msg(f"❌ 找不到: {login_exe}")
            messagebox.showerror("错误", f"找不到登录程序: {login_exe}\n请确保BiliLogin.exe在同一文件夹")
            return
        
        try:
            subprocess.Popen(
                [str(login_exe)], 
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=str(BASE_DIR)
            )
            self.log_msg(f"✅ 已启动: {login_exe}")
            self.log_msg("请在弹出的窗口中扫码登录")
            
            # 后台检测登录成功
            def check_login():
                for i in range(180):
                    time.sleep(1)
                    if COOKIE_PATH.exists():
                        self.root.after(0, lambda: self.log_msg("🎉 检测到登录成功！"))
                        return
                self.root.after(0, lambda: self.log_msg("⏱️ 登录检测超时"))
            
            threading.Thread(target=check_login, daemon=True).start()
            
        except Exception as e:
            self.log_msg(f"❌ 启动失败: {e}")
            messagebox.showerror("错误", f"启动登录程序失败: {e}")
    
    def on_start(self):
        if not COOKIE_PATH.exists():
            messagebox.showwarning("提示", "请先扫码登录！")
            self.log_msg("⚠️ 未检测到登录，请先点击'扫码登录'")
            return
        
        start_exe = BASE_DIR / "BiliStart.exe"
        
        if not start_exe.exists():
            self.log_msg(f"❌ 找不到: {start_exe}")
            messagebox.showerror("错误", f"找不到监控程序: {start_exe}")
            return
        
        try:
            subprocess.Popen([str(start_exe)], cwd=str(BASE_DIR))
            self.log_msg("✅ 监控已启动（后台运行）")
            messagebox.showinfo("成功", "监控已启动！可以关闭本窗口")
        except Exception as e:
            self.log_msg(f"❌ 启动失败: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
