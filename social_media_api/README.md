Here is a **professional, production-ready README.md** tailored exactly to your project requirements.

You can copy this directly into your `README.md` file.

---

# 📱 Social Media API

A Django REST Framework–based Social Media API supporting user authentication and profile management.

---

## 📌 Project Overview

This project is a backend Social Media API built with **Django** and **Django REST Framework (DRF)**.

It implements:

* Custom user model
* Token-based authentication
* User registration and login
* Profile retrieval and update
* Foundation for social features (followers, posts, comments, notifications)

The API is designed following REST principles and production-ready best practices.

---

## 🛠 Tech Stack

* Python 3.x
* Django
* Django REST Framework
* DRF Token Authentication
* SQLite (default, can be configured for PostgreSQL in production)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd social_media_api
```

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is not available:

```bash
pip install django djangorestframework pillow
```

---

### 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

API Base URL:

```
http://127.0.0.1:8000/api/accounts/
```

---

# 🔐 Authentication Guide

The API uses **Token Authentication**.

After registration or login, a token is returned.
This token must be included in request headers for protected routes.

---

## 📝 User Registration

### Endpoint

```
POST /api/accounts/register/
```

### Request Body

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "strongpassword123"
}
```

### Successful Response

```json
{
  "user": {
    "username": "john",
    "email": "john@example.com"
  },
  "token": "generated_auth_token"
}
```

---

## 🔑 User Login

### Endpoint

```
POST /api/accounts/login/
```

### Request Body

```json
{
  "username": "john",
  "password": "strongpassword123"
}
```

### Response

```json
{
  "token": "generated_auth_token"
}
```

---

## 🔒 Using the Token

Include the token in request headers:

```
Authorization: Token your_generated_token
```

Example (Postman):

Headers →
Key: `Authorization`
Value: `Token abc123xyz`

---

## 👤 User Profile

### Retrieve Profile

```
GET /api/accounts/profile/
```

### Update Profile

```
PUT /api/accounts/profile/
```

Fields that can be updated:

* bio
* profile_picture
* email

Authentication required.

---

# 👥 User Model Overview

The project uses a **custom user model** extending Django’s `AbstractUser`.

### Additional Fields

| Field           | Type                   | Description                |
| --------------- | ---------------------- | -------------------------- |
| bio             | TextField              | Short user biography       |
| profile_picture | ImageField             | User profile image         |
| followers       | ManyToManyField (self) | Users who follow this user |

### Follow System Design

* `followers` is a self-referencing ManyToMany field
* `symmetrical=False` allows one-way following
* Enables future implementation of:

  * Follower lists
  * Following lists
  * Personalized feeds

---

# 🔐 Security Notes

* Passwords are securely hashed using Django’s authentication system.
* Token authentication protects private endpoints.
* Authentication is required for profile access and updates.

---

# 📂 Project Structure

```
social_media_api/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py
```

---

# 🚀 Next Development Steps

The foundation supports extending the API with:

* Posts
* Comments
* Follows endpoints
* Likes
* Notifications
* Feed system
* Deployment to production (e.g., Render, Railway, AWS)

---

# 📄 License

This project is developed for educational and professional practice purposes.

---

If you would like, I can now:

* Upgrade this README to production-deployment level (including environment variables and PostgreSQL setup), or
* Prepare the README for GitHub best practices (badges, API documentation section, example curl requests).
