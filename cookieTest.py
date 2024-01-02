import requests
from bs4 import BeautifulSoup  # 如果需要处理HTML

# 目标网站的登录页面URL和登录操作URL
login_page_url = 'https://ehall.szu.edu.cn/login_page'
login_url = 'https://authserver.szu.edu.cn/authserver/login?service=https://ehall.szu.edu.cn:443/qljfwapp/sys/lwSzuCgyy/index.do%23%2FsportVenue'

# 创建一个session对象
session = requests.Session()

# 设置一个常见的用户代理，模仿浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


# TODO: 从soup中提取任何必要的隐藏字段，例如CSRF令牌
# csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

# 登录信息
payload = {
    'username': '2310324009',
    'password': '11185272',
    # 'csrf_token': csrf_token,  # 添加隐藏字段，如果有的话
}

# 发送POST请求进行登录
response = session.post(login_url, data=payload, headers=headers)

# 打印响应内容
print("Response Content:")
print(response.text)

# 获取cookie
cookies = session.cookies

# 打印cookie
print("\nCookies:")
for cookie in cookies:
    print(f"{cookie.name}: {cookie.value}")
