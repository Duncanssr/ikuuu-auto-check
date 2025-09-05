import requests
import time
import os

BASE_URL = "https://ikuuu.org"
LOGIN_URL = f"{BASE_URL}/auth/login"
CHECKIN_URL = f"{BASE_URL}/user/checkin"

# 从环境变量读取账号密码（格式：邮箱1,密码1;邮箱2,密码2）
accounts_str = os.getenv("ACCOUNTS", "")
ACCOUNTS = []

# 解析账号密码，增加异常处理
if accounts_str:
    for item in accounts_str.split(';'):
        if item and ',' in item:  # 确保项目不为空且包含分隔符
            parts = item.split(',', 1)  # 限制只分割一次，避免密码中包含逗号
            if len(parts) == 2 and all(parts):  # 确保分割后有两个非空值
                ACCOUNTS.append((parts[0].strip(), parts[1].strip()))
            else:
                print(f"无效的账号格式: {item}")
        else:
            print(f"跳过无效的账号项: {item}")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": f"{BASE_URL}/auth/login",
    "X-Requested-With": "XMLHttpRequest",
}

def login(email, password):
    """登录并返回 session"""
    session = requests.Session()
    session.headers.update(HEADERS)

    data = {
        "email": email,
        "passwd": password,
        "code": ""  # 没有验证码时留空
    }

    try:
        resp = session.post(LOGIN_URL, data=data, timeout=10)
        result = resp.json()
        if result.get("ret") == 1:
            print(f"✅ 登录成功: {email}")
            return session
        else:
            print(f"❌ 登录失败: {email} | {result.get('msg')}")
            return 无
    except Exception:
        print(f"⚠️ 登录异常: {email} | 返回内容: {resp.text[:100]}")
        return None


def check_in(session, email):
    """签到"""
    try:
        resp = session.post(CHECKIN_URL, timeout=10)
        result = resp.json()
        if result.get("ret") == 1:
            print(f"🎉 签到成功: {email} | {result.get('msg')}")
        else:
            print(f"ℹ️ 提示: {email} | {result.get('msg')}")
    except Exception:
        print(f"⚠️ 签到异常: {email} | 返回内容: {resp.text[:100]}")


def main():
    print("🎯 ikuuu 多账号自动签到脚本")
    print(f"📆 时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")

    for email, password in ACCOUNTS:
        print("\n==============================")
        session = login(email, password)
        if session:
            check_in(session, email)


if __name__ == "__main__":
    main()
