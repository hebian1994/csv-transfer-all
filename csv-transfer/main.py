from flask_cors import *
from typing import List, Dict, Any
import sqlite3
import json
from flask import Flask, send_file, make_response, jsonify, request
import pandas as pd
from io import BytesIO
import re

from entities import UploadReq, ColTransfer, ColRename, Template

app = Flask(__name__)
CORS(app)


# 定义一个装饰器来拦截请求
def log_request_params(func):
    def wrapper(*args, **kwargs):
        # 打印请求方法和路径
        print(f"Request: {request.method} {request.path}")

        # 打印请求的参数
        try:
            if request.method == 'GET':
                print(f"Query Params: {request.args}")
            elif request.method == 'POST':
                print(f"JSON Data: {request.get_json()}")
                print(f"Form Data: {request.form}")
        finally:
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
    if 'file' not in request.files:
        return '没有文件部分', 400
    file = request.files['file']
    template_id = request.form['template_id']
    print(template_id)

    if file.filename.lower().endswith('.csv'):

        # TODO use the template to convert the file
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("SELECT * FROM template WHERE id = ?", (template_id,))
        record = c.fetchone()
        conn.close()
        print({"data": record[2]})

        json_str = record[2]
        data_dict = json.loads(json_str)

        template = Template(
            data_dict['templateName'],
            data_dict['headerLineNum'],
            data_dict['rowDelFromHead'],
            data_dict['rowDelFromTail'],
            data_dict['colDeleted'],
            [ColTransfer.from_dict(item) for item in data_dict['colTransfer']],
            [ColRename.from_dict(item) for item in data_dict['colRename']]
        )

        print(template.headerLineNum)
        print(template.rowDelFromHead)
        print(template.rowDelFromTail)
        # transfer 1
        # df = pd.read_csv(file, header=3,
        #                  skipfooter=6)
        df = pd.read_csv(file, header=int(template.headerLineNum),
                         skipfooter=int(template.rowDelFromTail))

        print(df)

        for item in template.colRename:
            df.rename(columns={item.nowColName: item.newColName}, inplace=True)

        for item in template.colDeleted:
            df.drop(item, axis=1, inplace=True)

        for item in template.colTransfer:
            if item.tranType == 'replace':
                match = re.search(r"Replace (\w+) with (\w+)", item.reg)
                if match:
                    x = match.group(1)
                    y = match.group(2)
                    print(f"x: {x}, y: {y}")
                    df[item.colName] = df[item.colName].replace(x, y)
                else:
                    print("No match found")

        print(df)
        csv_data = df.to_csv(index=False)

        response = make_response(csv_data)

        filename = 'after.csv'

        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["access-control-expose-headers"] = "Content-disposition"
        response.headers["Content-type"] = "text/csv"

        return response

    return jsonify({"data": 'OK'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
