from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.web.forms import RegistrationForm, LoginForm
import httpx
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with httpx.Client() as client:
            response = client.post(
                f"{FASTAPI_URL}/register",
                json={
                    "username": form.username.data,
                    "password": form.password.data
                }
            )
            if response.status_code == 200:
                flash("Registration successful! Please login.", "success")
                return redirect(url_for("auth.login"))
            else:
                flash("Registration failed. Username may already exist.", "danger")
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with httpx.Client() as client:
            response = client.post(
                f"{FASTAPI_URL}/login",
                json={
                    "username": form.username.data,
                    "password": form.password.data
                }
            )
            if response.status_code == 200:
                data = response.json()
                session["access_token"] = data["access_token"]
                session["username"] = form.username.data
                flash(f"Welcome back, {form.username.data}!", "success")
                return redirect(url_for("main.index"))
            else:
                flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))