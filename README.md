# PyChartAccounting

TL;DR: Cold analysis (disconnected) of HPC Scheduler accounting file (currently SGE only).

Status : Prototype. Work in Progress. It display charts! (thanks to Fleura29)

Usable with Flask directly, or mod_wsgi-express, for now.


## Specifications

Offer a 'graphical' analysis tool (charts) to admins and users of
our clusters. Multiple filter possibilities (see § Charts). Inspired by 
[S-GAE2](https://rdlab.cs.upc.edu/s-gae/) (from rdlab, Barcelona University).

Accounting files, over several years, become (very) heavy, and
difficult to query (4.4GiB 2011-2017, already 4.8GiB for 2018-2020).

Injecting their content into a `middleware/datawarehouse` to crush the data in all directions becomes relevant.


### Frontend

* Web (python3? R-shiny? -> Flask),
* At first: "No authentication", at least, not related to accounting: A DR can look at the accounting of his doctoral students or his group, a Correspondent must be able to look at the accounting of the lab(s) for which he is responsible, etc.
* Easy to use : Select, display, Boom!.
* As fast as possible...

**Choix final** :

* frontend : python3/html/js (Flask)

### Charts

Piecharts, plotted dots, barcharts...

* By calendar year, or by period (start date, end date), over the entire available data:
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time (wait, start - submission)

    * by user, group, metagroup (group of groups or users):
        * total executed jobs
        * total executed hours
        * average job memory usage
        * average job execution time
        * average job queued time (wait, start - submission)
        * duration (min, max, med, avg) of jobs
        * cpu vs system? (I/O ? ratio % ?)
        * ram (avg, max)

We understood the principle, but in doubt, and so as not to forget (always on the basis of a period of time):

* by cluster(s), waiting queue(s), nodes :
    * total executed jobs
    * total executed hours
    * average job memory usage
    * average job execution time
    * average job queued time
    * duration (min, max, med, avg) of jobs
    * cpu vs system? (I/O ? ratio % ?)
    * ram (avg, max)

* Top 10:
    * users
    * group(s)
    * métagroup(s)?

* Inverted Top 10: (least used)?
    * queue(s)
    * node(s)

* Others: (TODO)
    * by projets (SGE projects or groups):
        * total executed jobs
        * total executed hours
        * average job memory usage
        * average job execution time
        * average job queued time
        * etc.
    * slots-per-job usage (nb of slots/job : sequential, // mononode (as OpenMP), // multinode (as openMPI))
    * leave the door open to frightening possibilities of mixtures...


### BackOffice / Middleware / Workflow

Python3 (parceque je comprends plus rien au php). Un exemple de ce qui était fait dans `parse_accounting.py` 
(voir aussi [SGE toolbox](https://github.com/ltaulell/sge_toolbox)).

Regarder aussi les outils d'analyse de log ? Malgré sa structure chelou, 
l'accounting *EST* un fichier de log (ou un CSV, aussi). Voir `SGE_accounting_file_format.rst`.

Pandas ? (csv, delimiter=':') timeseries.

Un QueryLangage quelconque : SQL (S-GAE2 mouline tout dans du SQL) ? NoSQL ? SQLite ?

Schéma(s) -> voir PyChartAccounting.mm (mindmap, freeplane) et model.gaphor (gaphor)

accounting -> python3 -> format intermédiaire -> query -> présentation (graphs)

**Final Choice**:

* backoffice : flask (python3) + psycopg2 (SQL)

requirements: flask flask_wtf wtforms pandas psycopg2 (see requirements.txt)

* datawarehouse : SQL (postgresql)


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

