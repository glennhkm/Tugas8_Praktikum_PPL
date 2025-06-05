# Electronic Store Management System

A Django web application for managing electronic products inventory with CRUD operations.

## Features

- Product listing with modern card-based UI
- Add new products with a user-friendly form
- Update existing products
- Delete products with confirmation
- Success messages for all operations
- Responsive design for all devices
- MySQL database integration

## Project Structure

```
electronic_store/          # Main Django project directory
├── settings.py            # Project settings
├── urls.py                # Main URL configuration
├── ...

products/                  # Products app directory
├── models.py              # Product model definition
├── views.py               # View functions
├── forms.py               # Form definitions
├── urls.py                # App URL configuration
├── admin.py               # Admin configuration
├── ...

templates/                 # HTML templates
├── base.html              # Base template with common structure
├── products/              # Product-specific templates
│   ├── product_list.html  # Product listing page
│   ├── product_form.html  # Add/Edit product form
│   └── product_confirm_delete.html  # Delete confirmation

static/                    # Static files
├── css/                   # CSS files
│   └── style.css          # Custom styles
└── js/                    # JavaScript files
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```
   source .venv/bin/activate  # On Linux/Mac
   ```
4. Install dependencies:
   ```
   pip install django mysqlclient
   ```
5. Configure the database in `electronic_store/settings.py`
6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
8. Run the development server:
   ```
   python manage.py runserver
   ```
9. Access the application at http://127.0.0.1:8000/

## Usage

1. Visit the homepage to see the product listing
2. Click "Add New Product" to create a new product
3. Click the edit icon on a product card to update it
4. Click the delete icon to remove a product
5. Access the admin panel at http://127.0.0.1:8000/admin/ 