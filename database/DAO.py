from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`)as anno
from new_ufo_sightings.sighting s 
order by anno desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getForme(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as forma
from new_ufo_sightings.sighting s 
where year (s.`datetime`) = %s
order by forma ASC"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["forma"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getArchi(anno,forma,idmap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as primo, s2.id as secondo
from new_ufo_sightings.sighting s, new_ufo_sightings.sighting s2 
where year (s.`datetime`) = %s and s.shape = %s and s2.shape = s.shape 
and year (s.`datetime`) = year (s2.`datetime`)and s.state = s2.state  and s2.id != s.id
and s2.`datetime` > s.`datetime`"""
            cursor.execute(query, (anno,forma,))

            for row in cursor:
                result.append((idmap[row["primo"]],idmap[row["secondo"]]))
            cursor.close()
            cnx.close()
        return result
