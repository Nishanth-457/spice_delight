# ============================================================
#  SPICE DELIGHT — Main Flask Application (Railway Version)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'spicedelight_secret_key_2025'

# ============================================================
# DATABASE SETTINGS — Railway MySQL
# ============================================================
DB_HOST     = os.environ.get('MYSQLHOST',     'mysql.railway.internal')
DB_USER     = os.environ.get('MYSQLUSER',     'root')
DB_PASSWORD = os.environ.get('MYSQLPASSWORD', 'SaKyjNPtmbZAVJTQqGbDCzIljnZJNvgi')
DB_NAME     = os.environ.get('MYSQLDATABASE', 'railway')
DB_PORT     = int(os.environ.get('MYSQLPORT', 3306))

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.Cursor
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================================
# ROUTE 1: Home
# ============================================================
@app.route('/')
def home():
    return redirect(url_for('login'))

# ============================================================
# ROUTE 2: Login
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email    = request.form['email']
        password = hash_password(request.form['password'])
        db  = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        db.close()
        if user:
            session['user_id']   = user[0]
            session['user_name'] = user[1]
            session['is_admin']  = user[4]
            return redirect(url_for('menu'))
        else:
            error = "Wrong email or password. Try again!"
    return render_template('login.html', error=error)

# ============================================================
# ROUTE 3: Signup
# ============================================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = hash_password(request.form['password'])
        db  = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()
        if existing:
            error = "Email already registered! Please login."
        else:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                        (name, email, password))
            db.commit()
            cur.close()
            db.close()
            return redirect(url_for('login'))
        cur.close()
        db.close()
    return render_template('signup.html', error=error)

# ============================================================
# ROUTE 4: Logout
# ============================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================================
# ROUTE 5: Menu
# ============================================================
@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM menu_items WHERE is_available=1")
    items = cur.fetchall()
    cur.close()
    db.close()
    return render_template('menu.html', menu_items=items, user_name=session['user_name'])

# ============================================================
# ROUTE 6: Place Order
# ============================================================
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    data          = request.get_json()
    customer_name = data['name']
    address       = data['address']
    cart          = data['cart']
    total_price   = data['total']
    user_id       = session['user_id']
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO orders (user_id, customer_name, address, total_price)
        VALUES (%s, %s, %s, %s)
    """, (user_id, customer_name, address, total_price))
    order_id = cur.lastrowid
    for item in cart:
        cur.execute("""
            INSERT INTO order_items (order_id, menu_item_id, item_name, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, item['id'], item['name'], item['price'], item['qty']))
    db.commit()
    cur.close()
    db.close()
    return jsonify({'success': True, 'order_id': order_id})

# ============================================================
# ROUTE 7: My Orders
# ============================================================
@app.route('/my_orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, customer_name, address, total_price, status, ordered_at
        FROM orders WHERE user_id=%s ORDER BY ordered_at DESC
    """, (session['user_id'],))
    orders = cur.fetchall()
    cur.close()
    db.close()
    return render_template('my_orders.html', orders=orders)

# ============================================================
# ROUTE 8: Admin Panel
# ============================================================
@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM menu_items")
    items = cur.fetchall()
    cur.execute("SELECT id, customer_name, total_price, status, ordered_at FROM orders ORDER BY ordered_at DESC")
    orders = cur.fetchall()
    cur.close()
    db.close()
    return render_template('admin.html', menu_items=items, orders=orders)

# ============================================================
# ROUTE 9: Admin — Add item
# ============================================================
@app.route('/admin/add_item', methods=['POST'])
def add_item():
    if session.get('is_admin') != 1:
        return redirect(url_for('login'))
    name        = request.form['name']
    category    = request.form['category']
    price       = request.form['price']
    ingredients = request.form['ingredients']
    img         = request.form['img']
    db  = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO menu_items (name, category, price, img, ingredients)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, category, price, img, ingredients))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin'))

# ============================================================
# ROUTE 10: Admin — Delete item
# ============================================================
@app.route('/admin/delete_item/<int:item_id>')
def delete_item(item_id):
    if session.get('is_admin') != 1:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM menu_items WHERE id=%s", (item_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin'))

# ============================================================
# ROUTE 11: Admin — Toggle item visibility
# ============================================================
@app.route('/admin/toggle_item/<int:item_id>')
def toggle_item(item_id):
    if session.get('is_admin') != 1:
        return redirect(url_for('login'))
    db  = get_db()
    cur = db.cursor()
    cur.execute("UPDATE menu_items SET is_available = 1 - is_available WHERE id=%s", (item_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('admin'))

# ============================================================
# START SERVER
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
