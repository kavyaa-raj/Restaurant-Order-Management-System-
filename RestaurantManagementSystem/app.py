from flask import Flask, render_template, request, redirect
from database import create_database
import sqlite3

app = Flask(__name__)

create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu")
    food_items = cursor.fetchall()

    conn.close()

    return render_template(
        "menu.html",
        food_items=food_items
    )


@app.route("/add_food", methods=["POST"])
def add_food():
    food_name = request.form["food_name"]
    category = request.form["category"]
    price = request.form["price"]

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO menu (food_name, category, price) VALUES (?, ?, ?)",
        (food_name, category, price)
    )

    conn.commit()
    conn.close()

    return redirect("/menu")


@app.route("/orders")
def orders():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()

    conn.close()

    return render_template(
        "orders.html",
        menu_items=menu_items
    )


@app.route("/place_order", methods=["POST"])
def place_order():

    customer_name = request.form["customer_name"]
    food_name = request.form["food_name"]
    quantity = int(request.form["quantity"])

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT price FROM menu WHERE food_name=?",
        (food_name,)
    )

    price = cursor.fetchone()[0]

    total_price = price * quantity

    cursor.execute("""
    INSERT INTO orders
    (customer_name, food_name, quantity, total_price)
    VALUES (?, ?, ?, ?)
    """, (
        customer_name,
        food_name,
        quantity,
        total_price
    ))

    conn.commit()
    conn.close()

    return redirect("/bill")


@app.route("/bill")
def bill():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT customer_name,
           food_name,
           quantity,
           total_price
    FROM orders
    ORDER BY id DESC
    LIMIT 1
    """)

    order = cursor.fetchone()

    conn.close()

    subtotal = order[3]
    gst = subtotal * 0.05
    final_amount = subtotal + gst

    return render_template(
        "bill.html",
        order=order,
        subtotal=subtotal,
        gst=gst,
        final_amount=final_amount
    )


@app.route("/history")
def history():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT customer_name,
           food_name,
           quantity,
           total_price
    FROM orders
    """)

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        orders=orders
    )


if __name__ == "__main__":
    app.run(debug=True)