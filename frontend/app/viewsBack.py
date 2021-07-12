from flask import Flask, request, url_for, redirect, json, jsonify, session
from app import app, bdd, users


@app.route('/users')
def LoadUsers():
    """
        Liste des utilisateurs contenu dans la bdd, pour une question d'optimisation et d'utilité, la liste est retourné sous forme json
        -js: utilisation de la liste pour de l'autocompletion (voir static/js/front.js:loadUsersGroupe)
    """
    users = bdd.listUser()
    users = [t for t in users["login"]]

    return jsonify(users=users)

@app.route('/queues')
def LoadQueues():
    """
        Liste des queues contenu dans la bdd, pour une question d'optimisation et d'utilité, la liste est retourné sous forme json
        -js: (voir static/js/front.js:loadQueues)
    """
    queues = bdd.listQueues()
    queues = [t for t in queues["queue_name"]]

    return jsonify(queues=queues)

@app.route('/clusters')
def LoadCluster():
    """
        Liste des clusters contenu dans la bdd, pour une question d'optimisation et d'utilité, la liste est retourné sous forme json
        -js: (voir static/js/front.js:loadQueues)
    """
    clusters = bdd.listClusters()
    clusters = [t for t in clusters["cluster_name"]]

    return jsonify(clusters=clusters)