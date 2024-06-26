import datetime
import requests
import json
import time
from pprint import pprint
import random
import pytz
from datetime import datetime

# requeset库发送请求
# getTimeList、getOpeningRoom、bookRoom三个函数分别用于获取可预约时间、获取可预约场地、预约场地
# 设置运行时间，当时间到达时，运行程序

# 设置下列参数,然后运行脚本即可
# 必须设置的参数如下
# 1 cookies参数 ----------cookie_str自行从浏览器中获取，cookie存在有效期，过期后需要重新获取，否则将预约失败--------------
# 2 订场时间 例子："19:00-20:00"
# 3 订场日期 例子："2024-01-03"
# 4 运行时间 例子："13:30:01"
# 5 学号
# 6 姓名
# 7 手机号

# ----------cookie_str自行从浏览器中获取，cookie存在有效期，过期后需要重新获取，否则将预约失败；若需要抢场，最好在当天12点左右从网站获取并更新下面的cookie--------------
cookie_str = 'EMAP_LANG=zh; _WEU=XMCRByurEmZURLfJCVhwz57S47isny65I4id*VMafy1lP9t7EnugYFwtXg4AcEAYBAFIyji1DiJA4SjLTZsqUsd_1BGtvLyWfpt6qAh5H_YZahLanJOZYFHgVvekDL0ahvic53*aaoair6X04c*f3wViEyNXLUwB9tMT4HztTdK4HUw4ax0sXUYhE8Bk3cVgLS479e2rPXQZ*9_3yTRSXH*vpyiVRyikR_qwd5J61X_DoP2sLYyy9xqs5c5LQtGQ; amp.locale=undefined; asessionid=d9d94bed-75f0-432b-a8b2-f82a3d1695cb; route=6fcc95effda7818ac250c10acfaab6fc; MOD_AUTH_CAS=MOD_AUTH_ST-1249562-cqaGWW1iFdofWHo0IBEY1713502785915-dSJ7-cas'
book_time = "21:00-22:00"
book_day = "2024-04-20"
run_time = "12:30:05"
YYRGH = "2310324009"
YYRXM = "顾仁杰"
LXFS = "18218196660"



# -----------------------下面参数勿修改-----------------------
available_rooms = []  # Store the WID of available rooms
booked_times = []  # Store the fully booked times
getTimeListNumber = 0
getOpeningRoomNumber = 0
bookRoomNumber = 0


cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}
# print(cookies)

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
    global bookRoomNumber
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
        bookRoomNumber +1
        if available_rooms and bookRoomNumber< 800:
            bookRoom(available_rooms)
        return False
    
def getOpeningRoom():
    global available_rooms,getOpeningRoomNumber
    print('打印信息getOpeningRoom',cookies,book_time,book_day,run_time,YYRGH,YYRXM,LXFS)

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
                if getOpeningRoomNumber < 800:
                    time.sleep(0.2)
                    print('调用第',getOpeningRoomNumber,'次',book_day,"没有空场了")
                    getOpeningRoom()
                return False
        
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            getOpeningRoomNumber += 1
            if getOpeningRoomNumber < 800:
                time.sleep(0.2)
                getOpeningRoom()
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        getOpeningRoomNumber += 1
        if getOpeningRoomNumber < 800:
            time.sleep(0.2)
            getOpeningRoom()
        return False
    
    print('getOpeningRoom调用结束')

def getTimeList():
    global book_time, start_time, end_time, booked_times,getOpeningRoom_data,book_timeKS,book_timeJS,getTimeListNumber
    # print('getTimeList',getOpeningRoom_data)
    # book_time = "19:00-20:00"
    # book_timeKS = book_time.split("-")[0]
    # book_timeJS = book_time.split("-")[1]   
    # getOpeningRoom_data["KSSJ"] = book_timeKS
    # getOpeningRoom_data["JSSJ"] = book_timeJS
    # print('getTimeList',getOpeningRoom_data)

    print('打印信息Gettimelist',cookies,book_time,book_day,run_time,YYRGH,YYRXM,LXFS)

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
                if getTimeListNumber < 800:
                    time.sleep(0.2)
                    print('调用第',getTimeListNumber,'次',book_day,"没有空场了")
                    getTimeList()
                return False
                
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            getTimeListNumber += 1
            if getTimeListNumber < 800:
                time.sleep(0.2)
                getTimeList()
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        getTimeListNumber += 1
        if getTimeListNumber < 800:
            time.sleep(0.2)
            getTimeList()
        return False  
    
    print('getTimeList调用结束')



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

def startRun():
    getTimeList()
    print('运行完毕')

if __name__ == "__main__":

    # print(book_time, book_day, start_time, end_time,run_time,'\n')
    # print(cookies,'\n')
    # print(book_timeKS,book_timeJS,'\n')


    # 设定运行时间，测试时可注释掉，可即刻运行
    # runScriptTime(run_time)
    # 入口函数
    # startRun()

    # 下列代码，用于测试，一般情况下注释下面的代码
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    getTimeList()
    # getOpeningRoom()