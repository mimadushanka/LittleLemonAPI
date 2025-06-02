This Django REST Framework (DRF) project provides a robust backend API for Little Lemon, a fictional restaurant. The system handles menu management, user group roles, shopping cart, and order processing with fine-grained permission control and rate throttling.

Features
User Roles & Permissions

Manager: Can manage menu items, assign delivery crew, and manage orders.

Delivery Crew: Can view and update assigned orders (status only).

Customer: Can browse menu, add items to cart, and place orders.

Menu Management

View all items with filters (by category, price, search, ordering).

Add, update, and delete items (restricted to managers).

Pagination support.

Cart Operations

Add items to cart.

View current cart.

Clear cart.

Order Management

Customers can place orders based on cart contents.

Managers can assign delivery crew and update status.

Delivery crew can update order status (0: Out for Delivery, 1: Delivered).

Orders can be deleted by managers.

Throttling & Security

Authenticated access enforced via token/session authentication.

Role-based access control via Django Group model.

Throttling enabled for both anonymous and authenticated users.

API Endpoints Overview

/api/menu-items/             - GET, POST

/api/menu-items/{id}/        - GET, PUT, PATCH, DELETE

/api/cart/menu-items/        - GET, POST, DELETE

/api/orders/                 - GET, POST

/api/orders/{orderId}/       - GET, PUT, PATCH, DELETE

/api/groups/manager/         - GET, POST

/api/groups/manager/{id}/    - DELETE

/api/groups/delivery-crew/   - GET, POST

/api/groups/delivery-crew/{id}/ - DELETE

Tech Stack
Python 3.12

Django 5.0.4

Django REST Framework

SQLite (default)

Token & Session Authentication

Pagination, Filtering, Throttling

# 1. Clone the repository
git clone https://github.com/your-username/LittLelemonAPI.git
cd little-lemon-api

# 2. Install dependencies and create a virtual environment
pipenv install

# 3. Activate the virtual environment
pipenv shell

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver


