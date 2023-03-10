from flask import Flask, render_template, redirect, request
from user import Profile
from datetime import datetime
import os

from db_controller import *


app = Flask(__name__)

user = Profile('', 0)


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
    entries = db.fetch_all_entries()
    user.current_balance = db.calc_value(entries)

    if request.method == 'POST':
        # Update Database on 'POST'
        transaction_name = request.form.get('trans_name')
        transaction_value = request.form.get('amount')
        curr_time = datetime.now().strftime('%Y-%m-%d')
        

        db.addEntry(curr_time, transaction_name, transaction_value)
        entries = db.fetch_all_entries()

        # Updates user current balance based on database
        user.current_balance = db.calc_value(entries)
    return render_template('home.html', user=user, entries=entries)

# Route to monthly spendings page
@app.route('/timeframe_spending', methods=['POST', 'GET'])
def monthly_spending():
    db = db_controller(data_path='database/{user}'.format(user=user.name))
    entries = []

    if request.method == 'POST':
        form_month = request.form.get('form_month')
        form_year = request.form.get('form_year')
        entries = db.grab_from_time(form_month, form_year)

    return render_template('timeframe_spending.html', entries=entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000, debug=True)