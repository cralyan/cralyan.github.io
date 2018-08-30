from flask import session,Flask,request,render_template,redirect,jsonify

app=Flask(__name__,template_folder='templates',static_path='/static/',static_url_path='/static/')
app.debug=True
app.secret_key='sjehfjeefrjewth43u'  #设置session加密
app.config['JSON_AS_ASCII']=False  #指定json编码格式 如果为False 就不使用ascii编码，
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8" #指定浏览器渲染的文件类型，和解码格式；

@app.route('/login/',methods=['GET','POST'])
def login():
    msg = ''
    if request.method=='POST':
        name=request.values.get('user')
        pwd=request.values.get('pwd')
        if name =='zhanggen' and pwd=='123.com':
            session['user']=name  #设置session的key value
            return redirect('/index/')
        else:
            msg='用户名或者密码错误'
    return render_template('login.html',msg=msg)

@app.route('/index/',methods=['GET','POST'])
def index():
    user_list = ['张根', 'egon', 'eric']
    user=session.get('user')           #获取session
    if user:
        user=['alex','egon','eric']
        return jsonify(user_list)
    else:
        return redirect('/login/')

if __name__ == '__main__':
    app.run()

