# 🔔 B站会员购订单监控

**自动监控B站会员购待支付订单，手机实时推送提醒，避免手办/周边流拍！**

[![Build](https://github.com/whiterole2006/bili-order-monitor/actions/workflows/build.yml/badge.svg)](https://github.com/whiterole2006/bili-order-monitor/actions)
[![Release](https://img.shields.io/github/v/release/whiterole2006/bili-order-monitor)](https://github.com/whiterole2006/bili-order-monitor/releases)

---

## 📋 目录
- [💻 系统要求](#-系统要求)
- [📥 下载安装](#-下载安装)
- [🚀 使用教程](#-使用教程)
- [📱 推送方式配置](#-推送方式配置)
- [❓ 常见问题](#-常见问题)

---

## 💻 系统要求

| 系统 | 要求 |
|:---|:---|
| Windows | Windows 10/11，64位 |
| macOS/Linux | 支持（需源码运行）|
| 网络 | 能访问GitHub和B站 |
| 浏览器 | Windows自带Edge（扫码登录用）|

---

## 📥 下载安装

### 方式一：Windows免安装版（推荐）

1. 访问 [Releases页面](https://github.com/whiterole2006/bili-order-monitor/releases) 下载 `BiliOrderMonitor_Windows.zip`
2. 解压到任意文件夹
3. 你会得到3个文件：
   - `BiliMonitor.exe` - 配置界面（首次使用）
   - `BiliLogin.exe` - 扫码登录（调用Edge浏览器）
   - `BiliStart.exe` - 后台监控（日常使用）

### 方式二：源码运行（全平台）

```bash
# 克隆仓库
git clone https://github.com/whiterole2006/bili-order-monitor.git
cd bili-order-monitor

# 安装依赖
pip install -r requirements.txt

# 安装浏览器（二选一）
playwright install chromium    # 使用Playwright自带浏览器
# 或确保系统已安装Chrome/Edge，修改代码使用系统浏览器

# 运行配置界面
python setup.py

# 或后台运行监控（无黑窗口）
pythonw main.py

```
## 🚀 使用教程

### 准备工作（手机下载Bark App）
- **安卓**：GitHub搜索 "Bark-Android" 下载，或应用商店搜索
- **iOS**：App Store搜索 "Bark" 下载安装
- 打开App，复制显示的Key（如：`aBcDeFgHiJkLmNoP`）

### 第一步：配置推送
1. 双击 `BiliMonitor.exe`
2. 在"Bark Key"输入框粘贴你的Key
3. 点击 **"💾 保存配置"**
4. 看到"配置保存成功"提示即可

### 第二步：扫码登录
1. 点击 **"🔑 扫码登录"**
2. 自动弹出浏览器显示B站二维码
3. **打开手机B站App** → 右上角扫一扫 → 扫描电脑屏幕二维码
4. **手机上确认登录**
5. 电脑显示"登录成功"即可

### 第三步：启动监控
1. 点击 **"▶️ 启动监控"**
2. 提示"监控已启动" → 完成！

**现在程序在后台运行：**
- 每60秒自动检查待支付订单
- 发现新订单立即推送到手机
- 可以关闭配置窗口，监控继续运行

**日常使用：** 以后每次开机只需双击 `BiliStart.exe`

---

## 📱 推送方式配置

### Bark（推荐）
- 免费、实时、支持安卓/iOS
- 配置：粘贴Bark App里的Key即可

### Server酱（适合微信）
- 访问 https://sct.ftqq.com 用GitHub登录
- 复制SendKey粘贴到配置界面的"Server酱 Key"栏

---

## ❓ 常见问题

**Q: 双击没反应？**
- 关闭杀毒软件或添加信任
- 安装 [VC++运行库](https://aka.ms/vs/17/release/vc_redist.x64.exe)

**Q: 浏览器没弹出？**
- 确认文件夹里有 `BiliLogin.exe`
- 源码运行需执行：`playwright install chromium`

**Q: 扫码后提示超时？**
- 手机扫码后一定要点"确认登录"
- 检查电脑能否正常访问B站

**Q: 手机收不到推送？**
- 检查Key是否填对（对比Bark App里显示的）
- 检查手机和电脑网络
- 检查Bark App是否允许通知

**Q: 提示"Cookie过期"？**
- 正常！Cookie有效期1-2个月
- 重新点击"扫码登录"扫码即可

**Q: 如何关闭监控？**
- 任务管理器 → 找到 `BiliStart.exe` 或 `python` → 结束任务

- **Q: 提示"无法启动Chrome/Edge"？**
- 确保Windows 10/11已安装Edge浏览器（系统自带）
- 如卸载了Edge，需重新安装或改用源码方式

---

## ⚠️ 重要提醒

- **3个exe文件必须在同一文件夹**，不能分开移动
- `cookies.json` 文件包含登录凭证，**不要分享给他人**
- Cookie约1-2个月过期，过期后重新扫码即可
- 监控启动后会一直在后台运行，重启电脑后需重新启动
- 可将`BiliStart.exe`放入Windows"启动"文件夹实现开机自启

---

## 📝 反馈

遇到问题？在 [Issues](https://github.com/whiterole2006/bili-order-monitor/issues) 提交，描述清楚系统版本、操作步骤、错误截图。

觉得好用？给个 ⭐ Star 支持一下！
