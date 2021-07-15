from flask import Flask, request, render_template, url_for, redirect, json, jsonify, session, Response, flash
from app.forms.public import InputForm, ConnexionForm
from functools import wraps
from uuid import uuid4
import app.utils as utils
from app import app, bdd, users
from app import userCharts, groupesCharts

def isLogged(f):
    @wraps(f)
    def logWrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login")) 
    return logWrapper


@app.route('/', methods=['GET', 'POST'])
def index():

        if "user" in session: #Afficher la page de connexion si l'utilisateur n'est pas connecté
            form = InputForm() #Recuperation des saisies de l'utilisateur
            rappel = None
            if request.method == 'POST' and form.submit.data == True:

                

                if form.users.data: #Si l'utilisateur saisie des informations dans l'input(user), alors on comprend qu'il veut les informations de l'utilisateur

                    if form.users.data in users and len(form.users.data.split()) <= 1:
                        output, rappel, errRet = userCharts.charts(form)
                        if errRet:
                            flash("Merci de verifier votre demande d'information", category="danger")
                        else:
                            return render_template('index.html', charts=output, form=form, user=form.users.data, group=form.groups.data, infos=rappel)
                    else:
                        flash("Aucun(e) utilisateur/trice est associé(e) à votre entrée", category="warning")
                elif form.groups.data != "Tout" and not form.users.data:
                    print("groupe")
                elif form.queue.data != "Tout" and not form.users.data:
                    print("queue")
                elif form.cluster.data != "default" and not form.users.data:
                    print("cluster")
                    
            elif request.method == 'POST' and form.reset.data == True:
                LoadGroupes(session["user"], reload=True)
                return redirect(url_for("index"))
            
            return render_template('index.html', charts=None, form=form, user=form.users.data, group=form.groups.data, infos=rappel) #Afficher une page blanche, ou avec des erreurs et informations
        else:
            return redirect(url_for("login")) #redirection

@app.route("/login", methods=["POST", "GET"])
def login():
    form = ConnexionForm() #Recuperation des saisies de l'utilisateur

    if request.method == 'POST' and form.submit.data == True:
        session.permanent = True
        session["user"] = str(uuid4()) #Génération d'un uuid, le manque de chance pour que deux utilisateurs aient le meme nom :p
        return redirect(url_for("login"))
    else:
        #Redirection à la page index si la variable user existe
        if "user" in session:
            return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """
        Fonction logout, la variable session["user"] est supprimée
    """
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/who')
@isLogged
def who():
    #Qui es-tu?
    #Format json
    return jsonify(user=session["user"])

@app.route('/output/<name>', methods=['GET', 'POST'])
@isLogged
def LoadGroupes(name=None, reload=False):
    """
        output/<name> utilisé pour les groupes, lorsque l'utilisateur se sert de l'input(user), chaque frappe est ramenée ici, 
        dans le variable text si un utilisateur connu de la bdd est égal au text alors on va chercher à quel groupe il appartient
        -js: utilisation de la liste groupe pour les afficher dans le select (voir static/js/front.js:loadUsersGroupe et ready)
    """
    text = request.args.get('outData') #receive data from the /output page
        
    if text in users:
        groupName = bdd.findGroupByUser(text)
        session["saveGroupe"] = [t for t in groupName["group_name"]]
    elif text == "":
        groupes = bdd.listGroupes()
        session["saveGroupe"] = [t for t in groupes["group_name"]]

    if reload:
        groupes = bdd.listGroupes()
        session["saveGroupe"] = [t for t in groupes["group_name"]]
    try:
        return jsonify(groupes=session["saveGroupe"])
    except KeyError:
        groupes = bdd.listGroupes()  # Il vaut mieux retourner la liste complete à chaque fois pour eviter tout bug
        session["saveGroupe"] = [t for t in groupes["group_name"]]
        return jsonify(groupes=session["saveGroupe"])