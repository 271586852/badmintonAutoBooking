import datetime
import requests
import json
import time
from pprint import pprint
import random


# 设置下列四个参数,然后运行脚本即可
# 必须设置的参数如下
# 1 cookies参数
# 2 订场时间 例子："19:00-20:00"
# 3 订场日期 例子："2024-01-03"
# 4 运行时间 例子："12:30:01"

# cookie_str从浏览器中获取
cookie_str = 'EMAP_LANG=zh; _WEU=Ixdoi6qoAzxx3v5QQu__WRu7m*7fJJgbwSjz7amuTlNAKR7II3pRnCo9SSeKVnBXEii8R2Pk1xWVhNT4vknqUq8MR_mheh7eB6GUaGQkSzG7GalPdRDZ7EU8EsSXAP2htYqUxCVYlCuZ3ahKv3HehqlMnrkA0FqVCaLqTp8qoMEnad3pLI6go0RQJGpCWAFCxAWkHjOjDg9GbGaw3pjgzo..; route=4c37e2ddc40281383dbb747bc4412a28; MOD_AUTH_CAS=MOD_AUTH_ST-1256648-fb95IsmzhjIKalucfwse1704357032188-4aun-cas'
book_time = "12:00-13:00"
book_day = "2024-01-05"
run_time = "12:30:01"




available_rooms = []  # Store the WID of available rooms
booked_times = []  # Store the fully booked times



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
    print('bookRoom函数',available_rooms)
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
            print(re_data)
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
    global available_rooms
    print('getOpeningRoom',getOpeningRoom_data)
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
                # bookRoom(available_rooms)

            # else:
            #     for _ in range(15):
            #         time.sleep(0.3)
            #         getOpeningRoom()
        
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False

def getTimeList():
    global book_time, start_time, end_time, booked_times,getOpeningRoom_data,book_timeKS,book_timeJS
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
                    else:
                        book_time = booked_times[0]

                book_timeKS = book_time.split("-")[0]
                book_timeJS = book_time.split("-")[1]    
                print(book_timeKS,book_timeJS,'\n')

                # book_timeKS修改后，还需要对getOpeningRoom_data中的book_timeKS进行修改
                getOpeningRoom_data["KSSJ"] = book_timeKS
                getOpeningRoom_data["JSSJ"] = book_timeJS

                print('修改后的',book_time)
                start_time = book_time.split('-')[0]
                end_time = book_time.split('-')[1]
                print('getTimeList',getOpeningRoom_data)

                getOpeningRoom()
            else:
                print(book_day,"没有空场了")
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
    current_time = time.strftime("%H:%M:%S", time.localtime())
    if current_time >= start_time:
        print("It's already past the specified start time.")
        return
    
    start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
    current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
    remaining_seconds = start_time_seconds - current_time_seconds
    
    print(f"Remaining time until {start_time}: {remaining_seconds} seconds")
    
    while remaining_seconds > 0:
        print(f"Remaining time: {remaining_seconds} seconds", end="\r")
        time.sleep(1)
        remaining_seconds -= 1
    
    print("Running the program now!")



if __name__ == "__main__":

    # print(book_time, book_day, start_time, end_time,run_time,'\n')
    # print(cookies,'\n')
    # print(book_timeKS,book_timeJS,'\n')

    # login_url = 'https://authserver.szu.edu.cn/authserver/login?service=https://ehall.szu.edu.cn:443/qljfwapp/sys/lwSzuCgyy/index.do%23%2FsportVenue'
    # print(username, password, login_url,'\n')


    # get_login_cookies(username, password, login_url)
    # runScriptTime(run_time)
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    getTimeList()
    # getOpeningRoom()