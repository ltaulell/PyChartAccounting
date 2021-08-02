from flask import Flask
from app.service.charts import queueCharts, userCharts, groupesCharts, queueCharts, clusterCharts
from app.service.bddTransaction import BddTransaction

bdd = BddTransaction("config/infodb.ini") #Initialisation base de données
userCharts = userCharts(bdd) #Initialisation des graphiques
groupesCharts = groupesCharts(bdd) #Initialisation des graphiques
queueCharts = queueCharts(bdd) #Initialisation des graphiques
clusterCharts = clusterCharts(bdd) #Initialisation des graphiques

users = [t for t in bdd.listUser()["login"]] #Chargement des utilisateurs

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


from app import views
from app import viewsBack
from app import errors_handlers