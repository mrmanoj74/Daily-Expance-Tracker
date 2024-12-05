from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify  # type: ignore
from flask_mysqldb import MySQL  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  # Needed for session management

# MySQL connection configuration
mysql = MySQL(app)

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']  # Get the email from the form
        
        # Insert user into database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                       (username, password, email))  # Include email
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        date = request.form['date']
        description = request.form['description']
        
        # Insert expense into the database
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO expenses (user_id, category, amount, date, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (session['user_id'], category, amount, date, description))
        mysql.connection.commit()
        cursor.close()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    report_data = []
    if request.method == 'POST':
        period = request.form['period']
        query = ""

        if period == 'daily':
            query = "SELECT * FROM expenses WHERE user_id = %s AND date = CURDATE()"
        elif period == 'weekly':
            query = "SELECT * FROM expenses WHERE user_id = %s AND WEEK(date) = WEEK(CURDATE())"
        elif period == 'monthly':
            query = "SELECT * FROM expenses WHERE user_id = %s AND MONTH(date) = MONTH(CURDATE())"
        elif period == 'yearly':
            query = "SELECT * FROM expenses WHERE user_id = %s AND YEAR(date) = YEAR(CURDATE())"

        cursor = mysql.connection.cursor()
        cursor.execute(query, (session['user_id'],))
        report_data = cursor.fetchall()
        cursor.close()

    return render_template('reports.html', report_data=report_data)

@app.route('/dashboard')
def dashboard():
    # Example data, replace with actual data fetched from DB
    user = {'username': 'john_doe'}
    recent_expenses = [
        {'category': 'Food', 'amount': 100, 'date': '2024-12-01'},
        {'category': 'Transport', 'amount': 50, 'date': '2024-12-02'}
    ]
    return render_template('dashboard.html', user=user, recent_expenses=recent_expenses)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Get the period from the AJAX request
    data = request.get_json()
    period = data['period']

    # Simulate fetching data based on the selected period
    # Replace this with database queries
    if period == 'daily':
        labels = ['2024-12-01', '2024-12-02', '2024-12-03']
        values = [100, 50, 150]
    elif period == 'weekly':
        labels = ['Week 1', 'Week 2', 'Week 3']
        values = [500, 700, 450]
    elif period == 'monthly':
        labels = ['January', 'February', 'March']
        values = [1000, 1200, 800]
    else:  # yearly
        labels = ['2023', '2024']
        values = [12000, 15000]

    # Return the data in JSON format for the frontend to use
    return jsonify({'labels': labels, 'values': values})

if __name__ == "__main__":
    app.run(debug=True)
