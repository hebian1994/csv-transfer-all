from flask import Flask, jsonify, request
from flask_cors import *
from typing import List, Dict, Any
import sqlite3
import json

from entities import UploadReq, ColTransfer, ColRename, Template

app = Flask(__name__)
CORS(app)


# 定义一个装饰器来拦截请求
def log_request_params(func):
    def wrapper(*args, **kwargs):
        # 打印请求方法和路径
        print(f"Request: {request.method} {request.path}")

        # 打印请求的参数
        if request.method == 'GET':
            print(f"Query Params: {request.args}")
        elif request.method == 'POST':
            print(f"JSON Data: {request.get_json()}")
            print(f"Form Data: {request.form}")

        # 调用原始的视图函数
        return func(*args, **kwargs)

    # 更新装饰器的__name__属性，以便Flask在日志和错误处理中使用
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/api/data', methods=['GET'])
@log_request_params
def get_data():
    return jsonify({"data": "Hello, Vue + ElementUI!"})


@app.route('/api/template/create', methods=['POST'])
@log_request_params
def template_create():
    # 获取请求体中的JSON数据
    data_dict: Dict = request.get_json()

    data_dict = data_dict['data']

    col_transfer_objs = [ColTransfer.from_dict(ct) for ct in data_dict['colTransfer']]
    col_rename_objs = [ColRename.from_dict(cr) for cr in data_dict['colRename']]
    data_obj = Template(
        data_dict['templateName'],
        data_dict['headerLineNum'],
        data_dict['rowDelFromHead'],
        data_dict['rowDelFromTail'],
        data_dict['colDeleted'],
        col_transfer_objs,
        col_rename_objs
    )

    # 将对象转换为JSON字符串
    json_str = json.dumps(data_dict)

    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("INSERT INTO template (t_name, json_config) VALUES (?, ?)", (data_dict['templateName'], json_str))
    conn.commit()

    c.execute("SELECT * FROM template")
    records = c.fetchall()
    for record in records:
        print(record)
    conn.close()
    return jsonify({"data": "OK"})


@app.route('/api/template/list-all', methods=['GET'])
@log_request_params
def template_list_all():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM template")
    records = c.fetchall()

    json_records = []

    # 遍历查询到的记录，并将每条记录转换为字典
    for record in records:
        json_record = {
            'id': record[0],
            't_name': record[1],
            'json_config': record[2]
        }
        json_records.append(json_record)

    # 关闭数据库连接
    conn.close()

    # 使用Flask的jsonify函数将列表转换为JSON响应
    return jsonify({"data": json_records})


@app.route('/api/template/delete', methods=['POST'])
@log_request_params
def template_delete_one():
    data_dict: Dict = request.get_json()

    template_id = data_dict['id']

    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("DELETE FROM template WHERE id= ?", (template_id,))
    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()

    # 使用Flask的jsonify函数将列表转换为JSON响应
    return jsonify({"data": 'OK'})


@app.route('/api/uploadFile', methods=['POST'])
@log_request_params
def upload():
    # 获取请求体中的JSON数据
    request_body: Dict = request.get_json()

    # 将字典数据转换为MyData对象
    my_data = UploadReq(request_body['data'])
    template_id = UploadReq(request_body['templateId'])

    # TODO use the template to convert the file

    return jsonify({"data": "OK"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
