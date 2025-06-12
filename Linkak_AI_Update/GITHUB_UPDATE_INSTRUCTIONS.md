# GitHub Update Instructions for Linkak

This guide will walk you through the process of updating your existing Linkak repository on GitHub with the new AI-powered features.

## What's New

We've added several powerful AI features to make Linkak stand out:

1. **Smart Link Categorization** - Automatically categorizes links based on content
2. **Link Health Monitoring** - Checks for broken links and performance issues
3. **Security Scanning** - Detects potential security threats in links
4. **Content Insights** - Analyzes linked content for better understanding
5. **Audience Matching** - Suggests optimal platforms and times for sharing
6. **Smart Link Previews** - Creates enhanced, customized link previews

## Update Instructions

### Option 1: Direct GitHub Update (Recommended)

1. **Clone your existing repository** (if you don't have it locally)
   ```bash
   git clone https://github.com/muhammedatef98/Linkak.git
   cd Linkak
   ```

2. **Create a new branch for the AI features**
   ```bash
   git checkout -b ai-features
   ```

3. **Download the new files**
   - Download the `Linkak_AI_Update.zip` file attached to this message
   - Extract the contents to your local Linkak repository
   - This will add new files and update existing ones

4. **Review the changes**
   ```bash
   git status
   ```

5. **Add the new and modified files**
   ```bash
   git add .
   ```

6. **Commit the changes**
   ```bash
   git commit -m "Add AI-powered features for enhanced link management"
   ```

7. **Push to GitHub**
   ```bash
   git push origin ai-features
   ```

8. **Create a Pull Request**
   - Go to your GitHub repository at https://github.com/muhammedatef98/Linkak
   - Click on "Pull requests" > "New pull request"
   - Select base branch "main" and compare branch "ai-features"
   - Click "Create pull request"
   - Add a title like "Add AI-powered features" and description
   - Click "Create pull request"

9. **Merge the Pull Request**
   - Review the changes
   - Click "Merge pull request"
   - Click "Confirm merge"

### Option 2: Manual File Update

If you prefer to manually update specific files:

1. **Add new model file**
   - Create a new file at `src/models/ai_features.py` with the provided content
   
2. **Add new route file**
   - Create a new file at `src/routes/ai_features.py` with the provided content

3. **Update main.py**
   - Add `from src.routes.ai_features import ai_features_bp` to the imports
   - Add `app.register_blueprint(ai_features_bp)` to register the blueprint

4. **Update documentation**
   - Replace the existing `DOCUMENTATION.md` with the updated version

5. **Commit and push each change**
   ```bash
   git add src/models/ai_features.py
   git commit -m "Add AI features models"
   git add src/routes/ai_features.py
   git commit -m "Add AI features routes"
   git add src/main.py
   git commit -m "Register AI features blueprint"
   git add DOCUMENTATION.md
   git commit -m "Update documentation with AI features"
   git push origin main
   ```

## Database Migration

After updating the code, you'll need to create the new database tables:

1. **Create a migration script**
   - Create a file named `create_ai_tables.py` in your project root with the following content:
   ```python
   import os
   from flask import Flask
   from src.models.ai_features import db
   
   app = Flask(__name__)
   
   # Configure database
   instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
   os.makedirs(instance_path, exist_ok=True)
   db_path = os.path.join(instance_path, 'linkak.db')
   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
   db.init_app(app)
   
   with app.app_context():
       db.create_all()
       print('AI feature tables created successfully')
   ```

2. **Run the migration script**
   ```bash
   python create_ai_tables.py
   ```

## Testing the New Features

To verify that everything is working correctly:

1. **Start the application**
   ```bash
   python -m src.main
   ```

2. **Access the AI features endpoints**
   - Smart Link Categorization: `/api/ai/categorize`
   - Link Health Monitoring: `/api/ai/health-check`
   - Security Scanning: `/api/ai/security-scan`
   - Content Insights: `/api/ai/content-insights`
   - Audience Matching: `/api/ai/audience-match`
   - Smart Link Previews: `/api/ai/smart-preview`

## Troubleshooting

If you encounter any issues during the update:

1. **Database errors**
   - Ensure the instance directory exists and is writable
   - Try deleting and recreating the database tables

2. **Import errors**
   - Check that all new files are in the correct locations
   - Verify that all required packages are installed

3. **API errors**
   - Check the application logs for specific error messages
   - Verify that the blueprints are correctly registered

For additional help, please refer to the updated documentation or contact support.
