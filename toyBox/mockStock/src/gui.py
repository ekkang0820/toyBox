import tkinter as tk
from hashlib import sha256
from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mysql.connector import connect, Error

from mockStock.src.api import get_stock_data, get_top_gainers_and_losers
from mockStock.src.investment import MockInvestment

current_user_id = None


def connect_db():
    return connect(
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
        messagebox.showinfo("Success", "User registered successfully!")
    except Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


def login_user(email, password):
    global current_user_id
    db = connect_db()
    cursor = db.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("SELECT user_id, name FROM users WHERE email=%s AND password=%s", (email, hashed_password))
        user = cursor.fetchone()
        if user:
            current_user_id = user[0]
            messagebox.showinfo("Success", f"Login successful! Welcome {user[1]}")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid email or password")
    except Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


def buy_stock(user_id, symbol, quantity, purchase_price):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO purchased_stocks (user_id, symbol, quantity, purchase_price) VALUES (%s, %s, %s, %s)",
            (user_id, symbol, quantity, purchase_price))
        db.commit()
        messagebox.showinfo("Success", "Stock purchased successfully!")
    except Error as err:
        messagebox.showerror("Error", f"Error: {err}")
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
            cursor.execute("UPDATE purchased_stocks SET quantity = quantity - %s WHERE user_id = %s AND symbol = %s",
                           (quantity, user_id, symbol))
            cursor.execute("DELETE FROM purchased_stocks WHERE quantity = 0")
            db.commit()
            messagebox.showinfo("Success", "Stock sold successfully!")
        else:
            messagebox.showerror("Error", "Not enough stock to sell")
    except Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


def show_register_form():
    def register():
        email = entry_email.get()
        password = entry_password.get()
        name = entry_name.get()
        register_user(email, password, name)
        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Email:").grid(row=0, column=0, padx=5, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(register_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(register_window, text="Name:").grid(row=2, column=0, padx=5, pady=5)
    entry_name = tk.Entry(register_window)
    entry_name.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(register_window, text="Register", command=register).grid(row=3, columnspan=2, pady=10)


def show_login_form():
    def login():
        email = entry_email.get()
        password = entry_password.get()
        login_user(email, password)

    global login_window
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Email:").grid(row=0, column=0, padx=5, pady=5)
    entry_email = tk.Entry(login_window)
    entry_email.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)


def show_buy_form():
    def buy():
        symbol = entry_symbol.get()
        quantity = int(entry_quantity.get())
        purchase_price = float(entry_purchase_price.get())
        buy_stock(current_user_id, symbol, quantity, purchase_price)
        buy_window.destroy()

    buy_window = tk.Toplevel(root)
    buy_window.title("Buy Stock")

    tk.Label(buy_window, text="Symbol:").grid(row=0, column=0, padx=5, pady=5)
    entry_symbol = tk.Entry(buy_window)
    entry_symbol.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(buy_window, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(buy_window)
    entry_quantity.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(buy_window, text="Purchase Price:").grid(row=2, column=0, padx=5, pady=5)
    entry_purchase_price = tk.Entry(buy_window)
    entry_purchase_price.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(buy_window, text="Buy", command=buy).grid(row=3, columnspan=2, pady=10)


def show_sell_form():
    def sell():
        symbol = entry_symbol.get()
        quantity = int(entry_quantity.get())
        sell_price = float(entry_sell_price.get())
        sell_stock(current_user_id, symbol, quantity, sell_price)
        sell_window.destroy()

    sell_window = tk.Toplevel(root)
    sell_window.title("Sell Stock")

    tk.Label(sell_window, text="Symbol:").grid(row=0, column=0, padx=5, pady=5)
    entry_symbol = tk.Entry(sell_window)
    entry_symbol.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(sell_window, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(sell_window)
    entry_quantity.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(sell_window, text="Sell Price:").grid(row=2, column=0, padx=5, pady=5)
    entry_sell_price = tk.Entry(sell_window)
    entry_sell_price.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(sell_window, text="Sell", command=sell).grid(row=3, columnspan=2, pady=10)


def search_stock():
    symbol = entry_symbol.get().upper()
    data = get_stock_data(symbol)
    if data is not None:
        plot_stock_data(data)
    else:
        messagebox.showerror("Error", "Failed to retrieve stock data")


def plot_stock_data(data):
    fig, ax = plt.subplots()
    data['close'].plot(ax=ax)
    ax.set_title('Stock Price')
    ax.set_ylabel('Price')
    ax.set_xlabel('Date')
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)


def update_portfolio():
    portfolio, balance = investment.show_portfolio()
    label_portfolio.config(text=f"Portfolio: {portfolio}\nBalance: ${balance:.2f}")


def display_top_gainers_and_losers():
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NFLX']  # 분석할 주식 심볼 리스트
    gainers, losers = get_top_gainers_and_losers(symbols)

    gainers_text = "Top Gainers:\n" + "\n".join([f"{g['symbol']}: {g['change']:.2f}%" for g in gainers])
    losers_text = "Top Losers:\n" + "\n".join([f"{l['symbol']}: {l['change']:.2f}%" for l in losers])

    label_gainers.config(text=gainers_text)
    label_losers.config(text=losers_text)


# GUI 설정
root = tk.Tk()
root.title("Mock Investment")

frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

frame_graph = tk.Frame(root)
frame_graph.pack(padx=10, pady=10)

frame_portfolio = tk.Frame(root)
frame_portfolio.pack(padx=10, pady=10)

frame_gainers_losers = tk.Frame(root)
frame_gainers_losers.pack(padx=10, pady=10)

label_symbol = tk.Label(frame_input, text="Symbol:")
label_symbol.grid(row=0, column=0, padx=5, pady=5)

entry_symbol = tk.Entry(frame_input)
entry_symbol.grid(row=0, column=1, padx=5, pady=5)

label_quantity = tk.Label(frame_input, text="Quantity:")
label_quantity.grid(row=1, column=0, padx=5, pady=5)

entry_quantity = tk.Entry(frame_input)
entry_quantity.grid(row=1, column=1, padx=5, pady=5)

button_search = tk.Button(frame_input, text="Search", command=search_stock)
button_search.grid(row=2, column=0, padx=5, pady=5)

button_buy = tk.Button(frame_input, text="Buy", command=show_buy_form)
button_buy.grid(row=2, column=1, padx=5, pady=5)

button_sell = tk.Button(frame_input, text="Sell", command=show_sell_form)
button_sell.grid(row=2, column=2, padx=5, pady=5)

button_register = tk.Button(frame_input, text="Register", command=show_register_form)
button_register.grid(row=3, column=0, padx=5, pady=10)

button_login = tk.Button(frame_input, text="Login", command=show_login_form)
button_login.grid(row=3, column=1, padx=5, pady=10)

label_portfolio = tk.Label(frame_portfolio, text="Portfolio:")
label_portfolio.pack(pady=10)

label_gainers = tk.Label(frame_gainers_losers, text="Top Gainers:")
label_gainers.pack(side=tk.LEFT, padx=10)

label_losers = tk.Label(frame_gainers_losers, text="Top Losers:")
label_losers.pack(side=tk.RIGHT, padx=10)

# 초기 투자 금액 설정
investment = MockInvestment(initial_balance=10000)
update_portfolio()
display_top_gainers_and_losers()

def run():
    root.mainloop()

