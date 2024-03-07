from functools import wraps
from flask import Blueprint, render_template, flash, redirect, url_for, current_app

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template(
        "main/index.jinja", 
        tskin=current_app.extensions["tskin"],
        )