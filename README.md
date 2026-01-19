🛒 Django Ecommerce Web Application

---
A full-stack Ecommerce web application built using Django and MySQL, featuring user authentication, product management, cart functionality, and admin control.

---
🚀 Features

User Registration & Login

Product Listing & Details

Add to Cart & Checkout

Order Management

Admin Dashboard

Responsive UI

Secure Authentication

MySQL Database Integration

---
🛠️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap

Database: MySQL

Version Control: Git & GitHub

---
🖼️ Screenshots
🏠 home.png
🔐about.png

---
📂 Project Structure
Django/
│── manage.py
│── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│── products/
│── users/
│── templates/
│── static/
│── screenshots/
│── requirements.txt
│── .gitignore
│── README.md

---
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Create & activate virtual environment
python -m venv .env
.env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure database (MySQL)

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create superuser
python manage.py createsuperuser

7️⃣ Run server
python manage.py runserver

---

Open browser:

http://127.0.0.1:8000/

---

