from flask import Flask,jsonify
import json

# json：字符串,本质是基于键值对形式的字符串；
# a = '123'
# b = '{"itcast":"python"}'

app = Flask(__name__)

@app.route('/')
def index():
    b = {"itcast":"python"}
    # 使用Flask内置的函数
    return jsonify(b)
    # 使用json模块提供的函数
    # dumps函数把字典转成json字符串
    # json_data = json.dumps(b)
    # return json_data

if __name__ == '__main__':
    app.run()