import requests
import json
import requests
import json

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

    return session.cookies


# 1 cookies参数
# 2 data参数

cookie_str = 'EMAP_LANG=zh; _WEU=GYfoqszAPdqUwGiVezS7XBfTfkhZAIpPt6l5eLLMB4MMrVRCaYYa0JMKDvrBrwqu2EuUmc6QXI2NB2OElmeAmET701IIK8gwIjyOoMeUcqguWHZ7KOgMoaw*fHaPed8GD1CUA6YK1Kb94v9*pzqZ_1x1W5108Z*U6lrC89k*N5NI1PiOu89Qu3i8cu8SbJA_; amp.locale=undefined; JSESSIONID=UHNid30IqXoA2tjXS8lI-TRNeMAtyb7Tv7oBEB8ZkuFBajcMyPEe!1678420362; asessionid=7b7db49b-6b4a-435a-9917-a565aba08c43; route=cb53dd1ffa5940bf740b34afe353a0ed; MOD_AUTH_CAS=MOD_AUTH_ST-1140825-6UBsawyVFQ2CZ50vojKO1703855495074-4aun-cas'

badminton_data = {
    "DHID": "",
    "YYRGH": "2310324009",
    # "CYRS": 1,
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    # "CGDM": "007",
    # "CDWID": "9a286792d4e24186a3663727906b5f27",
    # "XMDM": "001",
    # "XQWID": 1,
    "KYYSJD": "18:00-19:00",
    "YYRQ": "2023-12-30",
    # "YYLX": 1.0,
    "YYKS": "2023-12-30 18:00",
    "YYJS": "2023-12-30 19:00",
    "PC_OR_PHONE": "pc"


}



p_data = {
    "DHID": "",
    "YYRGH": "2310324009",
    "CYRS": 1,
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    "CGDM": "007",
    "CDWID": "9a286792d4e24186a3663727906b5f27",
    "XMDM": "002",
    "XQWID": 1,
    "KYYSJD": "18:00-19:00",
    "YYRQ": "2023-12-30",
    "YYLX": 2.0,
    "YYKS": "2023-12-30 18:00",
    "YYJS": "2023-12-30 19:00",
    "PC_OR_PHONE": "pc"
}

p0_data = {
    "DHID": "",
    "YYRGH": "2310324009",
    "CYRS": 1,
    "YYRXM": "顾仁杰",
    "LXFS": "18218196660",
    "CGDM": "007",
    "CDWID": "d007d192dd634b35ba2f0f7d77b1f05e",
    "XMDM": "002",
    "XQWID": 1,
    "KYYSJD": "18:00-19:00",
    "YYRQ": "2023-12-30",
    "YYLX": 2.0,
    "YYKS": "2023-12-30 18:00",
    "YYJS": "2023-12-30 19:00",
    "PC_OR_PHONE": "pc"
}

getTimeList_data = {
    "XQ": 1,
    "YYRQ": "2023-12-29",
    "YYLX": 1.0,
    "XMDM": "001"
}

# ------------------------------
accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"

url = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/insertVenueBookingInfo.do"

urlgetTimeList = 'https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/sportVenue/getTimeList.do'

headers = { "Accept": accept, "User-Agent": user_agent, "Referer": referer }

cookies = {item.split("=")[0]: item.split("=")[1] for item in cookie_str.split("; ")}

# ------------------------------


def bookTest():

    try:
            re = requests.post(url, data=p0_data, headers=headers,cookies=cookies)
            re.raise_for_status()
            try:
                re_data = json.loads(re.text)
            except json.JSONDecodeError:
                print("无效的 JSON 数据: ", re.text)
                return False
            re_data = json.loads(re.text)
           
    except requests.RequestException as e:
            print(f"请求错误: {e}")
            return False
    
def getTimeList():
    try:
        re = requests.post(urlgetTimeList, data=getTimeList_data, headers=headers, cookies=cookies)
        print('\n','headers:', headers)
        print('\n','cookies:', cookies)
        print()
        re.raise_for_status()
        try:
            re_data = json.loads(re.text)

            for item in re_data:
                print(item)
        except json.JSONDecodeError:
            print("无效的 JSON 数据: ", re.text)
            return False
 
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return False    


if __name__ == "__main__":
    # bookTest()
    getTimeList()