from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, TextAreaField, PasswordField, validators, StringField
from wtforms.fields import simple

app = Flask(__name__)
# app.debug = True


# =======================simple===========================
class RegisterForm(Form):
    name = simple.StringField(label="用户名",validators=[validators.DataRequired()])
    pwd = simple.PasswordField(label="密码",validators=[
    validators.DataRequired(message="密码不为空")])


@app.route('/', methods=["GET", "POST"])
def register3():
    # if request.method == "GET":
    #     form = RegisterForm(data={'gender': 1})  # 默认是1,
    #     return render_template("register.html", form=form)
    # else:

    form = RegisterForm(formdata=request.form)
    if request.method=='POST':
        if form.validate():  # 判断是否验证成功
            print('用户提交数据通过格式验证，提交的值为：', form.data)  # 所有的正确信息
        # else:
        #     print(form.errors)  #所有的错误信息
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
