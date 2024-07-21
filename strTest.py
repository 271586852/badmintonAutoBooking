import requests

# 测试 URL，可以选择上述任何一个 URL
test_url = "https://jsonplaceholder.typicode.com/todos/1"

try:
    response = requests.get(test_url, stream=True, verify=False)
    if response.status_code == 200:
        print("成功获取数据：")
        print(response.text)
    else:
        print(f"请求失败，状态码：{response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"请求出现异常：{e}")
