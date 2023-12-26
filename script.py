import requests
import time
import datetime
import json
import random
# config = {
#     "Accept": "*/*",
#     "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "referer":"https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"
# }

accept = "*/*"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer = "https://ehall.szu.edu.cn/qljfwapp/sys/lwSzuCgyy/index.do"


CGDM = "001"
XMDM = "001"
XQWID = "1"
book_time = "09:08-10:08"
book_day = "2023-12-26"
LX = "1.0"
YYK5 = "2023-12-26 09:09"
YYJ5 = "2023-12-26 18:09"
PC_OR_PHONE = "PC"

class Reservation():
    def __init__(self, start_time, end_time, user_agent) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.user_agent = user_agent

    def post_reservation(self, config, id: int):
        url = "http://reservation.ruichengyunqin.com/api/blade-app/qywx/saveOrder?userid=" + config["student_id"]
        p_data = {

            "DHID": "",
            "YYRGH": "2310324039",
            "CYRS": "",
            "YYRXM": "顾仁杰",
            "LXFS": "18218196660",
            "CGDM": CGDM,
            "CDWID": "7d5d32e7@3c34c7@ad72aca1f02a3c28",
            "XMDM": XMDM,
            "XQWID": XQWID,
            "KYYSJD": book_time,
            "YYRQ": book_day,
            "YYLX": LX,
            "YYK5": YYK5,
            "YYJ5": YYJ5,
            "PC OR PHONE": PC_OR_PHONE,

        }
        headers = {
            "Accept": accept,
            "User-Agent": user_agent,
            "Referer": referer
        }
        try:
            re = requests.post(url, json=p_data, headers=headers)
            re.raise_for_status()
            re_data = json.loads(re.text)
            if re_data["success"]:
                print(str(id) + "号场地预定成功！", "时间：" + self.start_time + "  -  " + self.end_time)
                return True
            else:
                print(str(id) + "号场地预定失败! ", "时间：" + self.start_time + "  -  " + self.end_time,
                      " 原因：" + re_data["msg"])
                return False
        except requests.RequestException as e:
            print(f"请求错误: {e}")
            return False

    def post_single(self, config):
        ground_ids = list(config["ground_id"].keys())
        random.shuffle(ground_ids)
        for ground_id in ground_ids:
            time.sleep(1) # 可以根据需要更改间隔时间，为避免封号，请尽量使用较大间隔设定（>1s）
            if self.post_reservation(config, int(ground_id)):
                return



if __name__ == "__main__":

    reservations = [Reservation(i, j, random_user_agent) for i, j in zip(start_time, end_time)]


    # MAX_ATTEMPTS = len(start_time) * 3
    attempts = 0


    while time_difference > 0: # 超过设定时间不予预定，此处可以根据需要更改停止条件
        if time_difference > 10:
            time.sleep(5)
        else:
            time.sleep(0.1) # 可以根据需要更改间隔时间
        time_difference = (book_time - datetime.datetime.now()).total_seconds()
        print(
            "==================距离设定时间还有: %.2f (s)========================" % (time_difference))

    # while attempts < MAX_ATTEMPTS:
    for reservation in reservations:
        reservation.post_single(config)
        attempts += 1

    print("预订结束，部分场次可能未预约成功，请手动检查。")
