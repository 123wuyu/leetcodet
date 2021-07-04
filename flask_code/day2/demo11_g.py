from flask import Flask,g,current_app,session,request

app = Flask(__name__)


def db_query():
    # 从g对象中取出数据
    user_id = g.user_id
    user_name = g.user_name
    print('user_id={},user_name={}'.format(user_id,user_name))

@app.route('/')
def index():
    # 用g对象来临时存储数据
    # g.user_id = request.args.get('user_id')
    g.user_id = 2019
    g.user_name = 'python42'
    db_query()
    return 'hello world'

if __name__ == '__main__':
    app.run()