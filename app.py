from flask import Flask, render_template, Response, request
import requests
import json
import os
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sample')
def sample():
    return render_template("apiInstance.html")


@app.route('/api', methods=['POST'])
def api():
    js_data = request.get_data()
    data = json.loads(js_data)
    url = data.get("url")
    payload = data.get("payload")
    headers = data.get("headers")
    method = data.get("method")
    headers = headers if headers else {}
    payload = payload if payload else {}
    if method.upper() == "GET":
        r = requests.get(url, params=payload, headers=headers)
        return Response(r)
    elif method.upper() == "POST":
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        return Response(r)
    elif method.upper() == "PUT":
        r = requests.put(url, data=json.dumps(payload), headers=headers)
        return Response(r)
    elif method.upper() == "DELETE":
        r = requests.delete(url, data=json.dumps(payload), headers=headers)
        return Response(r)


@app.route('/api2', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api2():
    method = request.method
    MYSQL_HOST = os.environ.get("MYSQL_HOST", None)
    MYSQL_USER = os.environ.get("MYSQL_USER", None)
    MYSQL_PORT = os.environ.get("MYSQL_PORT", None)
    MYSQL_PASS = os.environ.get("MYSQL_PASS", None)
    DB_NAME = os.environ.get("DB_NAME", None)
    if not MYSQL_HOST or not MYSQL_USER or not MYSQL_PASS or not DB_NAME:
        return json.dumps("参数不全", ensure_ascii=False)
    if method == 'GET':
        db = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, DB_NAME), echo=True)
        resultProxy = db.execute("show tables;")
        u = resultProxy.fetchall()
        resultProxy.close()
        table_name_list = []
        if len(u) > 0:
            for i in u:
                table_name_list.append(i[0])
        if 'user_info' not in table_name_list:
            sql = "CREATE TABLE `user_info` (   `ID` int(11) NOT NULL AUTO_INCREMENT,   `user_name` varchar(128),   `password` varchar(128),   PRIMARY KEY (`ID`) ) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;"
            resultProxy = db.execute(sql)
            resultProxy.close()

        sql = "select * from user_info;"
        resultProxy = db.execute(sql)
        u = resultProxy.fetchall()
        resultProxy.close()
        print(u)
        user_list = []
        if len(u) > 0:
            for i in u:
                user_list.append(i[1])
        return json.dumps(user_list, ensure_ascii=False)
    elif method == 'POST':
        data = request.data
        j_data = json.loads(data)
        user_name = j_data["user_name"]
        password = j_data["password"]
        db = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, DB_NAME), echo=True)
        resultProxy = db.execute("show tables;")
        u = resultProxy.fetchall()
        resultProxy.close()
        table_name_list = []
        if len(u) > 0:
            for i in u:
                table_name_list.append(i[0])
        if 'user_info' not in table_name_list:
            sql = "CREATE TABLE `user_info` (   `ID` int(11) NOT NULL AUTO_INCREMENT,   `user_name` varchar(128),   `password` varchar(128),   PRIMARY KEY (`ID`) ) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;"
            resultProxy = db.execute(sql)
            resultProxy.close()
        sql = "INSERT INTO `user_info` (`user_name`, `password`) VALUES('{0}', '{1}');".format(user_name, password)
        resultProxy = db.execute(sql)
        resultProxy.close()
        return json.dumps("添加成功", ensure_ascii=False)
    elif method == 'PUT':
        data = request.data
        j_data = json.loads(data)
        user_name = j_data["user_name"]
        password = j_data["password"]
        db = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, DB_NAME), echo=True)
        resultProxy = db.execute("show tables;")
        u = resultProxy.fetchall()
        resultProxy.close()
        table_name_list = []
        if len(u) > 0:
            for i in u:
                table_name_list.append(i[0])
        if 'user_info' not in table_name_list:
            sql = "CREATE TABLE `user_info` (   `ID` int(11) NOT NULL AUTO_INCREMENT,   `user_name` varchar(128),   `password` varchar(128),   PRIMARY KEY (`ID`) ) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;"
            resultProxy = db.execute(sql)
            resultProxy.close()
        sql = "select * from user_info where user_name='{0}'".format(user_name)
        resultProxy = db.execute(sql)
        u = resultProxy.fetchall()
        resultProxy.close()
        if not len(u):
            return json.dumps("用户不存在", ensure_ascii=False)
        sql = "update `user_info` set password='{0}' where user_name='{1}';".format(password, user_name)
        resultProxy = db.execute(sql)
        resultProxy.close()
        return json.dumps("修改成功", ensure_ascii=False)
    else:
        data = request.data
        j_data = json.loads(data)
        user_name = j_data["user_name"]
        db = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, DB_NAME), echo=True)
        resultProxy = db.execute("show tables;")
        u = resultProxy.fetchall()
        resultProxy.close()
        table_name_list = []
        if len(u) > 0:
            for i in u:
                table_name_list.append(i[0])
        if 'user_info' not in table_name_list:
            sql = "CREATE TABLE `user_info` (   `ID` int(11) NOT NULL AUTO_INCREMENT,   `user_name` varchar(128),   `password` varchar(128),   PRIMARY KEY (`ID`) ) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;"
            resultProxy = db.execute(sql)
            resultProxy.close()
        sql = "select * from user_info where user_name='{0}'".format(user_name)
        resultProxy = db.execute(sql)
        u = resultProxy.fetchall()
        resultProxy.close()
        if not len(u):
            return json.dumps("用户不存在", ensure_ascii=False)
        sql = "delete from user_info where user_name='{0}'".format(user_name)
        resultProxy = db.execute(sql)
        resultProxy.close()
        return json.dumps("删除成功", ensure_ascii=False)


@app.route('/mysql')
def mysql():
    MYSQL_HOST = os.environ.get("MYSQL_HOST", None)
    MYSQL_USER = os.environ.get("MYSQL_USER", None)
    MYSQL_PORT = os.environ.get("MYSQL_PORT", None)
    MYSQL_PASS = os.environ.get("MYSQL_PASS", None)
    DB_NAME = os.environ.get("DB_NAME", None)
    if not MYSQL_HOST or not MYSQL_USER or not MYSQL_PASS or not DB_NAME:
        return render_template("mysql.html", msg='参数不全')
    db = create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, DB_NAME), echo=True)
    resultProxy = db.execute("show tables;")
    u = resultProxy.fetchall()
    resultProxy.close()
    table_name_list = []
    if len(u) > 0:
        for i in u:
            table_name_list.append(i[0])
    return render_template("mysql.html", table_name_list=table_name_list, msg='数据库连接成功')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
