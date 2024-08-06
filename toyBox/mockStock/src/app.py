import mysql.connector
from getpass import getpass
from hashlib import sha256

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="eksldpf1!",
        database="StockTrading"
    )

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def register_user(email, password, name):
    db = connect_db()
    cursor = db.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, hashed_password, name))
        db.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def login_user(email, password):
    db = connect_db()
    cursor = db.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("SELECT user_id, name FROM users WHERE email=%s AND password=%s", (email, hashed_password))
        user = cursor.fetchone()
        if user:
            print(f"Login successful! Welcome {user[1]}")
            return user[0]
        else:
            print("Invalid email or password")
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def buy_stock(user_id, symbol, quantity, purchase_price):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO purchased_stocks (user_id, symbol, quantity, purchase_price) VALUES (%s, %s, %s, %s)",
                       (user_id, symbol, quantity, purchase_price))
        db.commit()
        print("Stock purchased successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def sell_stock(user_id, symbol, quantity, sell_price):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT quantity FROM purchased_stocks WHERE user_id=%s AND symbol=%s", (user_id, symbol))
        stock = cursor.fetchone()
        if stock and stock[0] >= quantity:
            cursor.execute("UPDATE purchased_stocks SET quantity = quantity - %s WHERE user_id = %s AND symbol = %s", (quantity, user_id, symbol))
            cursor.execute("DELETE FROM purchased_stocks WHERE quantity = 0")
            db.commit()
            print("Stock sold successfully!")
        else:
            print("Not enough stock to sell")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    print("1. Register User")
    print("2. Login User")
    print("3. Buy Stock")
    print("4. Sell Stock")
    choice = input("Enter choice: ")

    if choice == "1":
        email = input("Enter email: ")
        password = getpass("Enter password: ")
        name = input("Enter name: ")
        register_user(email, password, name)
    elif choice == "2":
        email = input("Enter email: ")
        password = getpass("Enter password: ")
        user_id = login_user(email, password)
        if user_id:
            print(f"Logged in with user ID: {user_id}")
    elif choice == "3":
        user_id = int(input("Enter user ID: "))
        symbol = input("Enter stock symbol: ")
        quantity = int(input("Enter quantity: "))
        purchase_price = float(input("Enter purchase price: "))
        buy_stock(user_id, symbol, quantity, purchase_price)
    elif choice == "4":
        user_id = int(input("Enter user ID: "))
        symbol = input("Enter stock symbol: ")
        quantity = int(input("Enter quantity: "))
        sell_price = float(input("Enter sell price: "))
        sell_stock(user_id, symbol, quantity, sell_price)
