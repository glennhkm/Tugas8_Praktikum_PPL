# Electronic Store Management System

A Django web application for managing electronic products inventory with CRUD operations, user authentication, and product reviews.

## Features

- Product listing with modern card-based UI
- Detailed product view with specifications and reviews
- Add new products with image upload via Supabase storage
- Update existing products
- Delete products with confirmation
- User authentication system (register, login, logout)
- User profile management
- Product review and rating system
- JWT authentication for API security
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
├── models.py              # Product and Review models
├── views.py               # View functions for products
├── forms.py               # Form definitions
├── urls.py                # App URL configuration
├── admin.py               # Admin configuration
├── supabase_storage.py    # Supabase integration for image storage
├── templatetags/          # Custom template tags
├── ...

accounts/                  # User accounts app directory
├── models.py              # User-related models
├── views.py               # Authentication views
├── forms.py               # User forms
├── urls.py                # Auth URL configuration
├── middleware.py          # JWT authentication middleware
├── ...

templates/                 # HTML templates
├── base.html              # Base template with common structure
├── products/              # Product-specific templates
│   ├── product_list.html  # Product listing page
│   ├── product_detail.html # Product details with reviews
│   ├── product_form.html  # Add/Edit product form
│   ├── product_confirm_delete.html # Delete confirmation
│   ├── edit_review.html   # Edit review form
│   └── delete_review.html # Delete review confirmation
├── accounts/              # Account-specific templates
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── profile.html       # User profile page
│   └── user_reviews.html  # User's reviews page

static/                    # Static files
├── css/                   # CSS files
│   └── style.css          # Custom styles
└── js/                    # JavaScript files
```

## Technologies Used

- Django 5.2
- MySQL
- Supabase (for image storage)
- JWT Authentication
- Bootstrap 5 (for UI components)
- Python-dotenv (for environment variables)
- Django REST Framework with SimpleJWT

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```
   source .venv/bin/activate  # On Linux/Mac
   .venv\Scripts\activate     # On Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Configure the database in `electronic_store/settings.py`
6. Create a `.env` file with the following variables:
   ```
   JWT_SECRET=your_jwt_secret_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```
7. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
8. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
9. Run the development server:
   ```
   python manage.py runserver
   ```
10. Access the application at http://127.0.0.1:8000/

## Usage

1. Visit the homepage to see the product listing
2. Register a new account or login with existing credentials
3. Browse products by category
4. View detailed product information and reviews
5. Add products to your cart (if implemented)
6. Add, edit or delete your reviews
7. Manage your user profile
8. Admin users can access the admin panel at http://127.0.0.1:8000/admin/ to manage all products, reviews, and users

## API Endpoints

The application provides JWT-secured API endpoints for:
- Product listing and details
- User authentication
- Review management

## Future Enhancements

- Shopping cart functionality
- Order processing
- Payment integration
- Advanced search and filtering
- User wishlists 