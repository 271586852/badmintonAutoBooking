from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 指定Chrome浏览器驱动的路径

# 启动浏览器
driver = webdriver.Chrome()

# 访问要登录的页面
driver.get("https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do#/sportVenue")

# time.sleep(50)


# 查找页面的用户名和密码输入框，并输入对应的值

username_input = driver.find_element(By.XPATH, "//*[@id='username']")
username_input.clear()
username_input.send_keys("2310324009")

password_input = driver.find_element(By.XPATH,"//*[@id='password']")
password_input.clear()
password_input.send_keys("11185272")

# 查找登录按钮，点击进行登录
login_button = driver.find_element(By.XPATH,"//*[@id='casLoginForm']/p[5]/button")
login_button.click()

time.sleep(8)

# 添加代码，点击该按钮：//*[@id="sportVenue"]/div[1]/div/div[1]
area_button = driver.find_element(By.XPATH, '//*[@id="sportVenue"]/div[1]/div/div[1]')
area_button.click()

time.sleep(3)

badminton_button = driver.find_element(By.XPATH, '//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/img')
badminton_button.click()

time.sleep(3)

# 发送网络请求
driver.get("https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do")

# 获取请求的cookie
request_cookie = driver.execute_script("return document.cookie")

print('request_cookie','\n',request_cookie)

# 取得登录成功后的Cookie
# cookie_dict = driver.get_cookies()

# print('cookie_dict','\n',cookie_dict)

time.sleep(500)

# 关闭浏览器
driver.close()
