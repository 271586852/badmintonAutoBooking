from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import  json


# 指定Chrome浏览器驱动的路径


# 配置Chrome选项以启用日志记录
chrome_options = Options()
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")

# 启动浏览器
driver = webdriver.Chrome()

# 访问要登录的页面
driver.get("https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do#/sportVenue")

# time.sleep(50)

book_day = "2024-03-06"

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

# 等待[@id="sportVenue"]/div[1]/div/div[1]出现
area_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sportVenue"]/div[1]/div/div[1]')))
area_button.click()

badminton_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/img')))
badminton_button.click()

time.sleep(3)



# 获取浏览器所有Cookies
all_cookies = driver.get_cookies()
# 根据Cookie名称获取特定Cookie的值
cookie_value = driver.get_cookie("cookie_name")
# 打印Cookies
for cookie in all_cookies:
    print(cookie)




# url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do"

# getTimeList_data = {
#     "XQ": 1,
#     "YYRQ": book_day,
#     "YYLX": 1.0,
#     "XMDM": "001"
# }

# response = requests.post(url, data=getTimeList_data,cookies=cookies)
# print(response)

# re_data = json.loads(response.text)
# print (re_data)


time.sleep(500)

# 关闭浏览器
driver.close()
