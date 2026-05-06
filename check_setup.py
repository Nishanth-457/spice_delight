import sys
print("=" * 50)
print("  Spice Delight — Setup Checker")
print("=" * 50)

# Check 1: Python
print(f"\n[1] Python version: {sys.version.split()[0]}", end="  ")
print("✅ OK" if sys.version_info >= (3,7) else "❌ Need Python 3.7+")

# Check 2: Flask
try:
    import flask
    print(f"[2] Flask: ✅ OK")
except ImportError:
    print("[2] Flask: ❌  Run: pip3 install Flask")
    sys.exit()

# Check 3: PyMySQL
try:
    import pymysql
    print(f"[3] PyMySQL: ✅ OK")
except ImportError:
    print("[3] PyMySQL: ❌  Run: pip3 install PyMySQL")
    sys.exit()

# Check 4: MySQL connection
print("\n[4] Testing MySQL connection...")
DB_PASSWORD = ''   # change this if your MySQL has a password

try:
    conn = pymysql.connect(host='localhost', user='root',
                           password='nishanth@rvu', database='spice_delight')
    cur = conn.cursor()
    for table in ['users','menu_items','orders','order_items']:
        cur.execute(f"SHOW TABLES LIKE '{table}'")
        r = cur.fetchone()
        print(f"    Table '{table}': {'✅ exists' if r else '❌ NOT found — run spice_delight.sql!'}")
    cur.execute("SELECT COUNT(*) FROM menu_items")
    count = cur.fetchone()[0]
    print(f"    Menu items: {count} {'✅' if count > 0 else '❌ run the SQL file!'}")
    cur.execute("SELECT email FROM users WHERE is_admin=1")
    admin = cur.fetchone()
    print(f"    Admin account: {'✅ ' + admin[0] if admin else '❌ run the SQL file!'}")
    conn.close()
    print("\n✅ All good! Now run:  python3 app.py")
except pymysql.err.OperationalError as e:
    print(f"    ❌ MySQL error: {e}")
    print("\n    Fix:")
    print("    1. Make sure MySQL is running")
    print("    2. Run spice_delight.sql in MySQL Workbench first")
    print("    3. If MySQL has a password, update DB_PASSWORD in this file")
