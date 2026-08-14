# Shruja Couture

A modern fashion e-commerce platform built with Django, designed for seamless online shopping and elegant product presentation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.2.15-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## About The Project

Shruja Couture is a full-featured fashion e-commerce website developed to provide customers with a smooth shopping experience while giving administrators complete control over products, orders, and customer management.

The platform focuses on modern UI design, responsive layouts, secure authentication, wishlist functionality, shopping cart management, order processing, and online payments.

Shruja Couture was developed as a scalable fashion e-commerce platform featuring secure user authentication, wishlist management, shopping cart functionality, order processing, and PostgreSQL-powered data management.

---

## ✨ Features

### Customer Features

- User Registration & Login
- Profile Management
- Product Browsing
- Category-based Shopping
- Product Detail Pages
- Wishlist Management
- Shopping Cart
- Checkout Process
- Order Tracking
- Order History
- Contact Form

### Admin Features

- Product Management
- Category Management
- Inventory Management
- Order Management
- Customer Management
- Dashboard Analytics

### Upcoming Features

- Razorpay Payment Gateway
- Email Notifications
- Product Reviews & Ratings
- Discount Coupons
- Advanced Search & Filters

---

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- PostgreSQL

### Tools & Services

- Git
- GitHub
- Razorpay Integration (Under Development)

---

## 📂 Project Structure

```text
ShrujaCouture/
│
├── accounts/
├── cart/
├── checkout/
├── core/
├── dashboard/
├── orders/
├── payments/
├── products/
├── wishlist/
│
├── static/
├── templates/
│
├── manage.py
└── config/
```

---

## Installation

## Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password

RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

Do not commit the actual `.env` file to GitHub.

### Clone Repository

```bash
git clone https://github.com/Aly-more/ShrujaCouture.git
```

### Navigate To Project

```bash
cd ShrujaCouture
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

---

## Application Preview

Screenshots will be added after final UI polishing and deployment.

## Security

Sensitive information such as:

- API Keys
- Secret Keys
- Email Credentials
- Payment Credentials

are stored using environment variables and are not committed to GitHub.

---

## Roadmap

- [x] User Authentication
- [x] Product Catalog
- [x] Wishlist
- [x] Cart System
- [x] Checkout Flow
- [x] Order Management
- [ ] Razorpay Integration
- [ ] Email Notifications
- [ ] Deployment

---

## Developer

**Aalisha More**

Masters in Computer Application
Thakur Institute of Management Studies, Career Development and Research, Mumbai

GitHub: https://github.com/Aly-more

---

## 📜 License

This project is developed for educational and portfolio purposes.

© 2026 Shruja Couture. All Rights Reserved.