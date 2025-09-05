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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": f"{BASE_URL}/auth/login",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

def checkin(email, password):
    """执行签到操作"""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        # 登录
        login_data = {
            "email": email,
            "passwd": password,
            "remember_me": "on"
        }
        
        login_response = session.post(LOGIN_URL, data=login_data)
        login_result = login_response.json()
        
        if login_result.get("ret") != 1:
            return f"登录失败: {login_result.get('msg', '未知错误')}"
        
        # 签到
        checkin_response = session.post(CHECKIN_URL)
        checkin_result = checkin_response.json()
        
        if checkin_result.get("ret") == 1:
            return f"签到成功: {checkin_result.get('msg', '获取流量成功')}"
        else:
            return f"签到失败: {checkin_result.get('msg', '未知错误')}"
            
    except Exception as e:
        return f"操作异常: {str(e)}"
    finally:
        session.close()

if __name__ == "__main__":
    if not ACCOUNTS:
        print("未配置任何账号，请检查ACCOUNTS环境变量")
    else:
        print(f"开始执行签到，共{len(ACCOUNTS)}个账号")
        for i, (email, password) in enumerate(ACCOUNTS, 1):
            print(f"\n处理第{i}个账号: {email}")
            result = checkin(email, password)
            print(result)
            # 每个账号签到间隔3-5秒，避免请求过于频繁
            time.sleep(3 + i % 2)
        print("\n所有账号签到处理完毕")
