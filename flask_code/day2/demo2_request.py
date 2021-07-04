from flask import Flask,request,current_app
# 获取请求信息

app = Flask(__name__)

# request对象的常用属性：
# http://127.0.0.1:5000/?mobile=123234234
@app.route('/',methods=['POST','GET'])
def index():
    # request.args['key']
    # 查询字符串args
    # mobile = request.args.get("mobile")
    # return 'hello world {}'.format(mobile)
    # 表单参数form
    # user = request.form.get('user')
    # pswd = request.form.get('pswd')
    # print('user={},pswd={}'.format(user,pswd))
    # 其它请求信息method/url/headers
    print(request.method)
    print(request.url)
    print('='*50)
    print(request.headers)
    print('='*50)
    return 'hello world'

# 获取文件信息
@app.route('/image',methods=['POST'])
def save_image():
    image = request.files.get('image')
    print('image={}'.format(image))
    # with open('666.jpg','wb') as f:
    #     f.write(image.read())
    image.save('./666.jpg')

    return 'save image success'


if __name__ == '__main__':
    print(app.url_map)
    app.run()