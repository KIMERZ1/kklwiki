from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models.user import User
from app.blueprints.auth.forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("wiki.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data):
            flash("이미 존재하는 아이디입니다.")
            return render_template("auth/register.html", form=form)

        user = User.create(form.username.data, form.password.data)
        login_user(user)
        return redirect(url_for("wiki.index"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("wiki.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)

        if user is None or not user.check_password(form.password.data):
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
            return render_template("auth/login.html", form=form)

        if user.is_banned:
            flash("차단된 계정입니다.")
            return render_template("auth/login.html", form=form)

        login_user(user)

        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("wiki.index"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("wiki.index"))
