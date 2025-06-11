# GitHub Upload and Usage Instructions for Linkak

This guide provides step-by-step instructions for uploading your Linkak project to GitHub and running it on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GitHub Repository Setup](#github-repository-setup)
3. [Preparing Your Linkak Project](#preparing-your-linkak-project)
4. [Uploading to GitHub](#uploading-to-github)
5. [Running Linkak Locally](#running-linkak-locally)
6. [Making Changes and Updates](#making-changes-and-updates)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following:

- [Git](https://git-scm.com/downloads) installed on your computer
- A [GitHub](https://github.com/) account
- Python 3.8 or higher installed
- Basic knowledge of command line operations

## GitHub Repository Setup

1. **Log in to GitHub**
   - Go to [GitHub](https://github.com/) and sign in to your account

2. **Create a new repository**
   - Click the "+" icon in the top right corner
   - Select "New repository"
   - Enter "Linkak" as the repository name
   - Add a description (optional): "A professional digital identity hub with URL shortening and business menu features"
   - Choose repository visibility (Public or Private)
   - Do NOT initialize the repository with a README, .gitignore, or license
   - Click "Create repository"

3. **Copy the repository URL**
   - After creating the repository, you'll see a page with setup instructions
   - Copy the repository URL (it should look like `https://github.com/yourusername/Linkak.git`)

## Preparing Your Linkak Project

1. **Extract the Linkak project**
   - If you received Linkak as a ZIP file, extract it to a location on your computer

2. **Open a terminal or command prompt**
   - Navigate to the extracted Linkak directory:
     ```bash
     cd path/to/Linkak
     ```

3. **Initialize Git repository**
   - Run the following command to initialize a Git repository:
     ```bash
     git init
     ```

4. **Create a .gitignore file**
   - Create a file named `.gitignore` in the root directory with the following content:
     ```
     # Python virtual environment
     venv/
     env/
     ENV/

     # Python cache files
     __pycache__/
     *.py[cod]
     *$py.class
     *.so
     .Python

     # Database files
     *.db
     *.sqlite
     *.sqlite3

     # Environment variables
     .env
     .env.*

     # IDE files
     .idea/
     .vscode/
     *.swp
     *.swo

     # OS files
     .DS_Store
     Thumbs.db

     # Log files
     *.log
     logs/

     # Temporary files
     tmp/
     temp/

     # User uploads (if you want to exclude them)
     # src/static/uploads/
     ```

## Uploading to GitHub

1. **Add your files to Git**
   - Stage all files for commit:
     ```bash
     git add .
     ```

2. **Commit your files**
   - Create your first commit:
     ```bash
     git commit -m "Initial commit of Linkak project"
     ```

3. **Connect to your GitHub repository**
   - Add the GitHub repository as a remote:
     ```bash
     git remote add origin https://github.com/yourusername/Linkak.git
     ```
   - Replace `yourusername` with your actual GitHub username

4. **Push your code to GitHub**
   - Upload your code to GitHub:
     ```bash
     git push -u origin main
     ```
   - If you're using an older version of Git, you might need to use `master` instead of `main`:
     ```bash
     git push -u origin master
     ```

5. **Verify the upload**
   - Go to your GitHub repository page (`https://github.com/yourusername/Linkak`)
   - You should see all your Linkak files there

## Running Linkak Locally

1. **Set up a Python virtual environment**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

2. **Install dependencies**
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```
   - If there's no requirements.txt file, install the necessary packages:
     ```bash
     pip install flask flask-login flask-sqlalchemy werkzeug validators qrcode pillow
     ```

3. **Initialize the database**
   - Run the following command to create the database:
     ```bash
     python -m src.main
     ```
   - This will create the database and populate it with demo data

4. **Run the application**
   - Start the Linkak server:
     ```bash
     python -m src.main
     ```

5. **Access the application**
   - Open your web browser and go to:
     ```
     http://localhost:5000
     ```
   - You should see the Linkak homepage

6. **Log in with demo account**
   - Username: `demo`
   - Password: `password`
   - Or register a new account

## Making Changes and Updates

1. **Edit files**
   - Make changes to the code, templates, or assets as needed

2. **Test your changes**
   - Run the application locally to test your changes
   - Fix any issues that arise

3. **Commit and push your changes**
   - Stage your changes:
     ```bash
     git add .
     ```
   - Commit your changes:
     ```bash
     git commit -m "Description of your changes"
     ```
   - Push to GitHub:
     ```bash
     git push
     ```

## Troubleshooting

### Common Issues and Solutions

**Issue**: `git push` fails with "Permission denied"
- **Solution**: Ensure you have the correct GitHub credentials and repository access
- Try using a personal access token or SSH key for authentication

**Issue**: Dependencies fail to install
- **Solution**: Check your Python version (should be 3.8+)
- Try installing dependencies one by one to identify problematic packages
- Make sure you're in the virtual environment when installing

**Issue**: Application doesn't start
- **Solution**: Check for error messages in the console
- Verify that all required files are present
- Ensure the database file is created and accessible
- Check if the port 5000 is already in use by another application

**Issue**: Database errors
- **Solution**: Delete the existing database file and reinitialize
- Check database connection string in the configuration
- Ensure proper permissions on the database file and directory

**Issue**: Changes not appearing in the application
- **Solution**: Restart the Flask server
- Clear your browser cache
- Check if you're editing the correct files

### Getting Help

If you encounter issues not covered here:

1. Check the [Linkak Documentation](DOCUMENTATION.md) for more detailed information
2. Look for error messages in the console or log files
3. Search for similar issues on GitHub or Stack Overflow
4. Reach out to the Linkak community or support channels

## Next Steps

After successfully uploading Linkak to GitHub, consider:

1. **Customizing your profile**: Update the branding, colors, and content to match your needs
2. **Adding your own links**: Populate your profile with your professional and personal links
3. **Creating menus**: If you run a business, set up digital menus
4. **Setting up URL shortening**: Configure custom domains for your shortened URLs
5. **Exploring advanced features**: Try out AI recommendations, analytics, and scheduling
6. **Deploying to production**: Follow the deployment guide in the documentation to make your Linkak instance publicly accessible
