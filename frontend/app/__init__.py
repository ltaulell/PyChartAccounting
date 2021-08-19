from flask import Flask

from app.service.userCharts import userCharts
from app.service.groupsCharts import groupsCharts
from app.service.queuesCharts import queuesCharts
from app.service.clustersCharts import clusterCharts
from app.service.defaultCharts import defaultCharts

from app.service.bddTransaction import BddTransaction

bdd = BddTransaction("config/infodb.ini") #Initialisation base de données
userCharts = userCharts(bdd) #Initialisation des graphiques
groupsCharts = groupsCharts(bdd) #Initialisation des graphiques
queuesCharts = queuesCharts(bdd) #Initialisation des graphiques
clusterCharts = clusterCharts(bdd) #Initialisation des graphiques
defaultCharts = defaultCharts(bdd) #Initialisation des graphiques

users = [t for t in bdd.listUser()["login"]] #Chargement des utilisateurs

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


from app import views
from app import viewsBack
from app import errors_handlers