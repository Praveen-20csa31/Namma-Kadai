from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Praveen@3814'
app.config['MYSQL_DB'] = 'nammakadai'

mysql = MySQL(app)

@app.route('/')
def home():
    # Fetch the cash balance from the Company table
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT cash_balance FROM Company')
    cash_balance = cursor.fetchone()[0]
    
    return render_template('home.html', cash_balance=cash_balance)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = float(request.form['price'])

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Item (item_name, price) VALUES (%s, %s)", (item_name, price))
        mysql.connection.commit()
        cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT item_name, price FROM Item")
    items = cursor.fetchall()
    cursor.close()

    return render_template('add_item.html', items=items)    
@app.route('/add_purchase', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantity = int(request.form['quantity'])
        price_per_item = float(request.form['price_per_item'])

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT price FROM Company")
        cash_balance = cursor.fetchone()[0]

        total_cost = price_per_item * quantity

        if total_cost <= cash_balance:
            cursor.execute("UPDATE Company SET cash_balance = cash_balance - %s", (total_cost,))
            cursor.execute("UPDATE Item SET qty = qty + %s WHERE item_id = %s", (quantity, item_id))
            mysql.connection.commit()
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT item_id, item_name, qty, price FROM Item")
    items = cursor.fetchall()
    cursor.close()

    return render_template('add_purchase.html', items=items )   

if __name__ == '__main__':
    app.run(debug=True)
