import datetime
import requests
import json
import time
from pprint import pprint
import random
import pytz
from datetime import datetime


# 获取当前的北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.now(beijing_tz).strftime("%H:%M:%S")

# 打印北京时间
print(current_time)
print(datetime.now())