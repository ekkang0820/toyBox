import mysql.connector


def initialize_db():
    db = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password"
    )

    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS StockTrading")
    cursor.execute("USE StockTrading")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchased_stocks (
        stock_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        symbol VARCHAR(10),
        quantity INT,
        purchase_price DECIMAL(10, 2),
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    initialize_db()
