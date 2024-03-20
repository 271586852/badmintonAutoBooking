from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import  json
import datetime
import requests
import json
import time
from pprint import pprint
import random
import pytz
from datetime import datetime
import tkinter as tk
import sys
import pytz
import random

# 密码以星号替代
# 

userName = 0
password = 0
KS_time = "21:00-22:00"
operatingMode = 0
start_time = "12:29:59"

root = tk.Tk()
root.title("Parameter Input")
root.geometry("300x300")

userNumber_label = tk.Label(root, text="学号:")
userNumber_label.pack()
userNumber_entry = tk.Entry(root)
userNumber_entry.pack()

passwordNumber_label = tk.Label(root, text="密码:")
passwordNumber_label.pack()
passwordNumber_entry = tk.Entry(root, show="*")
passwordNumber_entry.pack()

KS_time_label = tk.Label(root, text="打球开始时间:")
KS_time_label.pack()
KS_time_entry = tk.Entry(root)
KS_time_entry.insert(0, "21:00-22:00")  # Set default value
KS_time_entry.pack()


run_mode = tk.IntVar()

run_mode_label = tk.Label(root, text="运行模式:")
run_mode_label.pack()

immediate_run_radio = tk.Radiobutton(root, text="立即运行", variable=run_mode, value=1)
immediate_run_radio.pack()

scheduled_run_radio = tk.Radiobutton(root, text="计划运行", variable=run_mode, value=2)
scheduled_run_radio.pack()

start_time_label = tk.Label(root, text="开始时间:")
start_time_entry = tk.Entry(root)
start_time_entry.insert(0, "12:29:59")  # Set default value

def show_start_time_entry():
    start_time_label.pack()
    start_time_entry.pack()

def hide_start_time_entry():
    start_time_label.pack_forget()
    start_time_entry.pack_forget()

def handle_run_mode_selection():
    if run_mode.get() == 1:
        hide_start_time_entry()
    else:
        show_start_time_entry()

scheduled_run_radio.configure(command=handle_run_mode_selection)
immediate_run_radio.configure(command=handle_run_mode_selection)

handle_run_mode_selection()

def submit():
    global userName, password, start_time, KS_time
    userName = userNumber_entry.get()
    password = passwordNumber_entry.get()
    KS_time = passwordNumber_entry.get()
    start_time = start_time_entry.get()
    print(userName,password,KS_time,start_time)
    root.destroy()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()




beijing_tz = pytz.timezone('Asia/Shanghai')


console_output = tk.Text(root)
console_output.pack()

def redirect_output():
    console_output.insert(tk.END, "开始运行程序！" + datetime.now(beijing_tz).strftime("%H:%M:%S") + "\n")
    sys.stdout = console_output

redirect_button = tk.Button(root, text="Redirect Output", command=redirect_output)
redirect_button.pack()

root.mainloop()


# 指定Chrome浏览器驱动的路径



# 特定时间运行
def runScriptTime(start_time):
    
    # 获取当前的北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

    # 打印北京时间
    print(current_time)
    
    if current_time >= start_time:
        print("已经过了指定的开始时间。", datetime.now(beijing_tz).strftime("%H:%M:%S"))
        return
    
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
    remaining_seconds = start_time_seconds - current_time_seconds
    
    print(f"距离 {start_time} 的剩余时间：{remaining_seconds} 秒")
    
    while remaining_seconds > 0:
        print(f"剩余时间：{remaining_seconds} 秒", end="\r")
        time.sleep(1)
        remaining_seconds -= 1
    
    print("开始运行程序！", datetime.now(beijing_tz).strftime("%H:%M:%S"), '\n')




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
username_input.send_keys(userName)

password_input = driver.find_element(By.XPATH,"//*[@id='password']")
password_input.clear()
password_input.send_keys(password)

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
    
runScriptTime(start_time)

xpath0 = '//*[@id="apply"]/div[2]/div[2]/div[3]/div' #方便实时更新和切换
button0 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath0)))
button0.click()
# time.sleep(3)
print('---------------------------------')
# 选择运动类型

xpath1 = '//*[@id="apply"]/div[2]/div[2]/div[1]' #羽毛球
# xpath1 = '//*[@id="apply"]/div[2]/div[2]/div[2]' #足球
button1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath1)))
button1.click()

# 选择日期
try:
    xpath2 = '//*[@id="apply"]/div[3]/div[4]/div[2]/label/div[2]'
    button2 = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath2)))
    button2.click()
except:
    xpath2 = '//*[@id="apply"]/div[3]/div[4]/div/label/div[2]'
    button2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath2)))
    button2.click()


# 选择时间
KSTime = 14
# '//*[@id="apply"]/div[3]/div[6]/div[13]/label/div[2]'
# '//*[@id="apply"]/div[3]/div[6]/div[14]/label/div[2]'
hour = int(KS_time.split(":")[0])
KSTime = hour - 7  # Assuming the starting hour is 8:00 AM

# xpath3 = '//*[@id="apply"]/div[3]/div[6]/div[' + str(KSTime) + ']/label/div[2]'
xpath3 = '//*[@id="apply"]/div[3]/div[6]/div[12]/label/div[2]'

button3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath3)))
button3.click()


# 选择场地
# area = 26
# A6 = '//*[@id="apply"]/div[3]/div[10]/div[4]/label/div[2]'
# B6 = '//*[@id="apply"]/div[3]/div[10]/div[10]/label/div[2]'
# C6 = '//*[@id="apply"]/div[3]/div[10]/div[18]/label/div[2]'
# D6 = '//*[@id="apply"]/div[3]/div[10]/div[26]/label/div[2]'

# xpath4 = '//*[@id="apply"]/div[3]/div[10]/div[' + str(area) + ']/label/div[2]'
# button4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath4)))
# button4.click()

# 足球：'//*[@id="apply"]/div[3]/div[10]/div/label/div[2]'
# 羽毛球：'//*[@id="apply"]/div[3]/div[6]/div/label/div[2]'

# 找到所有匹配的元素
elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="apply"]/div[3]/div[10]/div/label/div[2]')))

# 过滤出可点击的元素
clickable_elements = [element for element in elements if element.is_enabled() and element.is_displayed()]
# 过滤出不可点击的元素
unclickable_elements = [element for element in elements if not element.is_enabled() or not element.is_displayed()]
print('不可点击:',unclickable_elements,'\n')
print('可点击:',clickable_elements,'\n')

# 随机选择一个元素进行点击
random.choice(clickable_elements).click()


# 提交预约
xpath5 = '//*[@id="apply"]/div[3]/div[11]/button[2]'
button5 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath5)))
button5.click()



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
