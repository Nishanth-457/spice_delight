# Spice Delight 🍛

A full-stack restaurant ordering web app built for the **CS1211 Database Management Systems** course at RV University.

**Stack:** Python · Flask · MySQL (PyMySQL) · HTML/CSS/JavaScript · Bootstrap 5

## Features

**Customers**
- Sign up / log in (passwords are hashed, never stored as plain text)
- Menu grouped into sections: Starters, Main Course, Biryani & Rice, Breads, Desserts, Beverages
- Cart and checkout; the delivery name and address are saved and auto-filled on the next order
- "My Orders" page with order history and status

**Admin**
- Add new menu items, delete items, and hide/show items that are unavailable
- View all incoming orders

## Database design

Four tables: `users`, `menu_items`, `orders`, `order_items`.

- `orders` ↔ `order_items` is one-to-many, so a single order can contain many dishes.
- `order_items` stores the item name and price **at the time of ordering**, so later menu price changes don't rewrite old orders.
- Placing an order is a **transaction**: the order row, every order item, and the saved address are committed together, or rolled back together if anything fails.
- All queries are parameterised (`%s` placeholders) to prevent SQL injection.
- Prices are always read from the database on the server, never trusted from the browser.

## Run it locally

1. Create the database: open MySQL and run `spice_delight (1).sql`.
2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in this folder:
   ```
   MYSQLPASSWORD=your_mysql_root_password
   FLASK_SECRET_KEY=any_long_random_string
   ```
4. Optional: `python3 check_setup.py` checks that Flask, PyMySQL and the database tables are set up.
5. Start the app: `python3 app.py` and open http://127.0.0.1:5000

See `HOW_TO_RUN.txt` for more detail.

## Known limitations

- Passwords use plain SHA-256; a production app should use a salted, slow hash such as bcrypt (`werkzeug.security`).
- Admin delete/toggle actions use GET links; a production app should use POST with CSRF protection.
- Runs on Flask's development server only.
