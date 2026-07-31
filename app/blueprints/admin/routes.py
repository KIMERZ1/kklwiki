from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app.decorators import admin_required
from app.models.user import User

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.list_all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/ban", methods=["POST"])
@login_required
@admin_required
def ban_user(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        abort(404)

    if user.id == current_user.id:
        flash("자기 자신은 차단할 수 없습니다.")
        return redirect(url_for("admin.users"))

    user.set_banned(True)
    flash(f"{user.username}님을 차단했습니다.")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/unban", methods=["POST"])
@login_required
@admin_required
def unban_user(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        abort(404)

    user.set_banned(False)
    flash(f"{user.username}님의 차단을 해제했습니다.")
    return redirect(url_for("admin.users"))
