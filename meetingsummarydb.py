'''
Create the relational datamodel of a corpus.
v.1.0.0 2022.3.28
'''

import sqlite3

class DBModel():
    '''The DM model creates a set of tables in a database based on the SQL.'''

    def __init__(self):
        pass

    def create(self, dbpath, pathtoscript):
        '''With an db path and path to script, create the db file.'''

        try:
            sqliteConnection = sqlite3.connect(dbpath)
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            with open(pathtoscript, 'r') as sqlite_file:
                sql_script = sqlite_file.read()
            cursor.executescript(sql_script)
            print("SQLite script executed successfully")
            cursor.close()

        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
        return dbpath

def main():
    ''' '''
    dbpath = "wordsample/summary.db"
    db  = DB.DBModel()
    db.create(dbpath, 'meetingsummary.sql')

if __name__ == "__main__":
    main()