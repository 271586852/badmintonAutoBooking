import datetime
import requests
import json
import time
from pprint import pprint
import random


# cookie_str从浏览器中获取
cookie_str = 'EMAP_LANG=zh; _WEU=rlffOeXK6MyHl80IVZUQvCp_4yGJvwiC4xa9Q_MAGax6EtHXDwB4nEpdVaqFXw11gEc5teqhGXhgTC0dH45WXnmUoOBPJ9SfSE*O0hR7acGt19uqnxQtb6gsp7jwkHwb1aosbjHWxxuXxFlEeRCwLvXxn8LVJIPS1Vc52q2MDdN4pQfzSTUR*cKhXvXmYvyf; route=4c37e2ddc40281383dbb747bc4412a28; MOD_AUTH_CAS=MOD_AUTH_ST-1241579-rhHe5mbMJ2GLqitqBiMt1704343510122-4aun-cas'
book_time = "17:00-18:00"
book_day = "2024-01-05"
run_time = "12:30:01"

available_rooms = []  # Store the WID of available rooms
booked_times = []  # Store the fully booked times




cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ") if "=" in item}

# cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ")}
start_time = book_day + " " + book_time.split("-")[0]
end_time = book_day + " " + book_time.split("-")[1]
book_timeKS = book_time.split("-")[0]
book_timeJS = book_time.split("-")[1]

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


def getOpeningRoom():
    global available_rooms
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
        except requests.RequestException as e:
            print(f"请求错误: {e}")
    except requests.RequestException as e:
            print(f"请求错误: {e}")
            return False
    
if __name__ == "__main__":

    print(book_time, book_day, start_time, end_time,run_time,'\n')
    print(cookies,'\n')
    print(book_timeKS,book_timeJS,'\n')

    # login_url = 'https://authserver.szu.edu.cn/authserver/login?service=https://ehall.szu.edu.cn:443/qljfwapp/sys/lwSzuCgyy/index.do%23%2FsportVenue'
    # print(username, password, login_url,'\n')


    # get_login_cookies(username, password, login_url)
    # runScriptTime(run_time)
    # bookRoom("7981ade524bd4b1ab92d3a622fb0d3af")
    # getTimeList()
    getOpeningRoom()
 