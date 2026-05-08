from flask import Flask, render_template, redirect, session, request
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================
# 🧠 HELPER
# =========================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# 🗄️ DATABASE
# =========================
def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        image TEXT
    )
    """)

    # ✅ UPDATED
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        items TEXT,
        total INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    return render_template(
        "index.html",
        name=session.get("name", "Guest"),
        user=session.get("user")
    )

# =========================
# 🔐 AUTH
# =========================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            session["name"] = user["name"]
            return redirect("/")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (name,username,password) VALUES (?,?,?)",
                  (name,username,password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# 🍔 MENU
# =========================
@app.route("/menu")
def menu_page():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM menu")
    items = c.fetchall()
    conn.close()

    return render_template("menu.html", menu=items, user=session.get("user"))

# =========================
# 🛒 CART
# =========================
@app.route("/add/<int:id>")
def add(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    session.modified = True
    return redirect("/menu")

@app.route("/remove/<int:id>")
def remove(id):
    if id in session.get("cart", []):
        session["cart"].remove(id)
        session.modified = True
    return redirect("/cart")

@app.route("/cart")
def cart():
    conn = get_db()
    c = conn.cursor()

    items = []
    total = 0

    for item_id in session.get("cart", []):
        c.execute("SELECT * FROM menu WHERE id=?", (item_id,))
        item = c.fetchone()
        if item:
            items.append(item)
            total += item["price"]

    conn.close()

    return render_template("cart.html", items=items, total=total, user=session.get("user"))

# =========================
# 💳 PAYMENT
# =========================
@app.route("/payment")
def payment():
    return render_template("payment.html", user=session.get("user"))

@app.route("/pay", methods=["POST"])
def pay():
    return redirect("/checkout")

# =========================
# ✅ CHECKOUT (UPDATED)
# =========================
@app.route("/checkout")
def checkout():
    conn = get_db()
    c = conn.cursor()

    items_list = []
    total = 0

    for item_id in session.get("cart", []):
        c.execute("SELECT * FROM menu WHERE id=?", (item_id,))
        item = c.fetchone()
        if item:
            items_list.append(item["name"])
            total += item["price"]

    items_text = ", ".join(items_list)

    c.execute("INSERT INTO orders (items,total,status) VALUES (?,?,?)",
              (items_text,total,"pending"))

    conn.commit()
    conn.close()

    session["cart"] = []

    return render_template("checkout.html", total=total, user=session.get("user"))

# =========================
# 👨‍🍳 ADMIN
# =========================

@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin")
    return render_template("admin_login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin_login")

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM orders")
    orders = c.fetchall()

    c.execute("SELECT SUM(total) as total FROM orders")
    revenue = c.fetchone()["total"] or 0

    c.execute("SELECT * FROM menu")
    items = c.fetchall()

    conn.close()

    return render_template("admin.html", orders=orders, revenue=revenue, items=items)

# ✅ COMPLETE ORDER
@app.route("/complete_order/<int:id>")
def complete_order(id):
    if not session.get("admin"):
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    c.execute("UPDATE orders SET status='done' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")

# =========================
# 🔥 FIX ADD ITEM
# =========================
@app.route("/add_item", methods=["POST"])
def add_item():
    if not session.get("admin"):
        return redirect("/")

    name = request.form.get("name")
    price = request.form.get("price")

    file = request.files.get("image")

    if file and file.filename != "":
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    else:
        filename = "default.jpg"

    conn = get_db()
    c = conn.cursor()

    c.execute("INSERT INTO menu (name,price,image) VALUES (?,?,?)",
              (name,price,filename))

    conn.commit()
    conn.close()

    return redirect("/admin")

# ❌ DELETE
@app.route("/delete_item/<int:id>")
def delete_item(id):
    if not session.get("admin"):
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM menu WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# ✏️ EDIT
@app.route("/edit_item/<int:id>", methods=["POST"])
def edit_item(id):
    if not session.get("admin"):
        return redirect("/")

    name = request.form["name"]
    price = request.form["price"]

    conn = get_db()
    c = conn.cursor()

    c.execute("UPDATE menu SET name=?, price=? WHERE id=?",
              (name,price,id))

    conn.commit()
    conn.close()

    return redirect("/admin")

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)