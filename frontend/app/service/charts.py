import datetime

class Charts(object):

    def __init__(self, bddCon):
        self.e = bddCon

    @staticmethod
    def pickDate(form, recall):

        date = """ AND start_time >= (%s)
                    AND start_time <= (%s) """
        
        if(form.dateByYear.data != None):
            year, month, day = form.dateByYear.data.year, form.dateByYear.data.month, form.dateByYear.data.day

            fromDate = datetime.datetime(year, month, day).timestamp()
            toDate = datetime.datetime(year+1, month, day).timestamp() #Year + 1
            recall["Année"] = str(year)

            return date % (fromDate, toDate), recall

        elif(form.dateByForkStart.data != None and form.dateByForkEnd.data != None):
            #FromYear, FromMonth, FromDay
            fromYear, fromMonth, fromDay = form.dateByForkStart.data.year, form.dateByForkStart.data.month, form.dateByForkStart.data.day
            #ToYear, ToMonth, ToDay
            toYear, toMonth, toDay = form.dateByForkEnd.data.year, form.dateByForkEnd.data.month, form.dateByForkEnd.data.day

            fromDate = datetime.datetime(fromYear, fromMonth, fromDay).timestamp()
            toDate = datetime.datetime(toYear, toMonth, toDay).timestamp()
            recall["Debut"] = str(datetime.datetime.fromtimestamp(fromDate).strftime('%d/%m/%Y'))
            recall["Fin"] = str(datetime.datetime.fromtimestamp(toDate).strftime('%d/%m/%Y'))
            
            return date % (fromDate, toDate), recall
            
        else:
            return "", recall

    @staticmethod
    def pickGroup(form):

        if(form.groups.data != "Tout"):
            group = "AND job_.id_groupe = groupes.id_groupe AND groupes.group_name = '%s'"%form.groups.data
        else:
            group = "AND job_.id_groupe = groupes.id_groupe"

        return group
   
    @staticmethod
    def detectError(values):
        if isinstance(values, int) or isinstance(values, float):
            return True
        elif(all(x==0 for x in values.values())):
            return True
        return False

    @staticmethod
    def isNullDict(name, value):
        if isinstance(value, int) or isinstance(value, float):
            return 0
        else:
            return value[name]
    
    @staticmethod
    def nameDict(name, value):
        return {name: value}

    @staticmethod
    def multiDict(values:dict, KeysValues : list):
        if not values:
            return ({'value': 0})
        dico = list()

        if len(KeysValues) == 2 and type(KeysValues[0]) != list:
            if len(values) == 2:
                temp = {values[KeysValues[0]]: values[KeysValues[1]]}
                dico.append(temp)
            else:
                for value in values:
                    temp = {value[KeysValues[0]]: value[KeysValues[1]]}
                    dico.append(temp)
        else:
            temp = dict()
            for value in values:
                for keyValue in KeysValues:
                    if len(keyValue) == 2:
                        temp = {value[keyValue[0]]: value[keyValue[1]]}
                    else:
                        temp = {keyValue[0]: value[keyValue[0]]}
                    dico.append(temp)

        return tuple(dico)

    def charts(self, form):
        pass
        