# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import GPS
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
    # visuallo la query per debug
    # creo un cursore
    cur = conn.cursor()
    cur.execute(fin_sql)

    stop = cur.fetchall()
    stop = json.dumps(stop)
    stop = stop.split(', ')
    if len(stop)>1:
        return stop[29]
    else:
        return None

def check_position(conn, lat, lon, delta):
    """ chiama il metodo 'select_stops_around' e se il valore ritornato differisce da 'None'
        chiama il metodo 'passed', 'update_passengers_at_stop', '#metodo annuncio vocale',
        e inoltre controlla tramite il database se la corsa ha raggiunto l'ultima fermata
    :param conn: connessione al database
    :param lat: latitudine della posizione
    :param lon: longitudine della posizione
    :param delta: valore di errore che segna l'intervallo di ricerca
    :return: 'True' o 'False'
    """
    stop = select_stops_around(conn, lat, lon, delta)
    if stop!=None and stop!="":
        passed(conn, stop)
        update_passengers_at_stop(conn, prova.count(prova.take_photo(0)), stop)
        # chiamata metodo annuncio vocale fermata
    global last_stop
    if stop==last_stop:
        global end_trip
        end_trip = True

def passed(conn, stop):
    """ Aggiorna la colonna 'passed' corrispondente alla fermata 'stop' nel database
        da 'False' a 'True'
    :param conn: connessione al database
    :param stop: nome della fermata raggiunta
    """
    try:
        cur = conn.cursor()
        change_state = """UPDATE trip SET passed = TRUE WHERE stop_name = """ + stop
        cur.execute(change_state)
    except Error as e:
        print(e)

def update_passengers_at_stop(conn, num, stop):
    """ Aggiorna il numero di passeggeri aggiungendolo all'interno del database, nella colonna 'passengers'
        nella riga corrispondente alla fermata
    :param conn: connessione al database
    :param num: numero di passeggeri presenti
    :param stop: nome della fermata in cui è stato effettuato il rilevamento
    """
    try:
        print(num)
        cur = conn.cursor()
        add_passengers = """UPDATE trip SET passengers = """ +str(num) +""" WHERE stop_name = """ +stop
        cur.execute(add_passengers)
        conn.commit()
    except Error as e:
        print(e)

def sparticorse(conn, trip_id):
    """ Crea la tabella contenente le informazioni relative alla corsa che sta venendo effettuata
    :param conn: connessione al database
    :param trip_id: codice identificativo della corsa che sta venendo effettuata
    """
    try:
        cur = conn.cursor()
        select = """CREATE TABLE trip AS SELECT * FROM routes inner join trips inner join stop_times inner join stops
                        on trips.route_id = routes.route_id
                        AND stop_times.trip_id = trips.trip_id
                        AND stops.stop_id = stop_times.stop_id
                        where trips.trip_id =""" +trip_id
        cur.execute(select)
        add_column = """ALTER TABLE trip
                                ADD passengers TEXT DEFAULT 0"""
        cur.execute(add_column)
        add_column = """ALTER TABLE trip
                                ADD passed TEXT DEFAULT FALSE"""
        cur.execute(add_column)
    except Error as e:
        print(e)

def define_last_stop(conn):
    """ Ricava dal database il nome dell'ultima fermata della corsa che sta venendo effettuata
        e lo assegna alla variabile 'last_stop'

    :param conn: connessione al database
    """
    try:
        cur = conn.cursor()
        select_stops = """SELECT stop_name FROM trip"""
        cur.execute(select_stops)
        stops = cur.fetchall()
        stops = json.dumps(stops)
        stops = stops.replace("[", "").replace("]", "").replace('"', "")
        stops = stops.split(", ")
        global last_stop
        last_stop = stops[len(stops)-1]
    except Error as e:
        print(e)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    end_trip = False
    last_stop = ''
    db_conn = create_connection('db\\actv_aut.db')
    sparticorse(db_conn, input('INSERIRE CODICE VIAGGIO'))
    define_last_stop(db_conn)
    while not end_trip:
        coordinate = GPS.get_gps_position()
        coordinate = coordinate.split(' ')
        check_position(db_conn, coordinate[0], coordinate[1], 0.00005)
    #check_position(db_conn, 3, 3, 0.00005)
    # select_all_stops(db_conn)

    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
