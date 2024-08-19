import requests
import json
import hashlib
from main import timestamp
from main import app_id
from main import app_key

# 配置信息
baseurl = "http://localhost:8080"
endpoint = "/pospal-api2/openapi/v1/orderOpenApi/completeOrder"
orderno = "24082001510762414104"
# 添加在线订单的请求体
post_body_online = {
    "appId": app_id,
    "orderNo": orderno,
    "shouldAddTicket": "true"
}
# 将请求体转换为JSON字符串
json_data = json.dumps(post_body_online, ensure_ascii=False)
# 生成data-signature
content = app_key + json_data
md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
data_signature = md5_hash.upper()
# 设置请求头
headers = {
    "User-Agent": "openApi",
    "Content-Type": "application/json; charset=utf-8",
    "accept-encoding": "gzip,deflate",
    "time-stamp": timestamp,
    "data-signature": data_signature,
}
# 将请求体转换为UTF-8编码
json_data_utf8 = json_data.encode('utf-8')
# 发送HTTP POST请求
response = requests.post(baseurl+endpoint, headers=headers, data=json_data_utf8)
# 处理响应
response_data = response.json()
print(json.dumps(response_data, indent=4, ensure_ascii=False))


