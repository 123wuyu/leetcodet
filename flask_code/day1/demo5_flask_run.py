from flask import Flask

app = Flask(__name__)

@app.route('/abc',methods=['POST'])
def index2019():
    print(app.url_map)
    return 'hello world'

# if __name__ == '__main__':
#     app.run()

