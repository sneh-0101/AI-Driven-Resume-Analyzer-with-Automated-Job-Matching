import os
import sys

# Add current directory to path so flask_app can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app, db
from flask_app.models import User

def reset_and_verify():
    app = create_app('development')
    with app.app_context():
        print("Searching for admin users...")
        admins = User.query.filter_by(is_admin=True).all()
        if not admins:
            print("No admin users found!")
            return

        for admin in admins:
            print(f"Resetting password for {admin.username} ({admin.email})...")
            admin.set_password('admin123')
            db.session.commit()
            
            # Verify immediately
            is_correct = admin.check_password('admin123')
            print(f"Verification for {admin.username}: {'SUCCESS' if is_correct else 'FAILED'}")

if __name__ == "__main__":
    reset_and_verify()
