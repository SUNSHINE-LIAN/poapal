import requests
import json
import hashlib
import time

# 配置信息
app_id = "72824C420E4098EF7946F96FD527D0D9"
app_key = "539458215541579163"
api_url = "https://area64-win.pospal.cn:443/pospal-api2/openapi/v1/userOpenApi/queryAllUser"

# 生成当前时间戳
timestamp = str(int(time.time() * 1000))

# 生成data-signature
def generate_data_signature(app_key, json_data):
    content = app_key + json_data
    md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    return md5_hash.upper()

# 设置请求头
def get_headers(data_signature, timestamp):
    return {
        "User-Agent": "openApi",
        "Content-Type": "application/json; charset=utf-8",
        "accept-encoding": "gzip,deflate",
        "time-stamp": timestamp,
        "data-signature": data_signature,
    }

def fetch_page(postBackParameter=None):
    # 构造请求体
    request_body = {
        "appId": app_id,
    }

    if postBackParameter:
        request_body["postBackParameter"] = postBackParameter

    # 将请求体转换为JSON字符串
    json_data = json.dumps(request_body, ensure_ascii=False)

    # 生成data-signature
    data_signature = generate_data_signature(app_key, json_data)

    # 设置请求头
    headers = get_headers(data_signature, timestamp)

    # 发送HTTP POST请求
    response = requests.post(api_url, headers=headers, data=json_data)

    # 处理响应
    response_data = response.json()
    return response_data

def AllUser():
    postBackParameter = None
    while True:
        response_data = fetch_page(postBackParameter)

        # 打印响应结果
        print(json.dumps(response_data, indent=4, ensure_ascii=False))

        if response_data["status"].lower() != "success":
            print("Error occurred:", response_data.get("messages"))
            break

        data = response_data.get("data", {})
        result = data.get("result", [])

        # 检查是否有下一页数据
        if len(result) < data.get("pageSize", 0):
            print("Reached the last page.")
            break

        # 更新postBackParameter
        postBackParameter = data.get("postBackParameter", None)
        if not postBackParameter:
            print("No postBackParameter found, stopping.")
            break

result = AllUser()
print(result)