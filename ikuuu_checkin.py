import requests
import time
import os
import json
from typing import List, Tuple

# 配置常量
BASE_URL = "https://ikuuu.org"
LOGIN_URL = f"{BASE_URL}/auth/login"
CHECKIN_URL = f"{BASE_URL}/user/checkin"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Telegram 配置（从环境变量获取）
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def mask_password(password: str) -> str:
    """密码遮罩处理：显示前2位和后2位，中间用*代替"""
    if len(password) <= 4:
        return "*" * len(password)
    return f"{password[:2]}{'*' * (len(password)-4)}{password[-2:]}"


def load_accounts() -> List[Tuple[str, str]]:
    """从环境变量加载多账号信息"""
    accounts_str = os.getenv("ACCOUNTS"， "")  # 正确的英文逗号
    accounts = []
    if not accounts_str:
        return accounts
        
    for item in accounts_str.split(";"):
        if item 和 "," 在 item:
            email, password = item.split(","， 1)
            accounts.append((email.strip(), password.strip()))
    return accounts


def send_telegram_message(content: str) -> None:
    """发送消息到Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ 未配置Telegram参数，跳过通知")
        return
        
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": content,
                "parse_mode": "Markdown"  # 支持简单格式
            }
        )
        if response.status_code != 200:
            print(f"❌ Telegram通知发送失败: {response.text}")
    except Exception as e:
        print(f"❌ Telegram通知异常: {str(e)}")


def login_and_checkin(email: str, password: str) -> str:
    """登录并执行签到，返回结果信息"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Referer": f"{BASE_URL}/auth/login",
        "X-Requested-With": "XMLHttpRequest"
    })
    
    # 登录
    try:
        login_data = {"email": email, "passwd": password, "code": ""}
        login_res = session.post(LOGIN_URL, data=login_data, timeout=15)
        login_res.raise_for_status()
        login_result = login_res.json()
        
        if login_result.get("ret") != 1:
            return f"登录失败: {login_result.get('msg', '未知错误')}"
    except Exception as e:
        return f"登录异常: {str(e)}"
    
    # 签到
    try:
        checkin_res = session.post(CHECKIN_URL, timeout=15)
        checkin_res.raise_for_status()
        checkin_result = checkin_res.json()
        return checkin_result.get("msg", "签到结果未知")
    except Exception as e:
        return f"签到异常: {str(e)}"


def main():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S")
    accounts = load_accounts()
    notification_lines = [
        f"📅 执行时间: {start_time}",
        f"🌐 地址: {BASE_URL}",
        ""  # 空行分隔
    ]
    
    if not accounts:
        print("❌ 未配置任何账号")
        notification_lines.append("❌ 未配置任何账号，请检查ACCOUNTS变量")
        send_telegram_message("\n".join(notification_lines))
        return
    
    # 处理所有账号
    notification_lines.append("📋 账号信息:")
    for i, (email, password) in enumerate(accounts, 1):
        masked_pwd = mask_password(password)
        notification_lines.append(f"  账号 {i}: {email}")
        notification_lines.append(f"  密码 {i}: {masked_pwd}")
        notification_lines.append("")  # 账号间空行分隔
    
    # 签到结果部分
    notification_lines.append("🎉 签到结果 🎉")
    for i, (email, password) in enumerate(accounts, 1):
        print(f"\n处理账号 {i}: {email}")
        result = login_and_checkin(email, password)
        notification_lines.append(f"  账号 {i}: {result}")
        time.sleep(3)  # 账号间隔
    
    # 发送通知
    final_message = "\n".join(notification_lines)
    print("\n" + final_message)
    send_telegram_message(final_message)


if __name__ == "__main__":
    main()
