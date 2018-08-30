from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, TextAreaField, PasswordField, validators, StringField
from wtforms.fields import simple

app = Flask(__name__)


class LoginForm(Form):
    username = simple.StringField(label='账号', validators=[validators.DataRequired(message='请输入用户名')])
    password = simple.PasswordField(label='密码', validators=[validators.DataRequired(message='请输入密码')])


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(formdata=request.form)
    if request.method == 'POST':
        if form.username.data == form.password.data:
            return '<h1>Hello {}</h>'.format(form.username.data)
            # return redirect('https://www.baidu.com/s?wd={}'.format(form.username.data))
        else:
            if form.validate():
                print(form.data)
            else:
                print(form.errors)  #所有的错误信息
            msg = '用户名或密码不正确'
            return render_template('login2.html', msg=msg, form=form)
    return render_template('login2.html', form=form)


@app.errorhandler(404)
def error(e):
    return '<img src="static/img/timg.gif"/>'


if __name__ == '__main__':
    app.run(debug=True, port=3456)
