# 💳 Payment Module – Django Backend Assignment

A complete backend **Payment Module** built using **Django REST Framework** and **PostgreSQL**, implementing real-world payment concepts such as idempotency, order-level validation, and refund handling.

---

## 📌 Project Overview

This project implements a simple and robust Payment Module that supports:

- Payment creation
- Payment status tracking
- Order-wise payment retrieval
- Refund functionality

The system is designed with **idempotency support** to avoid duplicate payments and ensure data consistency.

---

## 🛠️ Technology Stack

- **Python 3.7.0**
- **Django 3.2.25**
- **Django REST Framework**
- **PostgreSQL**
- **psycopg2-binary**
- **Postman** (API testing)

---


## ⚙️ Project Setup (Step-by-Step)

1. Install **Python 3.7.0** and ensure it is added to PATH.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate


### Clone the project repository from GitHub.

### Install dependencies:
```bash
pip install -r requirements.txt
```


Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```


### Update database credentials in settings.py.

Run database migrations.
```bash
python manage.py makemigrations
python manage.py migrate
```
Start the Django development server.
```bash
python manage.py runserver
```
## ▶️ Execution Commands
```bash
pip install -r requirements.txt
pip install psycopg2-binary
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
Server will start at:

http://127.0.0.1:8000/

## 🔗 API Endpoints

POST /payments/ – Create a new payment

GET /payments/ – List all payments

GET /payments/{id}/ – Get payment details

GET /payments/order/{order_id}/ – Get payments by order

POST /payments/{id}/refund/ – Refund a successful payment

PATCH /payments/{id}/ – Update payment status

## 🧠 Business Rules Implemented

Idempotency key prevents duplicate payment creation.

Only one successful payment is allowed per order.

Payments with status other than SUCCESS cannot be refunded.

Refunded payments are marked as REFUNDED.

## 🧪 Testing

All APIs can be tested using Postman.

Sample requests are provided in api_test_examples.txt.

Ensure the Django server is running before testing.

## Conclusion

This assignment demonstrates:

Backend payment flow design

REST API development

Database interaction

Real-world concepts such as idempotency and refund handling

The project follows clean backend practices and is suitable for technical evaluations and interviews.


   # 👤 Author
   ## Prasad Naidu                                                                                                                          

                                                                                                                              


---


