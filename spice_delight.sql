-- ============================================================
--  RUN THESE IN MYSQL WORKBENCH (in order)
--  These add the 'section' column to menu_items
--  and saved address columns to users
-- ============================================================

USE spice_delight;

-- Step 1: Add section column to menu_items
ALTER TABLE menu_items ADD COLUMN section VARCHAR(50) DEFAULT 'Main Course';

-- Step 2: Set sections for all 36 items
UPDATE menu_items SET section = 'Starters' WHERE name IN (
  'Paneer Tikka','Chicken 65','Spring Rolls','Fish Fry','Samosa Chat',
  'Chicken Tikka','Hara Bhara Kabab','Prawn Fry','Gobi 65',
  'Tandoori Chicken','Mutton Seekh'
);
UPDATE menu_items SET section = 'Main Course' WHERE name IN (
  'Dal Makhani','Paneer Butter Masala','Palak Paneer','Malai Kofta',
  'Dal Tadka','Aloo Gobi','Butter Chicken','Mutton Rogan Josh',
  'Chicken Curry','Fish Curry','Egg Curry'
);
UPDATE menu_items SET section = 'Biryani & Rice' WHERE name IN (
  'Veg Biryani','Chicken Biryani','Jeera Rice'
);
UPDATE menu_items SET section = 'Breads' WHERE name IN (
  'Garlic Naan','Butter Naan','Tandoori Roti'
);
UPDATE menu_items SET section = 'Desserts' WHERE name IN (
  'Gulab Jamun','Rasgulla','Gajar Ka Halwa','Rasmalai'
);
UPDATE menu_items SET section = 'Beverages' WHERE name IN (
  'Mango Lassi','Masala Chai','Fresh Lime Soda','Cold Coffee'
);

-- Step 3: Add saved address columns to users
ALTER TABLE users ADD COLUMN saved_name    VARCHAR(100) DEFAULT NULL;
ALTER TABLE users ADD COLUMN saved_address TEXT         DEFAULT NULL;

-- Verify
SELECT name, section FROM menu_items ORDER BY section;
