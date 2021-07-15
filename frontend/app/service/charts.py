import datetime
from app.utils import combineDict


class Charts(object):

    def __init__(self, bddCon):
        self.e = bddCon

    @staticmethod
    def pickDate(form, rappel):

        date = """ AND start_time >= (%s)
                    AND start_time <= (%s) """
        
        if(form.dateByYear.data != None):
            year, month, day = form.dateByYear.data.year, form.dateByYear.data.month, form.dateByYear.data.day

            fromDate = datetime.datetime(year, month, day).timestamp()
            toDate = datetime.datetime(year+1, month, day).timestamp() #Year + 1
            rappel["Année"] = str(year)

            return date % (fromDate, toDate), rappel

        elif(form.dateByForkStart.data != None and form.dateByForkEnd.data != None):
            #FromYear, FromMonth, FromDay
            fromYear, fromMonth, fromDay = form.dateByForkStart.data.year, form.dateByForkStart.data.month, form.dateByForkStart.data.day
            #ToYear, ToMonth, ToDay
            toYear, toMonth, toDay = form.dateByForkEnd.data.year, form.dateByForkEnd.data.month, form.dateByForkEnd.data.day

            fromDate = datetime.datetime(fromYear, fromMonth, fromDay).timestamp()
            toDate = datetime.datetime(toYear, toMonth, toDay).timestamp()
            rappel["Debut"] = str(datetime.datetime.fromtimestamp(fromDate).strftime('%d-%m-%Y'))
            rappel["Fin"] = str(datetime.datetime.fromtimestamp(fromDate).strftime('%d-%m-%Y'))
            
            return date % (fromDate, toDate), rappel
            
        else:
            return "", rappel

    @staticmethod
    def pickGroup(form):

        if(form.groups.data != "Tout"):
            group = "AND job_.id_groupe = groupes.id_groupe AND groupes.group_name = '%s'"%form.groups.data
        else:
            group = "AND job_.id_groupe = groupes.id_groupe"

        return group
   
    @staticmethod
    def detectError(values:dict):
        if(all(x==0 for x in values.values())):
            return True
        return False

    def charts(self, form):
            pass

class userCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)
    
    def charts(self, form):
        charts = list()
        output = dict() #Sortie
        rappel = dict()
        error = False

        # Variables input
        date = self.pickDate(form, rappel)[0]
        user = form.users.data
        group = self.pickGroup(form)
        
        rappel["Utilisateur"] = form.users.data
        rappel["Groupe"] = form.groups.data


        # Job executé, Temps de calcul
        sql = """ 
            SELECT COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu {select}
            FROM job_, users {fromm}
            WHERE job_.id_user = users.id_user
                AND users.login {test} '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {where}
                {date}
            {groupBy}
            """
        
        totalExecUser = self.e.fetch(command=sql.format(select='',
                                                        date=date, 
                                                        test = "=",
                                                        user=user, 
                                                        fromm='', 
                                                        where='', 
                                                        groupBy=''), 
                                    fetchOne=True)
        if(Charts.detectError(totalExecUser)):
            return charts, rappel, True
        
        totalExecGroupe = self.e.fetch(command=sql.format(select='',
                                                        date=date, 
                                                        test = "!=",
                                                        user=user, 
                                                        fromm=', groupes', 
                                                        where=group, 
                                                        groupBy='GROUP BY groupes.id_groupe;'),
                                    fetchOne=True)
        if(Charts.detectError(totalExecGroupe)):
            return charts, rappel, True

        job_user, heure_user = totalExecUser["nb_job"], totalExecUser["sum_cpu"]/3600
        job_groupe, heure_groupe = totalExecGroupe["nb_job"], totalExecGroupe["sum_cpu"]/3600
        jobUserGroupe = {'job_user' : job_user, 'job_groupe' : job_groupe}
        heureUserGroupe = {'heure_user' : heure_user, 'heure_groupe' : heure_groupe}

        # Job Ok vs Hs
        sql = """
            SELECT COUNT(job_.id_job_) {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user     
                AND users.login = '{user}'     
                {where}
                {date}
            {groupBy}
                """

        requeteOk = self.e.fetch(command=sql.format(select = 'AS job_ok',
                                                        date  = date, 
                                                        user  = user, 
                                                        where = ' AND (job_.failed = 0 OR job_.exit_status = 0) ' + group, 
                                                        groupBy = ''), 
                                    fetchOne=True)
                                    
        requeteHs = self.e.fetch(command=sql.format(select = 'AS job_hs',
                                                        date  = date, 
                                                        user  = user, 
                                                        where = ' AND (job_.failed != 0 OR job_.exit_status != 0) ' + group, 
                                                        groupBy = ''), 
                                    fetchOne=True)
                                    
        requeteOkHs = combineDict(requeteOk, requeteHs)

        # Max de ru_wallclock, Avg de ru_wallclock et Min de ru_wallclock
        sql = """
            SELECT MAX(job_.ru_wallclock) AS max_wall, AVG(job_.ru_wallclock) AS avg_wall, MIN(job_.ru_wallclock) AS min_wall
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {where}
                {date}
            {groupBy}
            """

        requeteOther = self.e.fetch(command=sql.format(select = 'AS job_hs',
                                                        date  = date, 
                                                        user  = user, 
                                                        where = group, 
                                                        groupBy = ''), 
                                    fetchOne=True)

        output["jobUserGroupe"] = {"id":"jobUserGroupe", "type": "PieChart", "values" : jobUserGroupe, "title" : "test"}
        output["heureUserGroupe"] = {"id":"heureUserGroupe", "type": "PieChart", "values" : heureUserGroupe, "title" : "test2"}
        output["requeteOkHs"] = {"id":"requeteOkHs", "type": "PieChart", "values" : requeteOkHs, "title" : "test3"}
        output["requeteOther"] = {"id":"requeteOther", "type": "BarChart", "values" : requeteOther, "title" : "test4"}
        output["testStacked"] = {"id":"testStacked", "type": "BarChartStacked", "values" : requeteOther, "title" : "test5"}

        for key in output:
            charts.append(output[key])

        return charts, rappel, error
    

class groupesCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)





""" 
            ########
              USER
            ########

SELECT users.login, COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu 
FROM job_, users 
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login;

SELECT groupes.group_name, COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu 
FROM job_, groupes, users
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.id_user = users.id_user
    AND users.login != 'cmichel'
GROUP BY groupes.id_groupe;

SELECT users.login, COUNT(job_.id_job_)
FROM job_, users 
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;

'SELECT users.login, COUNT(job_.id_job_) 
FROM job_, users 
WHERE job_.id_user = users.id_user     
    AND users.login = 'cmichel'     
    AND job_.failed != 0     
    AND job_.exit_status != 0     
    AND job_.start_time >= 1325376000     
    AND job_.start_time <= 1356998400 
GROUP BY users.login ;

SELECT users.login, MAX(job_.ru_wallclock) AS max_wall, AVG(job_.ru_wallclock) AS avg_wall, MIN(job_.ru_wallclock) AS min_wall
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login;
"""

"""
            ##########
              GROUPE
            ##########

groupes, conso cpu + taux reussite

    SELECT groupes.group_name, COUNT(job_.id_job_), SUM(job_.cpu) AS sum_cpu 
    FROM job_, groupes 
    WHERE job_.id_groupe = groupes.id_groupe     
        AND groupes.group_name = 'chimie'     
        AND (job_.failed = 0 OR job_.exit_status = 0)     
        AND job_.start_time >= 1325376000     
        AND job_.start_time <= 1356998400 
    GROUP BY groupes.id_groupe ;

    SELECT groupes.group_name, COUNT(job_.id_job_) 
    FROM job_, groupes 
    WHERE job_.id_groupe = groupes.id_groupe     
        AND groupes.group_name = 'chimie'     
        AND (job_.failed = 0 OR job_.exit_status = 0)     
        AND job_.start_time >= 1325376000     
        AND job_.start_time <= 1356998400 
    GROUP BY groupes.id_groupe ;

    SELECT groupes.group_name, COUNT(job_.id_job_) 
    FROM job_, groupes 
    WHERE job_.id_groupe = groupes.id_groupe     
        AND groupes.group_name = 'chimie'     
        AND job_.failed != 0     
        AND job_.exit_status != 0     
        AND job_.start_time >= 1325376000     
        AND job_.start_time <= 1356998400 
    GROUP BY groupes.id_groupe ;

"""