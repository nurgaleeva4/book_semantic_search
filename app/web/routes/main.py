from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.web.forms import RecommendForm
import httpx
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))

    form = RecommendForm()
    recommendations = None

    if form.validate_on_submit():
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        with httpx.Client() as client:
            response = client.post(
                f"{FASTAPI_URL}/recommend",
                json={"text": form.text.data},
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommendations", [])
            else:
                flash("Recommendation failed. Please try again.", "danger")

    return render_template("index.html", form=form, recommendations=recommendations)