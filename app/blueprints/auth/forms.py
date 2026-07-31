from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = StringField("아이디", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("비밀번호", validators=[DataRequired(), Length(min=8)])


class LoginForm(FlaskForm):
    username = StringField("아이디", validators=[DataRequired()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
