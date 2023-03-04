import sqlite3

class db_controller:
    def __init__(self, data_path):
        self.conn = sqlite3.connect(data_path, check_same_thread=False)
        self.c = self.conn.cursor()

    # Initializes db
    def initialize_db(self):
        self.c.execute("""CREATE TABLE user (
            time_of_entry text,
            transaction_name text,
            transaction_value number
        )
        """)
        self.conn.commit()
    
    # Add entry to database
    def addEntry(self, time, transaction, value):
        self.c.execute("""INSERT INTO user VALUES ('{time}', '{transaction_name}', '{transaction_value}')
        """.format(time=time, transaction_name=transaction, transaction_value=value)
        )
        self.conn.commit()
    
    # Fetch all the data based on the username(search_for)
    def fetch_entries(self):
        self.c.execute("SELECT * FROM user")
        self.conn.commit()
        return self.c.fetchall()
    

    # Clears all data from the table
    def clear_table(self):
        self.c.execute('DELETE FROM user;',)
        self.conn.commit()

    # Calculate Sum of transaction_value
    def calc_value(self):
        rows = self.fetch_entries()
        sum = 0
        for row in rows:
            sum += row[2]
        return sum
    
    def grab_month(self, month):
        self.c.execute("SELECT * FROM user WHERE strftime('%m', time_of_entry) = '{month}'".format(month=month))
        self.conn.commit()
        return self.c.fetchall()
    