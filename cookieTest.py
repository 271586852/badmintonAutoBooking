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


# 访问登录页面并获取可能需要的cookie和隐藏字段
response = session.get(login_page_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

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


from selenium import webdriver
from selenium.webdriver.chrome.options import Options


username = 2310324009
password = 11185272



options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)

 # 访问要登录的页面
driver.get("https://www.demo.com/login.html")

 # 查找页面的用户名和密码输入框，并输入对应的值
username_input = 	driver.find_element_by_name("username")
username_input.clear()
username_input.send_keys(username)

password_input = driver.find_element_by_name("password")
password_input.clear()
password_input.send_keys(password)

# 查找登录按钮，点击进行登录
login_button = driver.find_element_by_class_name("login-btn")
login_button.click()

# 取得登录成功后的Cookie
cookie_dict = {}
for cookie in driver.get_cookies():
    cookie_dict[cookie['name']] = cookie['value']

# 关闭浏览器
driver.close()



