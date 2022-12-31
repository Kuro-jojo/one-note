import sqlite3
from sqlite3 import Error

def get_db(db_file:str):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)
   
    return conn

def init_db(db_file:str, sql_script:str):
    """ create all tables in the database
    :param db_file: database file
    :param sql_script: sql script
    :return: 
    """
    db = get_db(db_file)

    with open(sql_script, 'r') as f:
        sql_script = f.read() # get the content of the sql script

    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

