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

jsonCookies = json.dumps(all_cookies)  # 转换成字符串保存

with open('damai_cookies.txt', 'w') as f:
    f.write(jsonCookies)
print('cookies保存成功！')


# 打印Cookies
for cookie in all_cookies:
    print(cookie)
    
time.sleep(3)
print('---------------------------------')



# cookie_str ='EMAP_LANG=zh; _WEU=NSUDWf1tGICtvoeNyRVYB6_Hcu1JFg*f68wEF0RoYx4XezZ3vaBNs1uq9kOCiPBh7bHsuBrp0jzYywmf_vw6tzP308bgLV97gKOMcSTivwEMN2Ha18B6uTCtdGx6FuzroeJR1o1DbSdbNgJexDuzFWypuirWvCVBN7r4lW2TyhbdzbVSP6OVzUij8jiDPOK2va6rMMr*xic.; asessionid=bb2e1ce1-f376-43dd-bef2-461385b7bd36; route=6fcc95effda7818ac250c10acfaab6fc'

# cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}



url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do"
# ------------------------------
accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

urlGetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

urlGetOpeningRoom = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/modules/sportVenue/getOpeningRoom.do'

headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer ,'Cache-Control': 'no-cache'}


# ------------------------------
getTimeList_data = {
    "XQ": 1,
    "YYRQ": book_day,
    "YYLX": 1.0,
    "XMDM": "001"
}

# loginCookie = {'domain': 'ehall.szu.edu.cn', 'httpOnly': 'False', 'name': '_WEU', 'path': '/qljfwapp/', 'sameSite': 'Lax', 'secure': 'True', 'value': 'rnbdYeAoidLVBzT6DkWZnpNYSxE7SetRWszVYDu*1N6bpX9zGbfr9nKWirh_DrrJRo_EXqWfIVx5A7aQ*JJSLH8X3GCJXMAIqWQEby1ZGYbQKZYCij80*j8EyqYhqJv0EQp8_M3saSIsCpozyATaIzQSEIQTX8*I5beQKHbcIvKMErfHZeEx2_mVFAARpF1R'}

# re = requests.post(urlGetTimeList, data=getTimeList_data, headers=headers,cookies=loginCookie)
# print(loginCookie)
# re.raise_for_status()
# print(re.text)

# re_data = json.loads(re.text)
print('日期为：', book_day,  '的场地信息：')
# print(re_data)
   
# print(re)

time.sleep(500)

# 关闭浏览器
driver.close()
