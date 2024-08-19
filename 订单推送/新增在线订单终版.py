import requests
import json
import hashlib
from main import timestamp
from main import app_id
from main import app_key
from main import host_port

# 配置信息
endpoint = "/pospal-api2/openapi/v1/orderOpenApi/addOnLineOrder"

# 添加在线订单的请求体
post_body_online = {
    "appId": app_id,  # Pospal配置的访问凭证
    "payMethod": "小程序",  # 支付方式：
    "payMethodCode": "115",  # 自定义支付code 当为自定义支付时，该字段必填通过销售单据api的 queryMyPayMethod 接口获取到的orignCode
    "customerNumber": "18974895093",  # 会员号
    "shippingFee": "15.00",  # 运费
    "packageFee": "5.00",  # 打包费
    "orderRemark": "测试订单备注",  # 订单备注
    "orderDateTime": "2024-08-19 11:00:54",  # 订单产生的时间，格式为yyyy-MM-dd HH:mm:ss
    "contactAddress": "测试地址",  # 送货地址，联系地址
    "contactName": "测试姓名",  # 联系人姓名
    "contactTel": "1360097865",  # 联系人电话
    "deliveryType": "1",  # 配送类型，默认为0-外卖单。1店内单，自助单
    "deliveryTime": "",  # 期望送达时间 格式为yyyy-MM-dd HH:mm:ss 当deliveryType=0时有效
    "skipProductStockValidation": "1",  # 是否跳过库存校验.orderSource为空: 0:会校验库存（默认） 1：不检验库存 orderSource不为空:统一不检验库存
    "reservationTime": "",  # 到店时间,预约时间，格式为yyyy-MM-dd HH:mm:ss
    "payOnLine": "1",  # 是否已经完成线上付款。若线上已付款，则设置payOnLine=1 且payMethod 只能为Wxpay或Alipay 或自定义支付方式。否则，该参数不传
    "orderSource": "openApi",  # 为openApi时，商品单价按接口的manualSellPrice计算为空时，按银豹后台设置的销售价计算
    "daySeq": "123",  # 牌号，取餐号。当orderSource=openApi时，才生效，如果不传，不会默认生成。 当orderSource!=openApi时，后台会默认生成一个
    "totalAmount": "178",  # 总金额，orderSource不为空时，totalAmount必填
    "items": [  # 商品列表
        {
            "productUid": "1000624729548948967",  # 商品在银豹系统的唯一标识
            "comment": "测试商品备注",  # 针对商品条目的备注
            "quantity": "1",  # 数量
            "manualSellPrice": "178"  # 商品单价,默认以银豹后台设置的价格为准。 只有当orderSource=openApi时，该字段才生效
        }
    ]
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
response = requests.post(host_port+endpoint, headers=headers, data=json_data_utf8)

# 处理响应
response_data = response.json()
print(json.dumps(response_data, indent=4, ensure_ascii=False))
