# PyChartAccounting

Status : Draft. Early Work in Progress.

TL;DR: Cold analysis (disconnected) of HPC Scheduler accounting file (currently SGE).


## Cahier des charges

Proposer un outil d'analyse 'graphique' (charts) aux admins et utilisateurs de 
nos clusters. Multiples possibilités de filtres (voir § Charts). Inspiré de 
[S-GAE2](https://rdlab.cs.upc.edu/s-gae/) (from rdlab, Barcelona University).

Les fichiers d'accounting, sur plusieurs années, deviennent (trés) lourds, et 
difficile a interroger (4.4Go 2011-2017, déjà 4.8Go pour 2018-2020).

Injecter leur contenu dans un `middleware` pour triturer les data dans tous les 
sens devient pertinent.


### Frontend

* Web (python3? R-shiny?),
* At first: "No authentication", at least, not related to accounting: Un DR peut regarder l'accounting de ses thésards ou de son groupe, un Correspondant doit pouvoir regarder l'accounting du/des labo(s) dont il a la charge.
* Easy to use : Select, display, Boom!.
* Fast...


### Charts

Piecharts, plotted dots, barcharts...

* Par année civile, ou par période (date de début, date de fin), sur la totalité :
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time (wait, start - submission)

    * par utilisateur, groupe, métagroupe (groupe de groupes ou d'utilisateurs) :
        * total executed jobs
        * total executed hours
        * average job memory usage
        * average job execution time
        * average job queued time (wait, start - submission)
        * durées (min, max, med, avg) des jobs
        * cpu vs système (I/O ? ratio % ?)
        * ram (avg, max)

On a compris le principe, mais dans le doute, et pour ne pas en oublier (toujours sur la base d'une période de temps) :

* par cluster(s), file(s) d'attentes, nodes :
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time
    * durées (min, max, med, avg) des jobs
    * cpu vs système (I/O ? ratio % ?)
    * ram (avg, max)

* Top 10 : (les + gros/utilisés)
    * utilisateurs
    * métagroups

* Inverted Top 10 : (les - utilisés)
    * queue(s)
    * node(s)

* Autres :
    * par projets (SGE projects ou groupes):
        * total executed jobs
        * total executed hours
        * average job memory usage
        * average job execution time
        * average job queued time
        * etc.
    * slots-per-job usage (nb de slots/job : séquentiel, // mononode, // multinode)
    * laisser la porte ouverte à d'effroyables possibilités de mélanges...


### Backend / Middleware / Workflow

Python3 (parceque je bite rien au php). Une partie du taff est déjà fait dans `parse_accounting.py` 
(voir aussi [SGE toolbox](https://github.com/ltaulell/sge_toolbox)).

Regarder aussi les outils d'analyse de log ? Malgré sa structure chelou, 
l'accounting *EST* un fichier de log (ou un CSV, aussi). Voir `SGE_accounting_file_format.rst`.

Pandas ? (csv, delimiter=':') timeseries.

Un QueryLangage quelconque : SQL (S-GAE2 mouline tout dans du SQL) ? NoSQL ? SQLite ?

Schéma(s) -> voir PyChartAccounting.mm (mindmap, freeplane) et model.gaphor (gaphor)

accounting -> python3 -> format intermédiaire -> query -> présentation (graphs)


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
    - chimistes, astro-chimistes, géo-chimistes, bio-chimistes,
    - physiciens, astro-physiciens, géo-physiciens, bio-physiciens,
    - mécaflu, multiphysique, thermie/acoustique,
    - workflow génomiques (fonctionnelle, cellulaire, plantes, virus/bactéries),
    - IA, apprentissage(s) profond, accélération GPU,
    - etc.


### Vrac

* https://www.dataquest.io/blog/how-to-analyze-survey-data-python-beginner/
* https://github.com/PBSPro/pbspro/blob/master/test/fw/bin/pbs_loganalyzer
* https://github.com/NCAR/PBS_Optimization/blob/master/README.md
