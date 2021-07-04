from flask import Flask,session
# session的设置和获取
app = Flask(__name__)
app.config['SECRET_KEY'] = '2019'

# 设置session
@app.route('/set')
def index():
    # session信息的设置
    session['itcast'] = 'python42'
    return 'hello world'

# 获取session
@app.route('/get')
def get_session():
    # session信息的设置
    itcast = session.get('itcast')
    return itcast

if __name__ == '__main__':
    app.run(debug=True)