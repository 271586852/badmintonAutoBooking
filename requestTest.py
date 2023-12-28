import requests
import json
import requests

def get_login_cookies(username, password, login_url):
    session = requests.Session()

    # 这是登录表单的数据
    login_data = {
        'username': username,
        'password': password,
    }

    # 发送 POST 请求到登录 URL，带上登录表单的数据
    response = session.post(login_url, data=login_data)

    # 检查响应状态码，如果不是 200，那么抛出异常
    response.raise_for_status()

    # 返回 session 对象的 cookies
    return session.cookies

p_data_football = {
    "DHID": "",
    "YYRGH": "2310324009",
    "CYRS": 1,
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    "CGDM": "007",
    "CDWID": "9a286792d4e24186a3663727906b5f27",
    "XMDM": "002",
    "XQWID": 1,
    "KYYSJD": "09:00-10:00",
    "YYRQ": "2023-12-27",
    "YYLX": 2.0,
    "YYKS": "2023-12-27 09:00",
    "YYJS": "2023-12-27 10:00",
    "PC_OR_PHONE": "pc"
}

p_data_badminton = {
    "DHID": "",
    "YYRGH": "2310324009",
    "CYRS": "",
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    "CGDM": "001",
    "CDWID": "17f8d1dd7a8446b0aece40f81f87981c",
    "XMDM": "001",
    "XQWID": 1,
    "KYYSJD": "18:00-19:00",
    "YYRQ": "2023-12-29",
    "YYLX": 1.0,
    "YYKS": "2023-12-29 18:00",
    "YYJS": "2023-12-29 19:00",
    "PC_OR_PHONE": "pc"
}

getTimeList_data = {
    "XQ": 1,
    "YYRQ": "2023-12-27",
    "YYLX": 2.0,
    "XMDM": "002"
}

accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

urlgetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer }

cookie_str = 'EMAP_LANG=zh; _WEU=fACp0H5UvYIPFkjmWSDYoSYcgRwqsk*tRoZCaCzxOrr059uAOlNM6NTfamM3B2QC3M9bckwqrar4iwvbP1XSlOtjnsf08Ea5*KomPyOOeBY36qkBZ6nYXSqAiL0q0r2SnMJM5xfU0rgtU7t7SnqAWnul7OKOVa0s3KcStH0FUmQHBgmuh*r4pqcAvv0v4ikU; amp.locale=undefined; JSESSIONID=UHNid30IqXoA2tjXS8lI-TRNeMAtyb7Tv7oBEB8ZkuFBajcMyPEe!1678420362; MOD_AUTH_CAS=MOD_AUTH_ST-1072598-geTPP3Ljdo2UXVcTMv4V1703605658472-4aun-cas; asessionid=7b7db49b-6b4a-435a-9917-a565aba08c43; route=cb53dd1ffa5940bf740b34afe353a0ed'

cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ")}

print(cookies)

def bookTest():

    try:
            re = requests.post(url, data=p_data, headers=headers,cookies=cookies)
            re.raise_for_status()
            try:
                re_data = json.loads(re.text)
            except json.JSONDecodeError:
                print("无效的 JSON 数据: ", re.text)
                return False
            re_data = json.loads(re.text)
           
            if re_data["success"]:
                print("场地预定成功！")
                return True
            else:
                print("场地预定失败! ", "时间：" , " 原因：" + re_data["msg"])
                return False
    except requests.RequestException as e:
            print(f"请求错误: {e}")
            return False
    
def getTimeList():
    try:
        re = requests.post(urlgetTimeList,data = getTimeList_data,headers=headers,cookies=cookies)
        print(headers, cookies)
        re.raise_for_status()
        try:
            re_data = json.loads(re.text)
            print(re_data)
            print ('re.cookies:',re.cookies)
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False    


if __name__ == "__main__":
    # bookTest()
    getTimeList()