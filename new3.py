from flask import Flask,request,render_template,redirect

app = Flask(__name__)
#绑定访问地址127.0.0.1:5000/user
@app.route("/",methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        if username =="user" and password=="password":
            return redirect("http://www.baidu.com")
        else:
            message = "Failed Login"
            return render_template('log.html',msg=message)
    return render_template('log.html')

if __name__ == '__main__':
    app.run(debug=True,port=8888)