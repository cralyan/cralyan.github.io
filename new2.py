from flask import Flask,redirect,request,render_template

app=Flask(__name__)
@app.route('/<name>')
def main(name):
    return "<a href='/login'>Hello,{}</a>".format(name)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user=request.form['user']
        pwd=request.form['pwd']
        print(user,pwd)
        if user == pwd and user.strip(' ')!='':
            return redirect('http://www.ecust.edu.cn')
        else:
            msg='登录失败!'
            return render_template('login.html',msg=msg)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)