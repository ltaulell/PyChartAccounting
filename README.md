# PyChartAccounting

Status : Draft. Early Work in Progress.

TL;DR: Cold analysis (disconnected) of HPC Scheduler accounting file (currently SGE).


## Cahier des charges

Proposer un outil d'analyse 'graphique' (charts) aux admins et utilisateurs de 
nos clusters. Multiples possibilités de filtres (voir § Charts). Inspiré de 
[S-GAE2](https://rdlab.cs.upc.edu/s-gae/) (from rdlab, Barcelona University).

Les fichiers d'accounting, sur plusieurs années, deviennent (trés) lourds, et 
difficile a interroger (4.4Go 2011-2017, déjà 1.2Go pour 2018-2019).

Injecter leur contenu dans un `middleware` pour triturer les data dans tous les 
sens devient pertinent.


### Frontend

* Web (et python3, for reasons),
* No authentication, at least, not related to accounting: Un DR peut regarder l'accounting de ses thésards ou de son groupe, un Correspondant doit pouvoir regarder l'accounting du/des labo(s) dont il a la charge.
* Easy to use : Select, display, Boom!.
* Fast...


### Charts

Piecharts, plotted dots, barcharts...

* Par année civile, ou par période (date de début, date de fin) :
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time

* par utilisateur, groupe, métagroupe (groupe de groupes) :
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

* Top 10 : (les + gros/utilisés)
    * utilisateurs
    * métagroups

* Inverted Top 10 : (les - utilisés)
    * queue(s)
    * node(s)

* Autres :
    * par projets (SGE projects ou groupes)
    * slots-per-job usage (nb de slots/job : séquentiel, mononode, multinode)
    * d'effroyables possibilités de mélanges...


### Backend / Middleware

Python3 (parceque je bite rien au php). Une partie du taff est déjà fait dans `parse_accounting.py` 
(voir aussi [SGE toolbox](https://github.com/ltaulell/sge_toolbox)).

Regarder aussi les outils d'analyse de log ? Malgré sa structure chelou, 
l'accounting *EST* un fichier de log. Voir `SGE_accounting_file_format.rst`.

Pandas ? (csv, delimiter=':') timeseries.

Un QueryLangage quelconque : SQL (S-GAE2 mouline tout dans du SQL) ? NoSQL ?


## Biais / Questionnements

À part les dates (*_time), rien n'est unique :

* un même $JOB_ID (job_number) peut être présent plusieurs fois dans le fichier (SGE est limité à max_jobs, et réalise une rotation)
* un même login (owner) peut être présent dans plusieurs groupes (variations sur de longues périodes)
* queue_name, hostname et appartenance d'un hostname à une ou plusieurs queue_name peuvent être déduite de l'accounting
* same pour owner et group
* SGE ne fait pas de rotation du fichier d'accounting : Un même fichier d'accounting pourra donc être parcouru plusieurs fois


### Glossaire

* SGE accounting file : /var/lib/gridengine/default/common/accounting (fichier cumulatif)

* qacct : Utilitaire SGE d'interrogation du fichier d'accounting

* métagroupe : groupe regroupant plusieurs disciplines aux usages comparables :
    - chimistes, astro-chimistes, géo-chimistes,
    - physiciens, astro-physiciens, géo-physiciens, bio-physiciens,
    - mécaflu, multiphysique, thermie/acoustique,
    - workflow génomiques (fonctionnelle, cellulaire, plantes, virus/bactéries),
    - HeeYa!^W IA, apprentissage(s) profond, accélération GPU,
    - etc.


### Vrac

* https://www.dataquest.io/blog/how-to-analyze-survey-data-python-beginner/
* https://github.com/PBSPro/pbspro/blob/master/test/fw/bin/pbs_loganalyzer
* https://github.com/NCAR/PBS_Optimization/blob/master/README.md
