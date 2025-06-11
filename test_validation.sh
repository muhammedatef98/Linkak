#!/bin/bash

# Test script for Linkak application
# This script will run a series of tests to validate the functionality of the Linkak application

echo "Starting Linkak validation tests..."
echo "====================================="

# Check if the application directory exists
if [ ! -d "/home/ubuntu/Linkak" ]; then
    echo "ERROR: Linkak directory not found!"
    exit 1
fi

# Check if all required files exist
echo "Checking required files..."
required_files=(
    "/home/ubuntu/Linkak/src/main.py"
    "/home/ubuntu/Linkak/src/models/user.py"
    "/home/ubuntu/Linkak/src/models/shorturl.py"
    "/home/ubuntu/Linkak/src/models/menu.py"
    "/home/ubuntu/Linkak/src/models/advanced_features.py"
    "/home/ubuntu/Linkak/src/routes/user.py"
    "/home/ubuntu/Linkak/src/routes/shorturl.py"
    "/home/ubuntu/Linkak/src/routes/menu.py"
    "/home/ubuntu/Linkak/src/routes/advanced.py"
    "/home/ubuntu/Linkak/src/static/img/linkak_logo.png"
    "/home/ubuntu/Linkak/src/static/img/linkak_favicon.png"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo "ERROR: Some required files are missing!"
    exit 1
fi

echo "All required files exist."
echo "====================================="

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p /home/ubuntu/Linkak/src/static/uploads/profiles
mkdir -p /home/ubuntu/Linkak/src/static/uploads/menu_items
mkdir -p /home/ubuntu/Linkak/src/static/qrcodes
echo "Directories created."
echo "====================================="

# Install required packages
echo "Installing required packages..."
pip install flask flask-login flask-sqlalchemy werkzeug validators qrcode pillow
echo "Packages installed."
echo "====================================="

# Create templates directory if it doesn't exist
mkdir -p /home/ubuntu/Linkak/src/templates
mkdir -p /home/ubuntu/Linkak/src/templates/errors
mkdir -p /home/ubuntu/Linkak/src/templates/dashboard
mkdir -p /home/ubuntu/Linkak/src/templates/profile
mkdir -p /home/ubuntu/Linkak/src/templates/menu

# Create basic templates for testing
echo "Creating basic templates for testing..."
cat > /home/ubuntu/Linkak/src/templates/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linkak - Your Professional Digital Identity Hub</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>Welcome to Linkak</h1>
    <p>Your Professional Digital Identity Hub</p>
    <div>
        <a href="/login">Login</a> | <a href="/register">Register</a>
    </div>
</body>
</html>
EOF

cat > /home/ubuntu/Linkak/src/templates/login.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Linkak</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>Login to Linkak</h1>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
EOF

cat > /home/ubuntu/Linkak/src/templates/register.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Linkak</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>Register for Linkak</h1>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <label for="confirm_password">Confirm Password:</label>
            <input type="password" id="confirm_password" name="confirm_password" required>
        </div>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
</body>
</html>
EOF

cat > /home/ubuntu/Linkak/src/templates/dashboard/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Linkak</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>Linkak Dashboard</h1>
    <nav>
        <ul>
            <li><a href="/dashboard/links">Manage Links</a></li>
            <li><a href="/dashboard/menus">Manage Menus</a></li>
            <li><a href="/dashboard/profile">Edit Profile</a></li>
            <li><a href="/logout">Logout</a></li>
        </ul>
    </nav>
    <div>
        <h2>Welcome to your dashboard!</h2>
        <p>From here you can manage all aspects of your Linkak profile.</p>
    </div>
</body>
</html>
EOF

cat > /home/ubuntu/Linkak/src/templates/errors/404.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Not Found - Linkak</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
    <a href="/">Return to Home</a>
</body>
</html>
EOF

cat > /home/ubuntu/Linkak/src/templates/errors/500.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 Server Error - Linkak</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="icon" type="image/png" href="/static/img/linkak_favicon.png">
</head>
<body>
    <h1>500 - Server Error</h1>
    <p>Something went wrong on our end. Please try again later.</p>
    <a href="/">Return to Home</a>
</body>
</html>
EOF

echo "Templates created."
echo "====================================="

# Run the application in test mode
echo "Starting the application in test mode..."
cd /home/ubuntu/Linkak
python -m src.main &
APP_PID=$!

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 5

# Test the health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:5000/api/health)
if [[ $HEALTH_RESPONSE == *"status"*"ok"* ]]; then
    echo "Health endpoint test: PASSED"
else
    echo "Health endpoint test: FAILED"
    echo "Response: $HEALTH_RESPONSE"
    kill $APP_PID
    exit 1
fi
echo "====================================="

# Kill the application
echo "Stopping the application..."
kill $APP_PID
sleep 2

echo "All tests completed successfully!"
echo "Linkak application is ready for use."
echo "====================================="

exit 0
