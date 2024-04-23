import pytz
from datetime import datetime
import time
from dateutil import tz

# start_time = "16:00:00"  # 设置开始时间

#  # 获取当前的北京时间
# beijing_tz = pytz.timezone('Asia/Shanghai')
# current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

# # 打印北京时间
# print('current_time',current_time)

# if current_time >= start_time:
#     print("已经过了指定的开始时间。", datetime.now(beijing_tz).strftime("%H:%M:%S"))
    

# start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
# current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
# remaining_seconds = start_time_seconds - current_time_seconds

# print(f"距离 {start_time} 的剩余时间：{remaining_seconds} 秒")

# while remaining_seconds > 0:
#     print(f"当前时间", datetime.now(beijing_tz).strftime("%H:%M:%S"))
#     print(f"剩余时间：{remaining_seconds} 秒", end="\r")
#     time.sleep(1)
#     remaining_seconds -= 1

# print("开始运行程序！", datetime.now(beijing_tz).strftime("%H:%M:%S"), '\n')

import ntplib
from datetime import datetime, timedelta, timezone

def get_network_beijing_time_formatted(server='pool.ntp.org'):
    try:
        client = ntplib.NTPClient()
        tryNumber = 0

        for _ in range(5):
            try:
                response = client.request(server, version=3)
                utc_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
                beijing_time = utc_time + timedelta(hours=8)
                # Format the datetime object to only show time
                return beijing_time.strftime('%H:%M:%S')
            except Exception as e:
                time.sleep(1)  # Pause for 1 second before retrying
                tryNumber += 1
                print(f"获取网络时间失败，重试第{tryNumber}次")
        # If failed to get network time after 10 attempts, return current Beijing time
        beijing_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        return beijing_time.strftime('%H:%M:%S')
    except Exception as e:
        return f"获取网络时间失败，使用本机时间: {e}"
    
for i in range(100):
    print(get_network_beijing_time_formatted())
    time.sleep(1)

