import os
import sys
sys.path.append('/home/ubuntu/Linkak')

from flask import Flask
from src.models.ai_features import db, SmartLinkCategorization, LinkHealthMonitor, SecurityScan, ContentInsight, AudienceMatch, SmartLinkPreview

app = Flask(__name__)

# Ensure instance directory exists at the correct location
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Use absolute path for SQLite database
db_path = os.path.join(instance_path, 'linkak.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Create tables for new AI models
    db.create_all()
    print(f'Database tables created successfully at {db_path}')
