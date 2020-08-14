# -*-coding:utf-8-*- 
# author: xdz
# @Time :2019/3/26 10:51
from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, \
    ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 128),
                                    Email(message='电子邮件不符合规范')])
    password = PasswordField(validators=[
        DataRequired(message='密码为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=
                           [DataRequired(),
                            Length(2, 10, message='昵称至少需要输入两个字符最大10个')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(5, 128),
                                    Email(message='电子邮件不符合规范')])
    password = PasswordField(validators=[
        DataRequired(message='密码为空，请输入你的密码'), Length(6, 32)])


# 忘记密码
class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(5, 128),
                                    Email(message='电子邮件不符合规范')])
    pass


# 重置密码验证
class RestPasswordForm(Form):
    # EqualTo作用是比较两个变量是否相同
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要在6到32位数'),
        EqualTo('password2', message='两次输入密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])
