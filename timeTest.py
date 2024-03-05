import pytz
from datetime import datetime
import time

start_time = "16:00:00"  # 设置开始时间

 # 获取当前的北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

# 打印北京时间
print(current_time)

if current_time >= start_time:
    print("已经过了指定的开始时间。", datetime.now(beijing_tz).strftime("%H:%M:%S"))
    

start_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(":"))))
current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
remaining_seconds = start_time_seconds - current_time_seconds

print(f"距离 {start_time} 的剩余时间：{remaining_seconds} 秒")

while remaining_seconds > 0:
    print(f"当前时间", datetime.now(beijing_tz).strftime("%H:%M:%S"))
    print(f"剩余时间：{remaining_seconds} 秒", end="\r")
    time.sleep(1)
    remaining_seconds -= 1

print("开始运行程序！", datetime.now(beijing_tz).strftime("%H:%M:%S"), '\n')