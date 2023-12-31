import datetime
import requests
import json
import time
from pprint import pprint
import random
import pytz
from datetime import datetime


# 设置下列四个参数,然后运行脚本即可
# 必须设置的参数如下
# 1 cookies参数
# 2 订场时间 例子："19:00-20:00"
# 3 订场日期 例子："2024-01-03"
# 4 运行时间 例子："13:30:01"

# cookie_str从浏览器中获取
cookie_str = 'EMAP_LANG=zh; _WEU=ibzf2MtHmmhaJTpDjfPFYChvK1oauOQu4R5PL4uStpNA4BhNwRZcFxAE*Zsm7FYb5adbIIdL_TEZjsuml5scobq**SWlx9gfxcnC423NpXG1iXQTb*KH9W_Gaw6BdjXR0GmTDWdl6J9QSg_JrvHnN68vfDiAjOQgpg6aNgtF210yLBjMNN5Q5mawCPRcUAa1w4j8kH8P4OgYkGOJ9Uctkj..; loginServiceclassifyId=all; loginServiceroleId=all; loginServiceSearchVal=; loginServiceserchVal=; openLoginServicePageFlag=false; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19693%7CMCMID%7C91670754967293786780646029497931279130%7CMCAAMLH-1702003739%7C11%7CMCAAMB-1702003739%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1701406139s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0%7CMCCIDH%7C1111208270; s_pers=%20v8%3D1701398952165%7C1796006952165%3B%20v8_s%3DFirst%2520Visit%7C1701400752165%3B%20c19%3Dsd%253Apdfft%253Apdf%253Aurl%7C1701400752171%3B%20v68%3D1701398951526%7C1701400752186%3B; amp.locale=undefined; MOD_AUTH_CAS=MOD_AUTH_ST-1309265-mkpTaIR6afA6HZ7AbhSW1704513091050-eCjG-cas; route=6fcc95effda7818ac250c10acfaab6fc'
book_time = "19:00-20:00"
book_day = "2024-01-07"
run_time = "15:29:00"





available_rooms = []  # Store the WID of available rooms
booked_times = []  # Store the fully booked times
getTimeListNumber = 0
getOpeningRoomNumber = 0



testBadminton_data = {
    "DHID": "",
    "YYRGH": "2310324009",
    "CYRS": '',
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    "CGDM": "001",
    "CDWID": "7981ade524bd4b1ab92d3a622fb0d3af",
    "XMDM": "001",
    "XQWID": 1,
    "KYYSJD": "18:00-19:00",
    "YYRQ": "2024-01-01",
    "YYLX": 1.0,
    "YYKS": "2024-01-01 18:00",
    "YYJS": "2024-01-01 19:00",
    "PC_OR_PHONE": "pc"
}

cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}

# cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ")}
start_time = book_day + " " + book_time.split("-")[0]
end_time = book_day + " " + book_time.split("-")[1]
book_timeKS = book_time.split("-")[0]
book_timeJS = book_time.split("-")[1]



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


# ------------------------------
accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

urlGetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

urlGetOpeningRoom = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/modules/sportVenue/getOpeningRoom.do'

headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer ,'Cache-Control': 'no-cache'}


# ------------------------------


def bookRoom(availableRoom):
    # print('bookRoom函数',available_rooms)
    if "7981ade524bd4b1ab92d3a622fb0d3af" in availableRoom:
        Room = "7981ade524bd4b1ab92d3a622fb0d3af"
    else:
        Room = random.choice(availableRoom)
        print('Room为', Room)

    # availableRoom.remove(Room)  
    # print("移除后的",availableRoom)
    bookBadminton_data = {
        "DHID": "",
        "YYRGH": "2310324009",
        "CYRS": '',
        "YYRXM": "顾仁杰",
        "LXFS": "18218196660",
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
                print("移除后的",availableRoom)
                if availableRoom:
                    bookRoom(availableRoom)  
                else:
                    print(book_day,book_time,"这个时间段已经没空场了")
                    getTimeList()
                    return False

            if "您已预约" in re.text:
                print("您已预约")
                return False
            
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False
    
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
                print(available_rooms)
                bookRoom(available_rooms)

            else:
                getOpeningRoomNumber += 1
                if getOpeningRoomNumber < 10:
                    time.sleep(0.2)
                    print('调用第',getOpeningRoomNumber,'次',book_day,"没有空场了")
                    getOpeningRoom()
                return False
        
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False

def getTimeList():
    global book_time, start_time, end_time, booked_times,getOpeningRoom_data,book_timeKS,book_timeJS,getTimeListNumber
    # print('getTimeList',getOpeningRoom_data)
    # book_time = "19:00-20:00"
    # book_timeKS = book_time.split("-")[0]
    # book_timeJS = book_time.split("-")[1]   
    # getOpeningRoom_data["KSSJ"] = book_timeKS
    # getOpeningRoom_data["JSSJ"] = book_timeJS
    # print('getTimeList',getOpeningRoom_data)
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
                if getTimeListNumber < 10:
                    time.sleep(0.2)
                    print('调用第',getTimeListNumber,'次',book_day,"没有空场了")
                    getTimeList()
                return False
                

            

        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False  

def get_login_cookies(username, password, login_url):
    session = requests.Session()

    # 这是登录表单的数据
    login_data = {
        'username': username,
        'password': password,
    }


    # 发送 POST 请求到登录 URL，带上登录表单的数据
    response = session.post(login_url, data=login_data)

    response.raise_for_status()

    print(response.text,response.content,session.cookies)

    return session.cookies

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



if __name__ == "__main__":

    # print(book_time, book_day, start_time, end_time,run_time,'\n')
    # print(cookies,'\n')
    # print(book_timeKS,book_timeJS,'\n')

    # login_url = 'https://authserver.szu.edu.cn/authserver/login?service=https://ehall.szu.edu.cn:443/qljfwapp/sys/lwSzuCgyy/index.do%23%2FsportVenue'
    # print(username, password, login_url,'\n')


    # get_login_cookies(username, password, login_url)
    runScriptTime(run_time)
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    getTimeList()
    # getOpeningRoom()