# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from distutils.command.build_scripts import first_line_re
import json
import GPS
import audio
import prova
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# def add_table(trip_file):
#     """ aggiunge tabella al database
#
#     :param trip_file: collegamento al database
#     """
#     try:
#         cur = trip_file.cursor()
#         table = """CREATE TABLE Trip(
#                         stop TEXT UNIQUE,
#                         latitude TEXT DEFAULT 0,
#                         longitude TEXT DEFAULT 0,
#                         passengers TEXT DEFAULT 0,
#                         passed TEXT DEFAULT 0
#                     );"""
#         cur.execute(table)
#     except Error as e:
#         print("Errore nella creazione della tabella")


# SELECT * FROM stops WHERE (stop_lat BETWEEN 45.493 AND 45.494 ) AND (stop_lon BETWEEN 12.245 AND 12.246)
def select_stops_around(conn, lat, lon, delta):
    """ Ricerca nel database le coordinate e se trova corrispondenza ritorna il nome della fermata,
        altrimenti ritorna 'None'
    :param conn: connessione al database
    :param lat: latitudine della posizione
    :param lon: longitudine della posizione
    :param delta: valore di errore che segna l'intervallo di ricerca
    :return: stringa contenente il nome della fermata corrispondente alle coordinate
    """
    # query sq per a ricerca geografica di una fermata
    sql = "SELECT * FROM trip WHERE (stop_lat BETWEEN {min_lat:.4f} AND {max_lat:.4f} ) AND (stop_lon BETWEEN {min_lon:.4f} AND {max_lon:.4f})"
    min_lat = lat-delta
    max_lat = lat+delta
    min_lon = lon-delta
    max_lon = lon+delta
    fin_sql = sql.format(min_lat=min_lat,max_lat=max_lat,min_lon=min_lon,max_lon=max_lon)
    # visualizzo la query per debug
    # creo un cursore
    cur = conn.cursor()
    cur.execute(fin_sql)
    stop = cur.fetchall()
    return stop

def check_position(conn, lat, lon, delta):
    """ chiama il metodo 'select_stops_around' e se il valore ritornato differisce da 'None'
        chiama il metodo 'passed', 'update_passengers_at_stop', 'audio'(questo tramite il passed),
        e inoltre controlla tramite il database se la corsa ha raggiunto l'ultima fermata
    :param conn: connessione al database
    :param lat: latitudine della posizione
    :param lon: longitudine della posizione
    :param delta: valore di errore che segna l'intervallo di ricerca
    :return: 'True' o 'False'
    """
    stop = select_stops_around(conn, lat, lon, delta)
    if stop!=None and stop!="":
        global cur_stop
        cur_stop = stop
        set_next_stop()
        passed(conn, cur_stop)#all'interno di questo metodo viene chiamato audio() per l'annuncio vocale
        update_passengers_at_stop(conn, prova.count(prova.take_photo(0)))
    global last_stop
    if cur_stop==last_stop:
        global end_trip
        end_trip = True
        delete_table_trip(conn)

def passed(conn):
    """ Aggiorna la colonna 'passed' corrispondente alla fermata 'stop' nel database
        da 'False' a 'True'
    :param conn: connessione al database
    :param stop: nome della fermata raggiunta
    """
    try:
        global cur_stop
        global next_stop
        cur = conn.cursor()
        query = """SELECT passed FROM trip WHERE stop_name = """ +cur_stop
        if cur.execute(query) == False:
            audio.audio(cur_stop, next_stop)
        change_state = """UPDATE trip SET passed = TRUE WHERE stop_name = """ + cur_stop
        cur.execute(change_state)
        conn.commit()
    except Error as e:
        print(e)

def update_passengers_at_stop(conn, num):
    """ Aggiorna il numero di passeggeri aggiungendolo all'interno del database, nella colonna 'passengers'
        nella riga corrispondente alla fermata
    :param conn: connessione al database
    :param num: numero di passeggeri presenti
    :param stop: nome della fermata in cui è stato effettuato il rilevamento
    """
    try:
        global cur_stop
        print(num)
        cur = conn.cursor()
        add_passengers = """UPDATE trip SET passengers = """ +str(num) +""" WHERE stop_name = """ +cur_stop
        cur.execute(add_passengers)
        conn.commit()
    except Error as e:
        print(e)

def delete_table_trip(conn):
    try:
        cur = conn.cursor()
        delete_table = """DROP TABLE trip"""
        cur.execute(delete_table)
        conn.commit()
    except Error as e:
        print(e)

def column_exists(conn, name, col):
    isExist = False
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(" + name + ")", None)
        cols = cur.fetchall()
        cols = json.dumps(cols)
        for c in cols:
            if (c == col):
                isExist = True
    except Error as e:
        print(e)
    finally:
        return isExist

def sparticorse(conn, trip_id):
    """ Crea la tabella contenente le informazioni relative alla corsa che sta venendo effettuata
    :param conn: connessione al database
    :param trip_id: codice identificativo della corsa che sta venendo effettuata
    """
    try:
        cur = conn.cursor()
        select = """CREATE TABLE IF NOT EXISTS trip AS SELECT * FROM routes inner join trips inner join stop_times inner join stops
                        on trips.route_id = routes.route_id
                        AND stop_times.trip_id = trips.trip_id
                        AND stops.stop_id = stop_times.stop_id
                        where trips.trip_id =""" +trip_id
        cur.execute(select)
        conn.commit()
        add_column = """ALTER TABLE trip
                                ADD passengers TEXT DEFAULT 0"""
        if (column_exists(conn, 'trip', 'passengers')):
            cur.execute(add_column)
        conn.commit()
        add_column = """ALTER TABLE trip
                                ADD passed TEXT DEFAULT FALSE"""
        if (column_exists(conn, 'trip', 'passed')):
            cur.execute(add_column)
        conn.commit()
    except Error as e:
        print(e)

def stop_list(conn):
    try:
        cur = conn.cursor()
        select_stops = """SELECT stop_name FROM trip"""
        cur.execute(select_stops)
        rows = cur.fetchall()
        stops = []
        for row in rows:
            t = row[0]
            stops.append(t)
        stops = json.dumps(stops)
        stops = stops.replace("[", "").replace("]", "").replace('"', "")
        stops = stops.split(", ")
        return stops
    except Error as e:
        print(e)



def set_next_stop():
    global next_stop, stops, cur_stop
    next_stop = stops[stops.index(cur_stop)+1]

def get_info(conn):
    try:
        global cur_stop
        cur = conn.cursor()
        get_info = """SELECT route_short_name, trip_headsign, route_long_name, stop_name, stop_lat, stop_lon, passengers, passed FROM trip WHERE stop_name = """ + cur_stop
        cur.execute(get_info)
        rows = cur.fetchall()
        print(rows)
        info = []
        for row in rows:
            t = row[0]
            info.append(t)
        save_file = open("info.json", "w")
        json.dump(info, save_file, indent = 2)
        save_file.close()
    except Error as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    end_trip = False
    last_stop = ''
    cur_stop = ''
    next_stop = ''
    db_conn = create_connection('db/actv_aut.db')
    sparticorse(db_conn, input('INSERIRE CODICE VIAGGIO\n')) #
    stops = stop_list(db_conn)
    last_stop = stops[len(stops)-1]
    first_stop = stops[0]
    next_stop = stops[1]
    while not end_trip:
        coordinate = GPS.get_gps_position()
        print(coordinate)
        coordinate = coordinate.split(' ')
        check_position(db_conn, float(coordinate[0]), float(coordinate[1]), 0.00005)
        get_info(db_conn)
        
    #check_position(db_conn, 3, 3, 0.00005) PER PROVE IN ASSENZA DI GPS

    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
