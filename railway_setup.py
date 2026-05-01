# ============================================================
#  railway_setup.py — Run this ONCE to create tables on Railway
#  Run: python3 railway_setup.py
# ============================================================

import pymysql
import hashlib

conn = pymysql.connect(
    host     = 'switchyard.proxy.rlwy.net',
    user     = 'root',
    password = 'SaKyjNPtmbZAVJTQqGbDCzIljnZJNvgi',
    database = 'railway',
    port     = 48303
)

cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category ENUM('veg','non-veg') NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    img VARCHAR(255),
    ingredients TEXT,
    is_available TINYINT(1) DEFAULT 1
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    total_price DECIMAL(8,2) NOT NULL,
    status ENUM('placed','preparing','delivered') DEFAULT 'placed',
    ordered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
)""")

# Admin account
pw = hashlib.sha256('admin123'.encode()).hexdigest()
cur.execute("SELECT id FROM users WHERE email='admin@spicedelight.com'")
if not cur.fetchone():
    cur.execute("INSERT INTO users (name,email,password,is_admin) VALUES (%s,%s,%s,%s)",
                ('Admin','admin@spicedelight.com', pw, 1))

# Menu items
cur.execute("SELECT COUNT(*) FROM menu_items")
if cur.fetchone()[0] == 0:
    items = [
        ('Paneer Tikka','veg',280,'images/PannerTikka.jpg','Paneer, Yogurt, Spices, Capsicum'),
        ('Chicken 65','non-veg',320,'images/Chicken65.jpg','Chicken, Curry Leaves, Red Chili'),
        ('Veg Biryani','veg',250,'images/VegBiryani.jpg','Basmati Rice, Mixed Vegetables, Spices'),
        ('Mutton Seekh','non-veg',450,'images/MuttonSeekh.jpg','Minced Mutton, Spices, Onion, Herbs'),
        ('Spring Rolls','veg',180,'images/SpringRolls.jpg','Cabbage, Carrot, Flour Wrapper'),
        ('Fish Fry','non-veg',380,'images/FishFingers.jpg','Fish Fillet, Breadcrumbs, Spices'),
        ('Samosa Chat','veg',60,'images/samosa-chat.jpg','Potatoes, Peas, Flour, Spices'),
        ('Chicken Tikka','non-veg',300,'images/ChickenTikka.jpg','Boneless Chicken, Yogurt, Tandoori Masala'),
        ('Hara Bhara Kabab','veg',220,'images/HaraBharaKabab.jpg','Spinach, Green Peas, Potatoes'),
        ('Prawn Fry','non-veg',420,'images/PrawnsFry.jpg','Prawns, Garlic, Red Chili, Lemon'),
        ('Gobi 65','veg',200,'images/Gobi65.jpg','Cauliflower, Soy Sauce, Garlic, Chili'),
        ('Tandoori Chicken','non-veg',500,'images/TandooriChicken.jpg','Whole Chicken, Yogurt, Lemon, Spices'),
        ('Dal Makhani','veg',280,'images/DalMakhani.jpg','Black Lentils, Butter, Cream, Tomatoes'),
        ('Paneer Butter Masala','veg',320,'images/PaneerButterMasala.jpg','Paneer, Butter, Cashew Paste, Cream'),
        ('Palak Paneer','veg',300,'images/PalakPaneer.jpg','Spinach, Paneer, Garlic, Cream'),
        ('Malai Kofta','veg',330,'images/MalaiKofta.jpg','Potato, Paneer, Cream, Cashew Nut'),
        ('Dal Tadka','veg',240,'images/DalTadka.jpg','Chickpeas, Onion, Tomato, Spices'),
        ('Aloo Gobi','veg',220,'images/AlooGobi.jpg','Potatoes, Cauliflower, Turmeric, Cumin'),
        ('Butter Chicken','non-veg',380,'images/ButterChicken.jpg','Chicken, Butter, Tomato Puree, Cream'),
        ('Mutton Rogan Josh','non-veg',480,'images/MuttonRoganJosh.jpg','Mutton, Kashmiri Chili, Yogurt, Spices'),
        ('Chicken Curry','non-veg',360,'images/ChickenCurry.jpg','Chicken, Yogurt, Almond Paste, Spices'),
        ('Fish Curry','non-veg',400,'images/FishCurry.jpg','Fish, Coconut Milk, Tamarind, Mustard'),
        ('Chicken Biryani','non-veg',350,'images/ChickenBiryani.jpg','Chicken, Basmati Rice, Saffron, Spices'),
        ('Egg Curry','non-veg',210,'images/EggCurry.jpg','Boiled Eggs, Tomato Gravy, Spices'),
        ('Garlic Naan','veg',60,'images/GarlicNaan.jpg','Flour, Garlic, Butter'),
        ('Butter Naan','veg',50,'images/ButterNaan.jpg','Flour, Butter, Sesame Seeds'),
        ('Tandoori Roti','veg',40,'images/TandooriRoti.jpg','Whole Wheat Flour'),
        ('Jeera Rice','veg',180,'images/JeeraRice.jpg','Basmati Rice, Cumin Seeds, Ghee'),
        ('Gulab Jamun','veg',120,'images/GulabJamun.jpg','Milk Solids, Sugar Syrup, Cardamom'),
        ('Rasgulla','veg',120,'images/Rasgulla.jpg','Chenna, Sugar Syrup'),
        ('Gajar Ka Halwa','veg',150,'images/GajarHalwa.jpg','Carrots, Milk, Sugar, Nuts'),
        ('Rasmalai','veg',160,'images/Rasmalai.jpg','Chenna, Milk, Saffron, Pistachios'),
        ('Mango Lassi','veg',100,'images/MangoLassi.jpg','Yogurt, Mango Pulp, Sugar'),
        ('Masala Chai','veg',50,'images/MasalaChai.jpg','Tea Leaves, Milk, Ginger, Cardamom'),
        ('Fresh Lime Soda','veg',80,'images/LimeSoda.jpg','Lemon, Soda, Salt/Sugar'),
        ('Cold Coffee','veg',140,'images/ColdCoffee.jpg','Coffee, Milk, Ice Cream, Chocolate'),
    ]
    cur.executemany("""
        INSERT INTO menu_items (name,category,price,img,ingredients)
        VALUES (%s,%s,%s,%s,%s)
    """, items)

conn.commit()
cur.close()
conn.close()
print("✅ Railway database setup complete!")
