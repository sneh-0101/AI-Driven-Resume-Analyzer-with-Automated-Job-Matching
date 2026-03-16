#!/usr/bin/env python3
"""
Create admin account script.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app, db
from flask_app.models import User


def create_admin():
    app = create_app('development')
    with app.app_context():
        existing_admin = User.query.filter_by(email='admin@demo.com').first()
        if existing_admin:
            print("Admin account already exists.")
            print(f"Email: {existing_admin.email}")
            print(f"Username: {existing_admin.username}")
            return

        admin = User(
            username='demo_admin',
            email='admin@demo.com',
            first_name='Demo',
            last_name='Admin',
            is_admin=True,
        )
        admin.set_password('admin123')

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully.")
        print("Email: admin@demo.com")
        print("Password: admin123")
        print("Username: demo_admin")
        print("Admin URL: http://localhost:5000/admin/")


if __name__ == "__main__":
    create_admin()
