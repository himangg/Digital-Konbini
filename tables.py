import sqlite3

conn = sqlite3.connect('Digital_Konbini.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Supplier (
                    Supplier_ID INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    mobile_number TEXT UNIQUE NOT NULL,
                    address TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Product (
                    Product_ID INTEGER PRIMARY KEY,
                    Supplier_ID INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL NOT NULL,
                    details TEXT,
                    quantity_remaining INTEGER NOT NULL,
                    discount_percentage REAL,
                    FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Customer (
                    Customer_ID INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    Mobile_number TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    address TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                    Order_ID INTEGER PRIMARY KEY,
                    Customer_ID INTEGER NOT NULL,
                    Payment_Date DATE,
                    Payment_PID INTEGER,
                    Delivered_Date DATE,
                    Coupon_Code_Applied TEXT,
                    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Product_Order_Bridge_Table (
                    Order_ID INTEGER,
                    Product_ID INTEGER,
                    Quantity INTEGER,
                    PRIMARY KEY (Order_ID, Product_ID),
                    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
                    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Admins (
                    Admin_ID INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Coupons (
                    Code TEXT PRIMARY KEY,
                    Admin_ID INTEGER NOT NULL,
                    Flat_Discount REAL NOT NULL,
                    Minimum_cart_value REAL NOT NULL,
                    FOREIGN KEY (Admin_ID) REFERENCES Admins(Admin_ID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Wishlist_Customer_Product_Bridge_Table (
                    Wishlist_ID INTEGER PRIMARY KEY,
                    Customer_ID INTEGER NOT NULL,
                    Product_ID INTEGER NOT NULL,
                    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
                    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
                )''')
 
conn.commit()
conn.close()

