# 🍽️ Smart Restaurant Management System

Python
Flask
SQLite

A full-stack restaurant management system built using Flask, designed to simulate real-world ordering and admin control systems.

---

## 🎯 Overview

This project demonstrates how to build a complete web application with:

- User interaction (menu, cart, orders)
- Admin control panel
- Database integration
- File upload system
- Session management

---

## ⚡ System Flow

text User → Browse Menu → Add to Cart → Checkout → Order Saved in DB Admin → Login → Dashboard → Manage Orders & Menu 

---

## 🧠 How It Works

### 1. Flask Routing
Each page is handled by a route:

python @app.route("/") def home():     return render_template("index.html") 

---

### 2. Dynamic Templates (Jinja2)

python return render_template("menu.html", menu=menu_items) 

html {% for item in menu %}   <h3>{{ item.name }}</h3> {% endfor %} 

---

### 3. Database Design (SQLite)

#### Tables:

Menu Table
| Column | Type |
|------|------|
| id | INTEGER |
| name | TEXT |
| price | REAL |
| image | TEXT |

Orders Table
| Column | Type |
|------|------|
| id | INTEGER |
| items | TEXT |
| total | REAL |

---

## 🗺️ Database Flow

text Admin adds item → Saved in Menu Table User selects items → Stored in Session Checkout → Saved in Orders Table 

---

## 🛒 Cart System (Sessions)

- Uses Flask session
- Stores selected item IDs
- Temporary storage (per user)

python session["cart"] = [] 

---

## 🖼️ File Upload System

- Images stored in:
text static/uploads/ 

- Code:
python file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 

- Display:
html <img src="{{ url_for('static', filename='uploads/' + item.image) }}"> 

---

## 🔐 Admin Authentication

python if not session.get("admin"):     return redirect("/admin_login") 

Default:
- Username: admin  
- Password: admin123  

---

## 📡 API Routes

| Route | Method | Description |
|------|--------|------------|
| / | GET | Home page |
| /menu | GET | Show menu |
| /add_to_cart | POST | Add item to cart |
| /cart | GET | View cart |
| /checkout | POST | Save order |
| /admin_login | GET/POST | Admin login |
| /admin | GET | Dashboard |

---

## 📁 Project Structure

bash project/ │── app.py │── database.db │── requirements.txt │ ├── templates/ │   ├── index.html │   ├── menu.html │   ├── cart.html │   ├── admin.html │ ├── static/ │   ├── uploads/ │   ├── css/ 

---

## ⚙️ Setup

bash pip install -r requirements.txt python app.py 

Open:
http://127.0.0.1:5000

---

## 📊 Admin Dashboard

Features:
- View total revenue
- View orders
- Add new items

---

## 📸 Screenshots

![Admin Dashboard] <img width="1365" height="767" alt="WhatsApp Image 2026-05-12 at 10 51 07 AM" src="https://github.com/user-attachments/assets/0807300d-7da1-408b-b62a-0a8211f95060" />

---

## 🚀 Future Improvements

- User authentication system
- Payment integration
- Order tracking
- REST API conversion
- Better UI/UX

---

## 🎓 What You Learn From This Project

- Flask fundamentals
- MVC-like structure
- Sessions & authentication
- Database integration
- Dynamic HTML rendering

---

