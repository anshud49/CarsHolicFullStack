# Django Car Details API

This project is a Django REST API for managing car details, including car models. The project includes a `cardetails` app and a main `api` module to handle endpoints. This README covers the project setup, file structure, available API endpoints, and JWT authentication.

## Project Structure

The project is organized as follows:

```
├── api/
│   ├── __init__.py
│   └── urls.py                   # URL routing for API endpoints
├── CAR/
│   ├── __init__.py
│   ├── admin.py                  # Admin configurations
│   ├── apps.py                   # Application configuration
│   ├── migrations/               # Database migrations
│   ├── models.py                 # Model definitions
│   ├── serializers.py            # API serializers for data models
│   ├── tests.py                  # Test cases
│   ├── utils.py                  # Utility functions
│   └── views.py                  # View definitions
├── cardetails/
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py                   # WSGI configuration
│   └── templates/                # HTML templates (if any)
├── cars/
│   └── images/                   # Directory for storing car images (if needed)
├── manage.py                     # Django management script
└── requirements.txt              # List of dependencies
```

## Requirements

The project requires the following Python packages, listed in `requirements.txt`:

- Django==5.1.3
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- pillow==11.0.0
- psycopg2==2.9.5    # PostgreSQL adapter for Python
- and other libraries (see `requirements.txt` for a full list)

To install these dependencies, run:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file in cardetails app directory and add the following content:**:

   

     ```python
    DJANGO_SECRET_KEY=carholic-anshu-secret-key
    DATABASE_URL=postgresql://CarHolicdb_owner:jUpr7dc3XPGL@ep-floral-surf-a1ti7dr4.ap-southeast-1.aws.neon.tech/CarHolicdb?sslmode=require
     ```

     
4.**In cardetails/settings.py, update the DATABASES setting to use django-environ for environment variables:**:
     ```python
            import environ

         # Initialize environment variables
         env = environ.Env()
         environ.Env.read_env()

         # Database configuration
         DATABASES = {
            'default': env.db(),
         }

         # Secret key
         SECRET_KEY = env('DJANGO_SECRET_KEY')
    ```
               
5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set the admin username, email, and password.

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000/`.

9. **Admin Panel**: You can access the Django Admin Panel at `http://127.0.0.1:8000/admin/`. Use the credentials you set during the `createsuperuser` step.



## API Endpoints



### User Authentication Operations

- *POST /api/register/*: Register a new user.
- *POST /api/login/*: Authenticate and login a user.
- *POST /api/logout/*: Logout the user by invalidating the JWT token.

### Car Model Endpoints(If user is not authenticated)
- **List all public car models**: `GET /api/cars/`

### Car Model Endpoints(user must be authenticated)

- **List all car models created by the user**: `GET /api/cars/`
- **List all car models except the models which are created by the user**: `GET /api/cars/isLoggedin=true`
- **Retrieve car model**: `GET /api/cars/<id>/`
- **Update a car model (full update)**: `PUT /api/cars/<id>/`
- **Partially update a car model (partial update)**: `PATCH /api/cars/<id>/`
- **Delete a car model**: `DELETE /api/cars/<id>/`
- **Delete a car image**: `DELETE /api/carimages/<id>/`


### Root Endpoint

- *GET /api/*: Retrieve the root endpoint of the API.

### JWT Authentication

For protected endpoints, you must include a Bearer token in the `Authorization` header. You can obtain a JWT token by logging in using the `/api/login/` endpoint.

- **Register**: 
  - `POST /api/register/`
  - Body:
    ```json
    {
      "username": "your_username",
      "email": "your_username",
      "password": "your_password"
    }
    ```

- **Login**: 
  - `POST /api/login/`
  - Body:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - On successful login, you will receive a JWT token:
    ```json
    {
       "refresh_token": "your_refresh_token",
       "access_token": "your_acess_token"
    }
    ```

- **Logout**:(include bearer token)
  - `POST /api/logout/`
  - This endpoint will invalidate the JWT token, logging the user out.

  - Body:
    ```json
    {
       "refresh_token": "your_refresh_token",
    }
    ```
   

To use the Bearer token for subsequent requests:

1. Include the token in the `Authorization` header of your requests like this:
   ```
   Authorization: Bearer your_jwt_token
   ```

Example of a `GET` request to list all car models with JWT authentication:

```bash
curl -H "Authorization: Bearer your_jwt_token" http://127.0.0.1:8000/api/cars/
```

### Notes

- Each endpoint also supports formatted responses with extensions like `.json` by appending `.<format>` to the URL.
- `^(?P<path>.*)$`: Catch-all route for handling unmatched paths.

## Additional Notes

- **Database**: The project now uses PostgreSQL instead of SQLite. Ensure you have PostgreSQL set up and the database configured correctly in `cardetails/settings.py`.
- **Admin Panel**: To access the Django Admin Panel, navigate to `http://127.0.0.1:8000/admin/`. Use the credentials created with the `createsuperuser` command to log in.

