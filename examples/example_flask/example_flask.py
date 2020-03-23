# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 13:07'
from flask import Flask
from pre_request import filter_params, Rule, Length, Range

app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


fields = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty"),
    "range": Rule(direct_type=int, range=Range(10, 30)),
    "reg": Rule(reg=r'^h\w{3,5}o$', key_map="reg_exp"),
    "trim": Rule(trim=True, json=True),
    "call": Rule(direct_type=int, callback=lambda x: x+100)
}


fields2 = {
    "tot": Rule(allow_empty=True, default="hello")
}


# 不知道Methods
@app.route("/test", methods=["GET", "POST"])
@filter_params(fields)
def test_handler(params):
    return str(params)


# 单独指定GET请求过滤
@app.route("/test2", methods=["GET"])
@filter_params(get=fields)
def test2_handler(params):
    return str(params)


# 单独指定POST请求过滤
@app.route("/test3", methods=["POST"])
@filter_params(post=fields)
def test3_handler(params):
    return str(params)


# 针对GET和POST方法指定不同的判断条件
@app.route("/test4", methods=["GET", "POST"])
@filter_params(get=fields, post=fields2)
def test4_handler(params):
    return str(params)