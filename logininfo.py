from flask import Flask, request, render_template, redirect, flash,session
from wtforms import Form, TextAreaField, PasswordField, validators, StringField
from wtforms.fields import simple

app = Flask(__name__)
app.secret_key='10170724'

class LoginForm(Form):
    username = simple.StringField(label='账号', validators=[validators.DataRequired(message='请输入用户名')])
    password = simple.PasswordField(label='密码', validators=[validators.DataRequired(message='请输入密码')])

@app.route('/')
def main():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(formdata=request.form)
    if request.method == 'POST' and form.validate():
        session['username']=form.username.data
        session['password']=form.password.data
        if form.username.data == form.password.data:
            return redirect('/user')
            # return '<h1>Hello {}</h>'.format(form.username.data)
            # return redirect('https://www.baidu.com/s?wd={}'.format(form.username.data))
        else:
            msg = '用户名或密码不正确'
            return render_template('login2.html', msg=msg, form=form)
    return render_template('login2.html', form=form)

@app.route('/user')
def user():
    if session.get('username'):
        return 'Hello {}'.format(session.get('username'))
    return redirect('/')

@app.errorhandler(404)
def error(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True, port=3455)
