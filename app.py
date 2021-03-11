###############################################################################
#
#   Imports
#
###############################################################################

from flask import Flask
from flask import render_template
from flask import request
import sqlite3
import os
import matplotlib
import time

matplotlib.use('Agg')
import matplotlib.pyplot as plt

###############################################################################
#
#   Variables
#
###############################################################################

current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = '\expenses.db'
expenses_plot_path = 'static/'
expenses_plot_name = 'expenses_bar'
app = Flask(__name__)


###############################################################################
#
#   Routing
#
###############################################################################

@app.route('/')
def expenses():
    # Connect to database
    con = sqlite3.connect(db_path[1:])
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute('select * from expenses')

    rows = cur.fetchall()

    # Create bar chart regarding current expense sum

    # remove existing charts
    for filename in os.listdir('static/'):
        if filename.startswith('expenses_bar'):  # not to remove other images
            os.remove('static/' + filename)

    # for each name, get sum of expense
    cur.execute('SELECT Name, SUM(Expense_Amount) '
                'FROM expenses '
                'GROUP BY Name')
    name_amount_tpl = list(cur)

    # Create bar chart including all names and expenses within database
    names = [i[0] for i in name_amount_tpl]
    amounts = [i[1] for i in name_amount_tpl]

    # Create and save bar chart
    plt.bar(names, amounts, align='center', color='tab:blue')

    # Set path and save chart
    full_path_barchart = expenses_plot_path + expenses_plot_name + str(
        time.time()) + ".png"
    plt.savefig(full_path_barchart)

    return render_template('expenses.html', rows=rows,
                           barchart_plot=full_path_barchart)


@app.route('/add-expense')
def add_expense_form():
    return render_template('add-expense.html')


@app.route('/add-expense', methods=['POST'])
def add_expenses():
    # Retrieve data from form
    name = request.form['name']
    expense_desc = request.form['expense-desc']
    expense_amount = float(request.form['expense-amount'])

    # Connect to databse
    connection = sqlite3.connect(current_directory + db_path)
    cursor = connection.cursor()
    # Insert data into database
    query_1 = f"INSERT INTO expenses VALUES('{name}', " \
              f"'{expense_desc}', {expense_amount})".format(
        name=name, expense_desc=expense_desc,
        expense_amount=expense_amount)
    cursor.execute(query_1)
    connection.commit()

    return render_template('add-expense.html')


###############################################################################
#
#   Run
#
###############################################################################

# if __name__ == '__main__':
#     app.run(debug=True)
