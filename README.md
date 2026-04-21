# 🛒 PerfectPC - E-commerce Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-Payment-635BFF?style=for-the-badge&logo=stripe&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-81%25-brightgreen?style=for-the-badge)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

PerfectPC is a full-featured, production-ready e-commerce web application built with Python and Flask. It demonstrates a complete online shopping flow, advanced admin management, and robust software engineering practices including high test coverage and a CI/CD pipeline.

---

## ✨ Key Features

### 👤 User Experience
* **Dynamic Catalog & Search:** Browse products with advanced filtering and search functionality.
* **Shopping Cart & Checkout:** Session-based cart management with seamless secure payment integration via **Stripe API**.
* **Personalized Features:** User authentication, order history tracking, and a "Favorites" wish list.
* **Promotions Engine:** Dedicated section for discounted items and special offers.

### 🛡️ Advanced Admin Panel
* **ReadyPC Builder:** A complex relationship management tool to assemble pre-built PCs from individual component categories (CPU, GPU, Motherboard, etc.).
* **Dynamic Category Templates:** Admins can create flexible characteristic templates for different product categories (e.g., "Refresh Rate" for Monitors).
* **Content Management:** Full CRUD operations for products, categories, FAQs, and image upload management.
* **Review Moderation:** Tools to approve or reject customer product reviews.

### ⚙️ Engineering & DevOps
* **Comprehensive Testing:** 40+ automated tests using `pytest` achieving **81% total code coverage**, including API mocking for payment gateways.
* **Continuous Integration:** Fully automated `GitHub Actions` pipeline that runs linting and tests inside a temporary PostgreSQL container on every push.
* **Containerization:** Fully dockerized environment (App + DB) using `docker-compose` for rapid local deployment.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.12, Flask, Flask-WTF, Flask-Login
* **Database:** PostgreSQL, SQLAlchemy (ORM), Flask-Migrate
* **Payment Gateway:** Stripe
* **Testing:** Pytest, coverage, unittest.mock
* **DevOps:** Docker, Docker Compose, GitHub Actions, Gunicorn

---

## 🚀 How to Run Locally

You can run this project effortlessly using Docker.

### Prerequisites
* Docker & Docker Compose installed on your machine.
* Git.

### Setup Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/HaoKann/online-shop-FLASK.git](https://github.com/HaoKann/online-shop-FLASK.git)
    cd online-shop-FLASK
    ```

2.  **Create an `.env` file**
    Create a file named `.flaskenv` or `.env` in the root directory and add your configuration:
    ```env
    SECRET_KEY=your_super_secret_key
    SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@db:5432/online_shop_db
    STRIPE_PUBLIC_KEY=your_stripe_public_key
    STRIPE_SECRET_KEY=your_stripe_secret_key
    ```

3.  **Build and Run via Docker**
    ```bash
    docker-compose up --build
    ```

4.  **Access the Application**
    Open your browser and navigate to: `http://localhost:8000`
    *(Note: Database tables and migrations are handled automatically).*

---

## 🧪 Testing

The project maintains an **81% code coverage** standard. To run the tests locally (requires local python environment):

```bash
# Install test dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run the test suite
pytest --cov=app -v

## 📂 Project Structure

```text
online-shop-FLASK/
├── .github/workflows/   # CI/CD pipelines (GitHub Actions)
├── app/                 # Application source code
│   ├── controllers/     # Route logic (Blueprints: admin, auth, cart, etc.)
│   ├── models/          # Database models (SQLAlchemy)
│   ├── forms/           # Flask-WTF form classes
│   ├── tests/           # 40+ Pytest functional & unit tests
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # CSS, JS, UI assets
├── migrations/          # Alembic database migration scripts
├── Dockerfile           # Production-ready image configuration
├── docker-compose.yml   # Multi-container setup (App + PostgreSQL)
├── requirements.txt     # Python dependencies
└── run.py               # WSGI entry point