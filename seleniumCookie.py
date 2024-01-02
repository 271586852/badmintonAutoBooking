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
