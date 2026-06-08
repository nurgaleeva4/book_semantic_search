from flask import Blueprint, render_template, session, redirect, url_for, flash
import httpx
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def history():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    with httpx.Client() as client:
        response = client.get(f"{FASTAPI_URL}/recommendations/history", headers=headers)

    if response.status_code == 200:
        data = response.json()
        recommendations = data.get("recommendations", [])
        return render_template("history.html", recommendations=recommendations)
    else:
        flash("Could not fetch history", "warning")
        return render_template("history.html", recommendations=[])