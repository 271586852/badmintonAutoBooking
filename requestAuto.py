import tkinter as tk
from tkinter import Image, ttk
import requests
import json
import time
from pprint import pprint
import random
import pytz
import datetime
from PIL import Image, ImageTk
import schedule
from datetime import datetime
import datetime as dt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import tkinter.messagebox as messagebox


# 设置下列参数,然后运行脚本即可
# 必须设置的参数如下
# 1 cookies参数 cookie_str自行从浏览器中获取 
# 2 订场时间 例子："19:00-20:00"
# 3 订场日期 例子："2024-01-03"
# 4 运行时间 例子："13:30:01"
# 5 学号
# 6 姓名
# 7 手机号


# 初始化全局变量
available_rooms = []
cookie_str = ''
remaining_seconds = 0
booked_times = []
getTimeListNumber = 0
getOpeningRoomNumber = 0
bookRoomNumber = 0
cookies = {}
start_time = ''
end_time = ''
book_timeKS = ''
book_timeJS = ''
getTimeList_data = {}
getOpeningRoom_data = {}
headers = {}
checkTime = False


book_time = "19:00-20:00"
book_day = "2024-03-03"
run_time = "12:29:00"
YYRGH = ""
YYRXM = ""
LXFS = ""


# 更新请求数据
getTimeList_data = {
    "XQ": 1,
    "YYRQ": book_day,
    "YYLX": 1.0,
    "XMDM": "001"
}
getOpeningRoom_data = {
    "XMDM": "001",
    "YYRQ": book_day,
    "YYLX": 1.0,
    "KSSJ": book_timeKS,
    "JSSJ": book_timeJS,
    "XQDM": 1
}

accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

urlGetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

urlGetOpeningRoom = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/modules/sportVenue/getOpeningRoom.do'

headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer ,'Cache-Control': 'no-cache'}

# 创建窗口
root = tk.Tk()
root.title("羽毛球场订场666")

# 定义变量
username_var = tk.StringVar()
password_var = tk.StringVar()
cookie_str_var = tk.StringVar()
book_time_var = tk.StringVar()
book_day_var = tk.StringVar()
run_time_var = tk.StringVar()
YYRGH_var = tk.StringVar()
YYRXM_var = tk.StringVar()
LXFS_var = tk.StringVar()
run_script_var = tk.BooleanVar()

# 创建按钮
tutorial_button = ttk.Button(root, text="订场教程", command=lambda: show_cookie_tutorial(root))
tutorial_button.grid(row=0, column=0, columnspan=2, pady=2)


# poem_button = ttk.Button(root, text="切换诗词", command=change_poem)
# poem_button.grid(row=11, column=0, columnspan=2, pady=10)

# 定义按钮点击事件
def show_cookie_tutorial(parent):
    # 创建新窗口
    tutorial_window = tk.Toplevel(parent)
    tutorial_window.title("订场教程")

    # 创建文本框
    text = tk.Text(tutorial_window, height=10, width=50)
    text.pack()

    # 显示文本内容
    text.insert(tk.END, "1、最好当天抢场前一个小时内运行本脚本\n")
    text.insert(tk.END, "2、若需要定时执行，则勾选设定运行时间；若需要立即运行，则取消勾选设定运行时间\n")
    text.insert(tk.END, "3、运行后会弹出浏览器,不要关闭窗口\n")


# 创建输入字段
ttk.Label(root, text="学号:").grid(row=1, column=0, sticky=tk.W, padx=7)
ttk.Entry(root, textvariable=username_var).grid(row=1, column=1)
username_var.set("")

# 创建输入字段
ttk.Label(root, text="密码:").grid(row=2, column=0, sticky=tk.W, padx=7)
password_entry = ttk.Entry(root, textvariable=password_var, show="*")
password_entry.grid(row=2, column=1)
password_var.set("")

# 创建眼镜按钮
show_password = tk.BooleanVar()
show_password.set(False)

def toggle_password_visibility():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

password_button = ttk.Checkbutton(root, text="", variable=show_password, command=toggle_password_visibility)
password_button.grid(row=2, column=2, sticky=tk.W)

# # 创建输入字段
# ttk.Label(root, text="Cookie 字符串:").grid(row=2, column=0, sticky=tk.W)
# ttk.Entry(root, textvariable=cookie_str_var).grid(row=2, column=1)
# cookie_str_var.set("")

ttk.Label(root, text="订场时间:").grid(row=3, column=0, sticky=tk.W, padx=7)
book_time_combobox = ttk.Combobox(root, textvariable=book_time_var, values=["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00", "21:00-22:00"])
book_time_combobox.grid(row=3, column=1)
book_time_var.set("20:00-21:00")

ttk.Label(root, text="订场日期:").grid(row=4, column=0, sticky=tk.W, padx=7)
current_date = dt.date.today()
next_date = current_date + dt.timedelta(days=1)
book_day_var.set(next_date.strftime("%Y-%m-%d"))
ttk.Entry(root, textvariable=book_day_var).grid(row=4, column=1)

ttk.Label(root, text="运行时间:").grid(row=5, column=0, sticky=tk.W, padx=7)
ttk.Entry(root, textvariable=run_time_var).grid(row=5, column=1)
run_time_var.set("12:30:03")

# ttk.Label(root, text="学号:").grid(row=6, column=0, sticky=tk.W)
# ttk.Entry(root, textvariable=YYRGH_var).grid(row=6, column=1)
# YYRGH_var.set("")

ttk.Label(root, text="姓名:").grid(row=7, column=0, sticky=tk.W, padx=7)
ttk.Entry(root, textvariable=YYRXM_var).grid(row=7, column=1)
YYRXM_var.set("")

ttk.Label(root, text="手机号:").grid(row=8, column=0, sticky=tk.W, padx=7)
ttk.Entry(root, textvariable=LXFS_var).grid(row=8, column=1)
LXFS_var.set("")

ttk.Checkbutton(root, text="定时运行", variable=run_script_var).grid(row=9, column=0, sticky=tk.W, padx=7)
run_script_var.set(True)

poems = [
    "此身原本不知愁,最怕万一见温柔",
    "海底月是天上月,眼前人是心上人",
    "遇事不决,可问春风",
    "山中何事,松花酿酒,春水煎茶",
    "江山风月,本无常主,闲者便是主人",
    "吹灭读书灯,一身都是月",
    "独立天地间,清风洒兰雪",
    "天地无尘,山河有影",
    "人生自是有情痴,此恨不关风与月",
    "一箫一剑平生意,负尽狂名十五年",
    "楼上看山;城头看雪;灯前看花;舟中看霞;月下看美人",
]

# 创建文本和按钮
poem_label = ttk.Label(root, text=random.choice(poems), anchor="center")
poem_label.grid(row=11, column=0, columnspan=2, )


def change_poem():
    # 切换诗词
    poem_label.config(text=random.choice(poems))

poem_button = ttk.Button(root, text="再来一句", command=change_poem, width=8)
poem_button.grid(row=12, column=0, columnspan=2,  pady = 5)

ttk.Label(root, text="version1.2 coding by @ ", anchor="center").grid(row=13, column=0,columnspan=2)

# 定义窗口关闭事件
root.protocol("WM_DELETE_WINDOW", root.quit)


# # 定义提交按钮的动作
# def submit_action():
#     global cookies, start_time, end_time, book_timeKS, book_timeJS, getTimeList_data, getOpeningRoom_data,book_day,book_time,YYRGH,YYRXM,LXFS
#     # 获取用户输入
#     cookie_str = cookie_str_var.get()
#     book_time = book_time_var.get()
#     book_day = book_day_var.get()
#     run_time = run_time_var.get()
#     YYRGH = YYRGH_var.get()
#     YYRXM = YYRXM_var.get()
#     LXFS = LXFS_var.get()


#     # cookie_str = 'EMAP_LANG=zh; _WEU=rRRwyrCKKMI23PHd5YPOTIEWeqX9PxqH155eG14O69G5FqbO_B9NvocYb5cEqH34y*7wQasWUhNcPhU_AmqklzwN3jjZogVMGphYJhVagcrNDj*fbi3vZkyOlfKpcSyI0pi9jO7IuD0z9T*bPdX1tYmU5zd1koJyouGqEJ5anywd2Mz3sFCEW9srRMmEXLoFjXbhWANexkE5iyVhjacwbj..; loginServiceclassifyId=all; loginServiceroleId=all; loginServiceSearchVal=; loginServiceserchVal=; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19731%7CMCMID%7C91670754967293786780646029497931279130%7CMCAAMLH-1705326203%7C3%7CMCAAMB-1705326203%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1704728603s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0%7CMCCIDH%7C1111208270; s_pers=%20v8%3D1704721403137%7C1799329403137%3B%20v8_s%3DMore%2520than%252030%2520days%7C1704723203137%3B%20c19%3Dsd%253Ahome%253Ahpx%7C1704723203139%3B%20v68%3D1704721404542%7C1704723203141%3B; openLoginServicePageFlag=false; amp.locale=undefined; asessionid=8fcaa73d-8de8-48a6-b300-7ec2cea60917; route=f9bb7d1dbb51bc04862ec2b9cddaff48; MOD_AUTH_CAS=MOD_AUTH_ST-259230-oPCkHFTFfQYrz1dmqSaa1709438447447-n3kw-cas'

#     # book_time = "19:00-20:00"
#     # book_day = "2024-03-03"
#     # run_time = "12:29:00"
#     # YYRGH = "2310324009"
#     # YYRXM = "顾仁杰"
#     # LXFS = "18218196660"

#     # 设置cookies和其他参数
#     cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}
#     start_time = book_day + " " + book_time.split("-")[0]
#     end_time = book_day + " " + book_time.split("-")[1]
#     book_timeKS = book_time.split("-")[0]
#     book_timeJS = book_time.split("-")[1]
#     # print(cookies,start_time)

#     # 更新请求数据
#     getTimeList_data = {
#         "XQ": 1,
#         "YYRQ": book_day,
#         "YYLX": 1.0,
#         "XMDM": "001"
#     }
#     getOpeningRoom_data = {
#         "XMDM": "001",
#         "YYRQ": book_day,
#         "YYLX": 1.0,
#         "KSSJ": book_timeKS,
#         "JSSJ": book_timeJS,
#         "XQDM": 1
#     }

#     print('submit_action',cookie_str, book_time, book_day, run_time, YYRGH, YYRXM, LXFS)

#     # 输出以确认
#     print(f"预定日期：{book_day}, 预定时间：{book_timeKS}")
#     # 根据用户选择执行
#     print('run_script_var',run_script_var.get())
#     root.withdraw()
#     if run_script_var.get():
#         runScriptTime(run_time)
#         startRun()
#     else:
#         startRun()


# 定义提交按钮的动作
def submit_action():
    global start_time, end_time, book_timeKS, book_timeJS, getTimeList_data, getOpeningRoom_data,book_day,book_time,YYRGH,YYRXM,LXFS,username, password,cookies_str,cookies,run_time
    # 获取用户输入
    username = username_var.get()
    password = password_var.get()
    # cookie_str = cookie_str_var.get()
    book_time = book_time_var.get()
    book_day = book_day_var.get()
    run_time = run_time_var.get()
    YYRGH = username_var.get()
    YYRXM = YYRXM_var.get()
    LXFS = LXFS_var.get()
    
    
    if not all([username, password, book_time, book_day, run_time, YYRGH, YYRXM, LXFS]):
        messagebox.showinfo("提示", "请完整输入信息")
        return
    
    # 检测username是否为十位阿拉伯数字
    if not re.match(r'^\d{10}$', username):
        messagebox.showinfo("提示", "用户名必须为十位阿拉伯数字")
        return

    # 检测book_day是否为xxxx-xx-xx
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', book_day):
        messagebox.showinfo("提示", "日期格式必须为xxxx-xx-xx")
        return

    # 检测run_time是否为xx:xx:xx
    if not re.match(r'^\d{2}:\d{2}:\d{2}$', run_time):
        messagebox.showinfo("提示", "时间格式必须为xx:xx:xx")
        return
    
    # 检测LXFS是否为11位阿拉伯数字
    if not re.match(r'^\d{11}$', LXFS):
        messagebox.showinfo("提示", "手机号必须为11位阿拉伯数字")
        return
    
    # 检测book_time是否为xx:xx-xx:xx
    if not re.match(r'^\d{2}:\d{2}-\d{2}:\d{2}$', book_time):
        messagebox.showinfo("提示", "时间格式必须为xx:xx-xx:xx")
        return
    
    authorized_users = ["顾仁杰", "黄冰洁", "李厚池", "郑嘉宜", "林绮婷", "袁之彬", "张李希", "李灿鹏", "夏禹", "阚思琪", "王智灵", "邓莉莉"]
    if YYRXM not in authorized_users:
        messagebox.showinfo("提示","用户未经授权，请联系授权")
        return
    
    
    # 其他代码...


    root.withdraw()

    # 判断run_script_var.get()是否为真
    # 若为真，判断当前时间离运行时间是否小于180秒，当小于180秒时，直接运行get_login_cookies函数
    # 若为假，直接运行get_login_cookies函数


    # if run_script_var.get() == True:
    #     beijing_tz = pytz.timezone('Asia/Shanghai')
    #     current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")
        

    #     if current_time >= start_time:
    #         print("已经过了指定的开始时间。", datetime.now(beijing_tz).strftime("%H:%M:%S"))
    #         return
        
    #     start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    #     current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
    #     remaining_seconds = start_time_seconds - current_time_seconds
    #     print(f"距离 {start_time} 的剩余时间：{remaining_seconds} 秒")
    #     if remaining_seconds < 300:
    #         get_login_cookies(username, password)
    # else:
    #     get_login_cookies(username, password)

    # 自动cookies
    # get_login_cookies(username, password)
    # print('cookies',cookies)



    # get_login_cookies(username, password)
    # print('cookie_str',cookies_str)

    # cookie_str = 'EMAP_LANG=zh; _WEU=rRRwyrCKKMI23PHd5YPOTIEWeqX9PxqH155eG14O69G5FqbO_B9NvocYb5cEqH34y*7wQasWUhNcPhU_AmqklzwN3jjZogVMGphYJhVagcrNDj*fbi3vZkyOlfKpcSyI0pi9jO7IuD0z9T*bPdX1tYmU5zd1koJyouGqEJ5anywd2Mz3sFCEW9srRMmEXLoFjXbhWANexkE5iyVhjacwbj..; loginServiceclassifyId=all; loginServiceroleId=all; loginServiceSearchVal=; loginServiceserchVal=; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19731%7CMCMID%7C91670754967293786780646029497931279130%7CMCAAMLH-1705326203%7C3%7CMCAAMB-1705326203%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1704728603s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0%7CMCCIDH%7C1111208270; s_pers=%20v8%3D1704721403137%7C1799329403137%3B%20v8_s%3DMore%2520than%252030%2520days%7C1704723203137%3B%20c19%3Dsd%253Ahome%253Ahpx%7C1704723203139%3B%20v68%3D1704721404542%7C1704723203141%3B; openLoginServicePageFlag=false; amp.locale=undefined; asessionid=8fcaa73d-8de8-48a6-b300-7ec2cea60917; route=f9bb7d1dbb51bc04862ec2b9cddaff48; MOD_AUTH_CAS=MOD_AUTH_ST-259230-oPCkHFTFfQYrz1dmqSaa1709438447447-n3kw-cas'

    # book_time = "19:00-20:00"
    # book_day = "2024-03-03"
    # run_time = "12:29:00"
    # YYRGH = "2310324009"
    # YYRXM = "顾仁杰"
    # LXFS = "18218196660"



    start_time = book_day + " " + book_time.split("-")[0]
    end_time = book_day + " " + book_time.split("-")[1]
    book_timeKS = book_time.split("-")[0]
    book_timeJS = book_time.split("-")[1]
    # print(cookies,start_time)

    # 更新请求数据
    getTimeList_data = {
        "XQ": 1,
        "YYRQ": book_day,
        "YYLX": 1.0,
        "XMDM": "001"
    }
    getOpeningRoom_data = {
        "XMDM": "001",
        "YYRQ": book_day,
        "YYLX": 1.0,
        "KSSJ": book_timeKS,
        "JSSJ": book_timeJS,
        "XQDM": 1
    }

    # print('submit_action',cookie_str, cookies,book_time, book_day, run_time, YYRGH, YYRXM, LXFS)

    # 输出以确认
    print(f"预定日期：{book_day}, 预定时间：{book_timeKS}")
    # 根据用户选择执行
    # print('run_script_var',run_script_var.get())
    root.withdraw()
    if run_script_var.get():
        get_login_cookies(username, password,print_callback)
        runScriptTime(run_time)
        startRun()
    else:
        get_login_cookies(username, password,startRun)
        # startRun()


def print_callback():
    print("Callback triggered!")


# -----------------------下面参数勿修改-----------------------
# available_rooms = []  # Store the WID of available rooms
# booked_times = []  # Store the fully booked times
# getTimeListNumber = 0
# getOpeningRoomNumber = 0



# cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}

# # cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ")}
# start_time = book_day + " " + book_time.split("-")[0]
# end_time = book_day + " " + book_time.split("-")[1]
# book_timeKS = book_time.split("-")[0]
# book_timeJS = book_time.split("-")[1]



# getTimeList_data = {
#     "XQ": 1,
#     "YYRQ": book_day,
#     "YYLX": 1.0,
#     "XMDM": "001"
# }

# getOpeningRoom_data = {
#     "XMDM": "001",
#     "YYRQ": book_day,
#     "YYLX": 1.0,
#     "KSSJ": book_timeKS,
#     "JSSJ": book_timeJS,
#     "XQDM": 1
# }


# ------------------------------
# accept = "*/*"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

# url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

# urlGetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

# urlGetOpeningRoom = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/modules/sportVenue/getOpeningRoom.do'

# headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer ,'Cache-Control': 'no-cache'}


# ------------------------------



def bookRoom(availableRoom):
    global available_rooms,bookRoomNumber
    # print('bookRoom函数',available_rooms)
    if "15093a7663fa498695608f3d52cca59d" in availableRoom:
        Room = "15093a7663fa498695608f3d52cca59d"
    elif "5bf45a019b8d40aaafbda985beb63dde" in availableRoom:
        Room = "5bf45a019b8d40aaafbda985beb63dde"
    elif "8c3d2aa5b7bf4067922153764c24934b" in availableRoom:
        Room = "8c3d2aa5b7bf4067922153764c24934b"
    elif "128957e632104f57b3fe9bb9fe0a7770" in availableRoom:
        Room = "128957e632104f57b3fe9bb9fe0a7770" 

    
    else:
        Room = random.choice(availableRoom)
        print('Room为', Room)

    # availableRoom.remove(Room)  
    # print("移除后的",availableRoom)
    bookBadminton_data = {
        "DHID": "",
        "YYRGH": YYRGH,
        "CYRS": '',
        "YYRXM": YYRXM,
        "LXFS": LXFS,
        "CGDM": "001",
        "CDWID": Room,
        "XMDM": "001",
        "XQWID": 1,
        "KYYSJD": book_time,
        "YYRQ": book_day,
        "YYLX": 1.0,
        "YYKS": start_time,
        "YYJS": end_time,
        "PC_OR_PHONE": "pc"
    }
    try:
        re = requests.post(url, data=bookBadminton_data, headers=headers, cookies=cookies)
        re.raise_for_status()

        try:
            re_data = json.loads(re.text)
            print(re_data,'预约成功，时间为',book_day,book_time,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\n')
        except json.JSONDecodeError:
            # print("无效的 JSON 数据: ", re.text)
            if "您来迟了" in re.text:
                print("您来迟了")
                availableRoom.remove(Room)
                print("移除后的",len(available_rooms))
                if availableRoom:
                    bookRoom(availableRoom)  
                else:
                    print(book_day,book_time,"这个时间段已经没空场了")
                    getTimeList()
                    return False
            
            if "该预约日期暂未开放预约" in re.text:
                print("该预约日期暂未开放预约")
                return False    

            if "您已预约" in re.text:
                print("您已预约")
                return False
            
    except requests.RequestException as e:
        print(f"bookRoomError: {e}")
        bookRoomNumber += 1
        if bookRoomNumber < 3:
            time.sleep(1.2)
            bookRoom(availableRoom)        
        return False
    
    print('bookRoom调用结束')
    
def getOpeningRoom():
    global available_rooms,getOpeningRoomNumber
    # print('getOpeningRoom',getOpeningRoom_data)
    try:
        re = requests.post(urlGetOpeningRoom, data=getOpeningRoom_data, headers=headers, cookies=cookies)
        re.raise_for_status()
        try:
            re_data = json.loads(re.text)
            print('日期为：', book_day, '时间为', book_time, '的空余场地信息：')
            # pprint(re_data['datas']['getOpeningRoom']['rows'])
            for item in re_data['datas']['getOpeningRoom']['rows']:
                if item['text'] == '可预约':
                    available_rooms.append(item['WID'])
                    pprint({
                        'WID': item['WID'],
                        'text': item['text'],
                        'CDMC': item['CDMC']
                    })
            print('\n')
            
            if available_rooms:
                print('可预约场地有',len(available_rooms),'个')
                bookRoom(available_rooms)

            else:
                getOpeningRoomNumber += 1
                if getOpeningRoomNumber < 5:
                    time.sleep(1.2)
                    print('调用getOpeningRoomNumber第',getOpeningRoomNumber,'次',book_day,"没有空场了")
                    getOpeningRoom()
                return False
        
        except json.JSONDecodeError:
            print("getOpeningRoomError: ", re.text)
            getOpeningRoomNumber += 1
            if "该预约日期暂未开放预约" in re.text:
                print("该预约日期暂未开放预约")
                return False    
            if getOpeningRoomNumber < 3:
                time.sleep(1.2)
                getOpeningRoom()
            return False
 
    except requests.RequestException as e:
        print(f"getOpeningRoomError: {e}")
        getOpeningRoomNumber += 1
        if "该预约日期暂未开放预约" in re.text:
            print("该预约日期暂未开放预约")
            return False   
        if getOpeningRoomNumber < 3:
            time.sleep(1.2)
            getOpeningRoom()
        return False
    
    print('getOpeningRoom调用结束')

def getTimeList():
    global book_time, start_time, end_time, booked_times,getOpeningRoom_data,book_timeKS,book_timeJS,getTimeListNumber,YYRGH,YYRXM,LXFS

    # print('打印信息',cookies,book_time,book_day,run_time,YYRGH,YYRXM,LXFS)
    try:
        re = requests.post(urlGetTimeList, data=getTimeList_data, headers=headers, cookies=cookies)
        re.raise_for_status()
        try:
            re_data = json.loads(re.text)
            print('日期为：', book_day,  '的场地信息：')
            for item in re_data:
                # print(item)
                if item['text'] == '可预约':
                    booked_times.append(item['NAME'])
            print(book_day,'可预约时间为',booked_times,'\n')
            
            if booked_times:
                if book_time not in booked_times:
                    if "19:00-20:00" in booked_times:
                        book_time = "19:00-20:00"
                    elif "20:00-21:00" in booked_times:
                        book_time = "20:00-21:00"
                    elif "18:00-19:00" in booked_times:
                        book_time = "18:00-19:00"
                    elif "17:00-18:00" in booked_times:
                        book_time = "17:00-18:00"
                    elif "21:00-22:00" in booked_times:
                        book_time = "21:00-22:00"
                    else:
                        book_time = random.choice(booked_times)

                book_timeKS = book_time.split("-")[0]
                book_timeJS = book_time.split("-")[1]
                print(book_timeKS,book_timeJS,'\n')

                # book_timeKS修改后，还需要对getOpeningRoom_data中的book_timeKS进行修改
                getOpeningRoom_data["KSSJ"] = book_timeKS
                getOpeningRoom_data["JSSJ"] = book_timeJS

                print('修改后的',book_time)
                start_time = book_time.split('-')[0]
                end_time = book_time.split('-')[1]
                # print('getTimeList',getOpeningRoom_data)

                getOpeningRoom()
                
            else:
                getTimeListNumber += 1
                if getTimeListNumber < 5:
                    time.sleep(1.2)
                    print('调用第',getTimeListNumber,'次',book_day,"没有空场了")
                    getTimeList()
                return False
                
        except json.JSONDecodeError:
            print("getTimelistError: ", re.text)
            getTimeListNumber += 1
            if "该预约日期暂未开放预约" in re.text:
                print("该预约日期暂未开放预约")
                return False   
            if getTimeListNumber < 5:
                time.sleep(1.2)
                getTimeList()
            return False
 
    except requests.RequestException as e:
        print(f"getTimelistError: {e}")
        getTimeListNumber += 1
        if "该预约日期暂未开放预约" in re.text:
            print("该预约日期暂未开放预约")
            return False   
        if getTimeListNumber < 5:
            time.sleep(1.2)
            getTimeList()
        return False  
    
    print('getTimeList调用结束')

def get_login_cookies(username, password,callback):
    global cookies_str,cookies
    # 配置Chrome选项以启用日志记录
    chrome_options = Options()
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")

    # 启动浏览器
    driver = webdriver.Chrome()

    # 访问要登录的页面
    driver.get("https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do#/sportVenue")

    

    # 查找页面的用户名和密码输入框，并输入对应的值
    username_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='username']")))    
    username_input.clear()
    username_input.send_keys(username)

    password_input = driver.find_element(By.XPATH,"//*[@id='password']")
    password_input.clear()
    password_input.send_keys(password)

   
    checkbox_xpath = '//*[@id="casLoginForm"]/p[4]/div'
    checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
    checkbox.click()

    # 查找登录按钮，点击进行登录
    login_button = driver.find_element(By.XPATH,"//*[@id='casLoginForm']/p[5]/button")
    login_button.click()

    time.sleep(3)

    # 等待[@id="sportVenue"]/div[1]/div/div[1]出现
    area_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sportVenue"]/div[1]/div/div[1]')))
    area_button.click()

    badminton_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sportVenue"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/img')))
    badminton_button.click()

    time.sleep(3)



    # # 获取浏览器所有Cookies
    # all_cookies = driver.get_cookies()
    # # 根据Cookie名称获取特定Cookie的值

    # jsonCookies = json.dumps(all_cookies)  # 转换成字符串保存

    # with open('damai_cookies.txt', 'w') as f:
    #     f.write(jsonCookies)
    # print('cookies保存成功！')


    # # 打印Cookies
    # for cookie in all_cookies:
    #     print(cookie)
        


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


    # 创建一个requests.session对象
    session = requests.Session()
    agent = driver.execute_script("return navigator.userAgent")
    print(agent,type(agent))
    # 获取登录cookies
    saveCookies = driver.get_cookies()
    c = saveCookies[0]['value']
    # print(saveCookies)
    # 将cookies设置到session中
    for cookie in saveCookies:
        session.cookies.set(cookie['name'],cookie['value'])
    # print('session的值', '键名:', session.cookies.keys(), 'value值:', session.cookies.values())

    # cookies_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in session.cookies])
    cookies_str = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
    print('\n','已经拼接cookies：',cookies_str)
    cookies = {item.split("=")[0]: item.split("=")[1] for item in cookies_str.split("; ") if "=" in item}
    # print('cookies',cookies)

    if cookies != 0:
        success = True  # 假设成功获取 cookies
    if success:
        print("成功获取 cookies。")
        callback()  # 获取成功，调用回调函数
    else:
        print("获取 cookies 失败。")


# 特定时间运行
def runScriptTime(start_time,is_restarted=False):
    global remaining_seconds
    # 获取当前的北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

    # 打印北京时间
    # print('currentTime',current_time)
    # print('startTime',start_time)
    
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
        # 如果剩余时间小于180秒，且未重启，调用get_login_cookies()
        if remaining_seconds < 180 and not is_restarted:
            # get_login_cookies(username, password,runScriptTime(start_time, is_restarted=True))
            print(f"剩余时间小于180秒，重新开始计时。")
            runScriptTime(start_time, is_restarted=True)
    
    print("开始运行程序！", datetime.now(beijing_tz).strftime("%H:%M:%S"), '\n')



def startRun():
    print('打印信息','\n','cookies：',cookies,'\n','预约时间：',book_time,'\n','预约日期：',book_day,'\n','运行时间',run_time,'\n','学号',YYRGH,'\n','姓名',YYRXM,'\n','预约电话',LXFS)

    getTimeList()
    # print('打印信息Get后',cookies,book_time,book_day,run_time,YYRGH,YYRXM,LXFS)

    print('程序运行结束')

    
# 创建提交按钮
ttk.Button(root, text="提交", command=submit_action).grid(row=10, column=0, columnspan=2, pady=10)

# 启动 Tkinter 事件循环
root.mainloop()

# if __name__ == "__main__":

    # print(book_time, book_day, start_time, end_time,run_time,'\n')
    # print(cookies,'\n')
    # print(book_timeKS,book_timeJS,'\n')

    # 自动获取用户cookie，日后完善
    # get_login_cookies(username, password, login_url)

    # 设定运行时间
    # runScriptTime(run_time)
    # 入口函数
    # startRun()

    # 下列代码，用于测试，一般情况下注释下面的代码
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    # getTimeList()
    # getOpeningRoom()