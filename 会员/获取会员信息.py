import requests
import json
import hashlib
import pandas
from main import app_id
from main import app_key
from main import host_port
from main import timestamp
endpoint = "/pospal-api2/openapi/v1/customerOpenApi/queryCustomerPages"
# 定义data-signature


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
    response = requests.post(host_port + endpoint, headers=headers, data=json_data)

    # 处理响应
    response_data = response.json()
    return response_data

def get_member_infor():
    postBackParameter = None
    while True:
        response_data = fetch_page(postBackParameter)

        # 打印响应结果
        # print(json.dumps(response_data, indent=4, ensure_ascii=False))
        data_member = response_data.get("data", {})
        data_member2 = data_member.get("result", [])
        df = pandas.json_normalize(data_member2, record_prefix='result')
        df.to_csv(path_or_buf='../member_infor_{i}.csv', mode='a', index=False)

        if response_data["status"].lower() != "success":
            print("Error occurred:", response_data.get("messages"))
            return response_data
            break

        data = response_data.get("data", {})
        resultm = data.get("result", [])
        # 检查是否有下一页数据
        if len(resultm) < data.get("pageSize", 0):
            print("Reached the last page.")
            return response_data
            break
        # 更新postBackParameter
        postBackParameter = data.get("postBackParameter", None)
        if not postBackParameter:
            print("No postBackParameter found, stopping.")
            break


result_member = get_member_infor()
# data_member = result_member.get("data", [])
# print(json.dumps(result_member, indent=4, ensure_ascii=False))
# df = pandas.json_normalize(results, record_path='result')
# df.to_csv("data.csv", index=False)
# df.to_excel('data.xlsx', index=False)

