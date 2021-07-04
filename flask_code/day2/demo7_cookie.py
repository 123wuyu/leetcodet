from flask import Flask,make_response,request
# cookie的操作：设置和获取
app = Flask(__name__)

# cookie设置
@app.route('/set')
def index():
    # 使用make_response生成响应信息
    resp = make_response('set cookie info')
    # 设置cookie信息，并且设置有效期，单位为秒
    resp.set_cookie('itcast','python42',max_age=60)
    return resp

# cookie获取
@app.route('/get')
def get_cookies():
    # 使用request对象，获取cookie信息
    itcast = request.cookies.get('itcast')
    return itcast

if __name__ == '__main__':
    app.run()