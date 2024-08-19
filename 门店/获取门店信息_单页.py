import requests
import json
import hashlib
from main import app_id
from main import app_key
from main import host_port
from main import timestamp
endpoint = "/pospal-api2/openapi/v1/userOpenApi/queryAllUser"


post_body = {
    "appId": app_id,
}

json_data = json.dumps(post_body, ensure_ascii=False)
content = app_key + json_data
md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
data_signature = md5_hash.upper()
post_head = {
    "User-Agent": "openApi",
    "Content-Type": "application/json; charset=utf-8",
    "accept-encoding": "gzip,deflate",
    "time-stamp": timestamp,
    "data-signature": data_signature,
}
response = requests.post(host_port + endpoint, json=post_body, headers=post_head)
response_data = response.json()
print(json.dumps(response_data, indent=4, ensure_ascii=False))
print(data_signature)
print(timestamp)
print(response)