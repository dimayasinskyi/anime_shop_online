# 🛒 anime_shop_online

**anime_shop_online** is a fully functional anime merchandise e-commerce platform built with Django. It includes all core features of a modern online store: user authentication, product listings, search, cart, order system with test payments, user profile, comments, and basic API.

## 📸 Screenshots

### 🏠 Home page
![Home Page]()

### 🛍️ Catalog
![Catalog]()

### 🛒 Cart and Checkout
![Basket]()

### 👤 User Profile
![Profile]()

---

## 🚀 Features

- 🔐 Registration/login via email and Google
- 👤 User profile with avatar, profile editing, and order history
- 🛍️ Product catalog:
  - Pagination
  - Search by product name
  - Category filtering via URL parameters
- 🛒 Shopping cart:
  - Add/remove products
  - Order directly or from cart
- 💳 Order system:
  - Address confirmation before payment
  - Test payment service integration
- 💬 Comments section on each product page
- ❤️ Favorites (wishlist)
- 📦 Basic API for integration (e.g. Telegram bot)
- 🧩 Django templates, forms, admin

---

## 🛠 Technologies Used

- **Backend:** Django (Function-Based Views)
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap
- **Other tools:** Git, GitHub, simple model tests, basic Docker usage

---

## ⚙️ How to Run Locally

```bash
git clone https://github.com/dimayasinskyi/anime_shop_online
cd anime_shop_online
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pipenv install
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
