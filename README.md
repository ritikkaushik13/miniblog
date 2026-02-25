# Mini Blog Platform – Django REST API

A mini blog platform built using Django and Django REST Framework with User Authentication, 2FA OTP login, Likes, Comments, REST APIs, Swagger documentation, and Docker support.

---

## 🚀 Features

- User Registration
- User Login with 2FA OTP verification
- Authenticated users can:
  - Create blog posts
  - Edit their own posts
  - Delete their own posts
- Authenticated users can:
  - View all posts
  - Like posts
  - Comment on posts
- RESTful API (GET, POST, PUT, DELETE)
- Strict validation and proper error handling
- Swagger API Documentation
- Dockerized project
- SQLite Database

---

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Docker
- Swagger

---

## 📂 Project Structure

```
miniblog/
│
├── blog/              # Blog app (Posts, Likes, Comments)
├── miniblog/           # Django project settings
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Setup Instructions (Without Docker)

### 1️⃣ Clone Repository

```
git clone repo-link
cd mini-blog
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```
python manage.py migrate
```

### 5️⃣ Start Server

```
python manage.py runserver
```

Server will run at:
```
http://127.0.0.1:8000/
```

---

## 🐳 Run Using Docker

Make sure Docker is installed.

### Build and Run

```
docker compose up --build
```

Application will be available at:
```
http://localhost:8000/
```

---

## 🔐 Authentication Flow

1. Register User
2. Login with username & password
3. Receive OTP
4. Verify OTP
5. Receive Authentication Token
6. Use token in headers:

```
Authorization: Token <your_token_here>
```

---

## 📌 API Endpoints

### User APIs
- POST `/api/register/`
- POST `/api/login/`
- POST `/api/verify-otp/`

### Blog APIs
- POST `/api/posts/create/`
- PUT `/api/posts/<id>/edit/`
- DELETE `/api/posts/<id>/delete/`
- GET `/api/posts/`
- GET `/api/posts/<id>/`

### Like & Comment APIs
- POST `/api/posts/<id>/like/`
- POST `/api/posts/<id>/comment/`

---

## 📖 Swagger Documentation

Swagger UI available at:

```
http://localhost:8000/swagger/
```

---


## 🔒 Validation & Security

- Field-level validation
- Proper serializer validation
- Authenticated access required for protected endpoints
- Users can edit/delete only their own posts
- Token-based authentication
- Environment variables used for sensitive data

---
