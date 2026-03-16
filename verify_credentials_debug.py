import os
import sys

# Add current directory to path so flask_app can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app, db
from flask_app.models import User

def verify():
    app = create_app('development')
    with app.app_context():
        print("Checking users in database...")
        users = User.query.all()
        for u in users:
            print(f"User: {u.username}, Email: {u.email}, Is Admin: {u.is_admin}")
            is_correct = u.check_password('admin123')
            print(f"  Password 'admin123' correct: {is_correct}")
            
            # Also check if password hash exists
            print(f"  Password hash present: {u.password_hash is not None}")
            if u.password_hash:
                print(f"  Password hash prefix: {u.password_hash[:20]}...")

if __name__ == "__main__":
    verify()
