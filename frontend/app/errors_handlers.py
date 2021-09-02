import warnings
from app import app
from flask import redirect, url_for, render_template, flash

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.errorhandler(400)
def not_found(e):
    flash("Erreur 400 - Erreur dans la requête", category="warning")
    return redirect(url_for("index"))
