from flask import Flask, render_template, redirect, request
from user import Profile
from datetime import datetime
import os

from db_controller import *


app = Flask(__name__)

user = Profile('', 0)
db = db_controller('')

# index Route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user.name = request.form.get('username').lower()
        # Checks if the user database exist. If not then we create a new table, otherwise we just connect to it
        if os.path.exists('database/{user}'.format(user=user.name)):
            db = db_controller(data_path='database/{user}'.format(user=user.name))
        else:
            db = db_controller(data_path='database/{user}'.format(user=user.name))
            db.initialize_db()

        return redirect('/home')
    return render_template('index.html')

# App route to home page
@app.route('/home', methods=['POST', 'GET'])
def home():
    db = db_controller(data_path='database/{user}'.format(user=user.name))
    entries = db.fetch_entries()
    user.current_balance = db.calc_value()

    if request.method == 'POST':
        # Update Database on 'POST'
        transaction_name = request.form.get('trans_name')
        transaction_value = request.form.get('amount')
        curr_time = datetime.now().strftime('%Y-%m-%d')
        

        db.addEntry(curr_time, transaction_name, transaction_value)
        entries = db.fetch_entries()

        # Updates user current balance based on database
        user.current_balance = db.calc_value()
    return render_template('home.html', user=user, entries=entries)

# Route to monthly spendings page
@app.route('/monthly-spending')
def monthly_spending():

    if request.method == 'POST':
        form_month = request.form.get('form_month')
        entries = db.grab_month(month=form_month)
    return render_template('monthly-spending.html', entries=entries)
    

if __name__ == "__main__":
    app.run(debug=True)