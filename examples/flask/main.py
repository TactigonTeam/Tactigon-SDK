from functools import wraps
from flask import Blueprint, render_template, flash, redirect, url_for, current_app

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET"])
@bp.route("/hand/<string:hand>", methods=["GET"])
def index(hand: str = "right"):
    return render_template(
        "main/index.jinja", 
        hand=hand,
        tskin_right=current_app.extensions["tskin_right"],
        tskin_left=current_app.extensions["tskin_left"],
        )

@bp.route("/disconnect", methods=["GET"])
def disconnect():

    if current_app.extensions["tskin_left"] is not None:
        current_app.extensions["tskin_left"].terminate()

    if current_app.extensions["tskin_right"] is not None:
        current_app.extensions["tskin_right"].terminate()

    flash("TSkin disconnected...", "info")
    return redirect(url_for("main.index"))