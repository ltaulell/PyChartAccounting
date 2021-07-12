import warnings
from app import app
from flask import redirect, url_for, flash


@app.errorhandler(404)
def not_found():
    flash("Erreur 404 - La page demandée est inconnu", category="warning")
    return redirect(url_for("index"))

@app.errorhandler(400)
def not_found():
    flash("Erreur 400 - Erreur dans la requête", category="warning")
    return redirect(url_for("index"))