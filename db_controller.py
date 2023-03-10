import sqlite3
from datetime import datetime

class db_controller:
    def __init__(self, data_path):
        self.conn = sqlite3.connect(data_path, check_same_thread=False)
        self.c = self.conn.cursor()

    # Initializes db
    def initialize_db(self):
        self.c.execute("""CREATE TABLE user (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            time_of_entry text,
            transaction_name text,
            transaction_value number
        )
        """)
        self.conn.commit()
    
    # Add entry to database
    def addEntry(self, time, transaction, value):
        self.c.execute("""INSERT INTO user (time_of_entry,transaction_name,transaction_value) VALUES ('{time}','{transaction_name}','{transaction_value}')
        """.format(time=time, transaction_name=transaction, transaction_value=value)
        )
        self.conn.commit()
    
    # Fetch all the data based on the username(search_for)
    def fetch_all_entries(self):
        self.c.execute("SELECT * FROM user")
        self.conn.commit()
        return self.c.fetchall()
    

    # Clears all data from the table
    def clear_table(self):
        self.c.execute('DELETE FROM user;',)
        self.conn.commit()

    # Calculate Sum of transaction_value
    # entries: formatted entries to calculate based on fetch entries
    def calc_value(self, entries):
        rows = entries
        sum = 0
        for row in rows:
            sum += row[3]
        return sum
    
    # Grab all the entries based on the specific month
    def grab_from_time(self, month, year):
        check_month = month

        if int(check_month) < 10:
            check_month = '0' + check_month
        self.c.execute("SELECT * FROM user WHERE strftime('%m %Y', time_of_entry) = '{month} {year}'".format(month=check_month, year=year))
        self.conn.commit()

        return self.c.fetchall()
    
