from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    resumes = db.relationship('Resume', backref='owner', lazy=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Resume")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Personal Info
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    website = db.Column(db.String(200))
    summary = db.Column(db.Text)
    
    # Store Education, Experience, Skills, Projects, Certs as JSON strings
    education = db.Column(db.Text)  # JSON list of dicts
    experience = db.Column(db.Text) # JSON list of dicts
    skills = db.Column(db.Text)     # JSON list of strings
    projects = db.Column(db.Text)   # JSON list of dicts
    certifications = db.Column(db.Text) # JSON list of strings
    
    template_id = db.Column(db.String(20), default="template1")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'website': self.website,
            'summary': self.summary,
            'education': json.loads(self.education) if self.education else [],
            'experience': json.loads(self.experience) if self.experience else [],
            'skills': json.loads(self.skills) if self.skills else [],
            'projects': json.loads(self.projects) if self.projects else [],
            'certifications': json.loads(self.certifications) if self.certifications else []
        }
