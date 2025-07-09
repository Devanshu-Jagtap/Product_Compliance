# Product_Compliance

# Product Compliance Management System


## Overview

The Product Compliance Management System is designed for businesses handling post-sales technical support. It enables customers to raise product claims, automatically assigns engineers based on specialization and availability, and allows administrators to monitor task progress. The system includes integrated email and WhatsApp notifications and supports asynchronous background processing.

## Features

* Role-based access: Admin, Engineer, Customer
* Product claim creation and lifecycle management
* Dynamic engineer assignment logic (specialization + workload)
* Asynchronous task execution using Celery and Redis
* Email notification system
* JWT-based authentication
* Admin dashboard using Django Admin

## Technology Stack

* Framework: Django, Django REST Framework
* Database: SQLLite
* Authentication: JWT (djangorestframework-simplejwt)
* Task Queue: Celery
* Message Broker: Redis
* Notifications: Gmail 


## Installation Instructions

### 1. Clone the repository

```
git clone https://github.com/yourusername/product-compliance-system.git
cd product-compliance-system
```

### 2. Set up a virtual environment

```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory and add the following:

```
DEBUG=True
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgres://username:password@localhost:5432/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379
```

### 5. Set up the database

Ensure PostgreSQL is running and the database is created.

Apply migrations:

```
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:

```
python manage.py createsuperuser
```

### 6. Run the development server

```
python manage.py runserver
```

### 7. Start Redis server

```
redis-server
```

### 8. Start Celery worker

In a separate terminal:

```
celery -A config worker --loglevel=info
```

## Authentication

This system uses JWT-based authentication.

Token endpoint:

```
POST /api/token/
```

Request body:

```
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```
## Environment Example

You can include a `.env.example` file with:

```
DEBUG=True
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgres://username:password@localhost:5432/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379
```

## Testing and Linting



## License

This project is proprietary and not intended for public distribution. Contact the maintainer for access or licensing.

## Maintainer

Devanshu Jagtap

