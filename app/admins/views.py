from flask import Blueprint, render_template

from app.users.decorators import admin_required

blueprint = Blueprint("admins", __name__, url_prefix="/admin")


@blueprint.route("/")
@admin_required
def admin_index():
    return render_template("admin/index.html")
