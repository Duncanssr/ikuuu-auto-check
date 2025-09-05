import requests
import time
import os
import json

# 配置
BASE_URL = "https://ikuuu.org"
LOGIN_URL = f"{BASE_URL}/auth/login"
CHECKIN_URL = f"{BASE_URL}/user/checkin"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": f"{BASE_URL}/auth/login",
    "X-Requested-With": "XMLHttpRequest",
}

# 从环境变量获取配置
ACCOUNTS_STR = os.getenv("ACCOUNTS", "")
TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID"， "")

# 解析账号
def parse_accounts():
    accounts = []
    if not ACCOUNTS_STR:
        print("未配置任何账号")
        return accounts
        
    for item 在 ACCOUNTS_STR.split(';'):
        if item 和 ',' 在 item:
            email, password = item.split(','， 1)
            accounts.append((email.strip(), password.strip()))
    return accounts

# 密码遮罩处理
def mask_password(password):
    if len(password) <= 4:
        return "*" * len(password)
    return f"{password[:2]}{'*'*(len(password)-4)}{password[-2:]}"

# 发送Telegram通知
def send_telegram_message(content):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("未配置Telegram，跳过通知")
        return
        
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TG_CHAT_ID,
        "text": content,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Telegram通知失败: {response.text}")
    except Exception as e:
        print(f"发送通知出错: {str(e)}")

# 登录并签到
def login_and_checkin(email, password):
    session = requests.Session()
    session.headers.update(HEADERS)
    
    # 登录
    try:
        login_data = {"email": email, "passwd": password, "code": ""}
        login_res = session.post(LOGIN_URL, data=login_data)
        login_res.raise_for_status()
        login_result = login_res.json()
        
        if login_result.get("ret") != 1:
            return False, f"登录失败: {login_result.get('msg', '未知错误')}"
    except Exception as e:
        return False, f"登录异常: {str(e)}"
    
    # 签到
    try:
        checkin_res = session.post(CHECKIN_URL)
        checkin_res.raise_for_status()
        checkin_result = checkin_res.json()
        
        if checkin_result.get("ret") == 1:
            return True, checkin_result.get("msg", "签到成功")
        else:
            return False, checkin_result.get("msg", "签到失败")
    except Exception as e:
        return False, f"签到异常: {str(e)}"

# 主函数
def main():
    accounts = parse_accounts()
    if not accounts:
        return
        
    # 准备通知内容
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    notification = [
        f"📅 执行时间: {current_time}",
        f"🌐 地址: {BASE_URL}\n",
        "📋 账号信息:"
    ]
    
    # 添加账号信息（带密码遮罩）
    for i, (email, password) in enumerate(accounts, 1):
        notification.append(f"  账号 {i}: {email}")
        notification.append(f"  密码 {i}: {mask_password(password)}\n")
    
    notification.append("🎉 签到结果 🎉")
    
    # 执行签到
    for i, (email, password) in enumerate(accounts, 1):
        print(f"\n处理账号 {i}: {email}")
        success, msg = login_and_checkin(email, password)
        result_line = f"  账号 {i}: {'✅' if success else '❌'} {msg}"
        print(result_line)
        notification.append(result_line)
        time.sleep(3)  # 避免请求过快
    
    # 发送通知
    send_telegram_message("\n".join(notification))
    print("\n所有账号处理完成")

if __name__ == "__main__":
    main()
