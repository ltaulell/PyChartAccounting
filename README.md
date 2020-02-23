# PyChartSGE

Status : Draft. Early Work in Progress.

TL;DR: Une copie +/- simplifiée de [S-GAE2](https://rdlab.cs.upc.edu/s-gae/) 
(from rdlab, Barcelona University). Analyse, à froid (disconnected), du fichier
d'accounting SGE.


## Cahier des charges

Proposer un outil d'analyse 'graphique' (charts) aux admins et utilisateurs de
nos clusters. Multiples possibilités de filtres. Inspiré de S-GAE2.

### Frontend

Web (python). No authentication. Select, display.


### Charts

Piecharts, plotted dots, barcharts...

* Par année civile, ou par période (date de début, date de fin) :
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time

* par utilisateur (login), groupe, métagroupe (groupe de groupes) :
    * nb de jobs
    * durées (min, max, med, moy)
    * cpu vs système (I/O ? ratio % ?)
    * ram (min, max, med, moy)
    * job execution time
    * job queued time

* par cluster(s), file(s) d'attentes, nodes :
    * nb de jobs
    * durées (min, max, med, moy)
    * cpu vs système (I/O ? ratio % ?)
    * ram (min, max, med, moy)
    * job execution time
    * job queued time

* Top 10 : (les + utilisés)
    * users
    * métagroups

* Inverted Top 10 : (les - utilisés)
    * queue(s)
    * node(s)

* Autres :
    * par projets (SGE projects ou groupes)
    * Queue slots-per-job usage (nb de slots/job)


### Backend

Python3. Une partie du taff est déjà fait dans parse_accounting.py 
(voir [SGE toolbox](https://github.com/ltaulell/sge_toolbox)).

Voir aussi les outils d'analyse de log. Malgré sa structure chelou,
l'accounting EST un fichier de log.

### Glossaire

* accounting file : /var/lib/gridengine/default/common/accounting (fichier cumulatif)

* qacct : Utilitaire SGE d'interrogation du fichier d'accounting

* métagroupe : groupe regroupant plusieurs disciplines aux usages comparables :
    - chimistes, astro-chimistes, géo-chimistes,
    - physiciens, astro-physiciens, géo-physiciens, bio-physiciens,
    - mécaflu, multiphysique, thermie/acoustique,
    - workflow génomiques (fonctionnelle, cellulaire, plantes, virus/bactéries),
    - HeeYa!^W, apprentissage(s) profond, accélération GPU,
    - etc.
