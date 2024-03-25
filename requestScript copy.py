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

# 14：45
cookie_str = 'EMAP_LANG=zh; _WEU=hsI00YWgHUlwCr0plETM*tG3pb1YkPt77pLtuK8LQjEdXaBzJahJnXWs8zbxDCtH6yVRPJoFU8T5aSMvUjOEA_Ayho*Zvgqr2bD1wguy57IzEKnG3hvZcc5mQ_LfaY9QdsiL_0O92V0y61_YtAooSzsZ2dm5ntvEUKl1h7p3ZlKLmLmDJa1YGDmEF3U0NqLFoO*GPv9MXEL.; XK_TOKEN=02bcffa6-5a3f-497b-9305-a0b518174649; amp.locale=undefined; JSESSIONID=VKEyval1_ojkDjX5z3tFNf8GoRt9yMsjFErKN0VJXZFMZl4GLyGd!314775203; MOD_AUTH_CAS=MOD_AUTH_ST-681086-rcPeffKbZ69ODKsqQ2VW1711340844361-dSJ7-cas; asessionid=111fc669-3ee0-4e92-b06f-4ccdde8e9f41; route=c74f3c8250d849c2cfd6230ee3f779bd'
# cookie_str = 'EMAP_LANG=zh; _WEU=MkijGTesq4L966Q**U3omvpz6x5AzwY3gzf*LcfeUMEaKRivEAI2_wEtXGaI*ZoyhPzNyxJKeLsMYqHYQqdGstvulPXsvLV3hUc8lhbETRV8FNh2BPb58s59wHKfNMl3JoQvdOddIgj5gIEAnWCjYx11ukJdCNsEae2j6liIFIxrwn_Vomf9UegMeaybUT9a; asessionid=13b3af03-4632-4101-b513-b9326e94bab5; route=f9bb7d1dbb51bc04862ec2b9cddaff48'
book_time = "21:00-22:00"
book_day = "2024-03-26"
run_time = "12:29:59"
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
        if available_rooms and bookRoomNumber<5:
            bookRoom(available_rooms)
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
            # print("无效的 JSON 数据: ", re.text)
            if "忘记密码" in re.text:
                print("Error: 请重新获取cookie")
            return False
 
    except requests.RequestException as e:
        error_message = str(e)
        print(f"请求错误: {error_message}")
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

def startRun():
    getTimeList()
    print('运行完毕')

if __name__ == "__main__":

    # print(book_time, book_day, start_time, end_time,run_time,'\n')
    # print(cookies,'\n')
    # print(book_timeKS,book_timeJS,'\n')

    # 自动获取用户cookie，日后完善
    # get_login_cookies(username, password, login_url)

    # 设定运行时间，测试时可注释掉，可即刻运行
    runScriptTime(run_time)
    # 入口函数
    startRun()

    # 下列代码，用于测试，一般情况下注释下面的代码
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    # getTimeList()
    # getOpeningRoom()