import requests
import time

BASE_URL = "https://ikuuu.org"
LOGIN_URL = f"{BASE_URL}/auth/login"
CHECKIN_URL = f"{BASE_URL}/user/checkin"

# 🟢 多账号账号密码列表
ACCOUNTS = [
    ("peige1985@gmail.com", "你的密码1")，
    ("example2@gmail.com", "你的密码2")，
    # 继续加 ...
]

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

