# LinkHub Setup and Run Guide

This guide will walk you through setting up and running the LinkHub application from scratch.

## Prerequisites

- Python 3.6 or higher
- MySQL (optional, for production)
- Git (optional, for version control)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/LinkHub.git
cd LinkHub
```

Or download and extract the ZIP file.

## Step 2: Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Database (Optional)

By default, LinkHub uses SQLite for development. For production, you can use MySQL:

1. Uncomment the database configuration in `src/main.py`
2. Set up environment variables for your database:
   - `DB_USERNAME` (default: root)
   - `DB_PASSWORD` (default: password)
   - `DB_HOST` (default: localhost)
   - `DB_PORT` (default: 3306)
   - `DB_NAME` (default: mydb)

## Step 5: Run the Application

```bash
# Make sure you're in the project root directory
cd /path/to/LinkHub

# Activate the virtual environment if not already activated
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Run the application
python -m src.main
```

The application will be available at http://localhost:5000

## Step 6: Access the Application

- Landing page: http://localhost:5000
- Dashboard (after login): http://localhost:5000/dashboard

## Step 7: Testing the API

You can test the API using the included test script:

```bash
python test.py http://localhost:5000
```

## Production Deployment

For production deployment, consider:

1. Using a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. Setting up a reverse proxy with Nginx or Apache

3. Using a production database (MySQL or PostgreSQL)

4. Setting proper environment variables for security:
   - Set a strong `SECRET_KEY` in `src/main.py`
   - Configure database credentials securely

## API Documentation

### Authentication

- `POST /api/register` - Register a new user
- `POST /api/login` - Log in a user
- `POST /api/logout` - Log out a user

### Profile Management

- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Link Management

- `GET /api/links` - Get all links for the logged-in user
- `POST /api/links` - Create a new link
- `PUT /api/links/<link_id>` - Update a link
- `DELETE /api/links/<link_id>` - Delete a link

### Analytics

- `GET /api/analytics` - Get analytics data for the logged-in user

## Troubleshooting

- **Database Connection Issues**: Verify your database credentials and ensure the database server is running
- **Import Errors**: Make sure you're running the application from the project root directory
- **Permission Errors**: Ensure you have write permissions for the application directory

## Support

For support, please open an issue on the GitHub repository or contact the maintainer.
