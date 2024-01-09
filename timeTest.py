import pytz
from datetime import datetime

# 用于测试当前时间是否准确
# 获取当前的北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

# 打印北京时间
print(current_time)
print(datetime.now())