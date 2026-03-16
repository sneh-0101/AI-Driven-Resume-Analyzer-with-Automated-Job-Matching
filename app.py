import os
import json
from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Resume

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Auth Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))
            
        new_user = User(
            username=username, 
            email=email, 
            password=generate_password_hash(password, method='scrypt')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Dashboard & Resume Routes ---
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', resumes=resumes)

@app.route('/resume/new', methods=['GET', 'POST'])
@login_required
def create_resume():
    if request.method == 'POST':
        resume = Resume(
            title=request.form.get('title'),
            user_id=current_user.id,
            full_name=request.form.get('full_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            website=request.form.get('website'),
            summary=request.form.get('summary'),
            education=json.dumps(request.form.getlist('edu[]')), # Complex parsing needed in real app
            experience=json.dumps(request.form.getlist('exp[]')),
            skills=json.dumps(request.form.getlist('skills[]')),
            projects=json.dumps(request.form.getlist('projects[]')),
            certifications=json.dumps(request.form.getlist('certs[]')),
            template_id=request.form.get('template_id', 'template1')
        )
        db.session.add(resume)
        db.session.commit()
        flash('Resume created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('resume_form.html')

@app.route('/resume/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_resume(id):
    resume = Resume.query.get_or_404(id)
    if resume.user_id != current_user.id:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        resume.title = request.form.get('title')
        resume.full_name = request.form.get('full_name')
        resume.email = request.form.get('email')
        resume.phone = request.form.get('phone')
        resume.address = request.form.get('address')
        resume.website = request.form.get('website')
        resume.summary = request.form.get('summary')
        
        # Simplified lists for now
        resume.skills = json.dumps(request.form.get('skills', '').split(','))
        
        db.session.commit()
        flash('Resume updated!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('resume_form.html', resume=resume.to_dict(), edit_mode=True)

@app.route('/resume/delete/<int:id>')
@login_required
def delete_resume(id):
    resume = Resume.query.get_or_404(id)
    if resume.user_id == current_user.id:
        db.session.delete(resume)
        db.session.commit()
        flash('Resume deleted.', 'info')
    return redirect(url_for('dashboard'))

# --- PDF Generation ---
@app.route('/resume/download/<int:id>')
@login_required
def download_pdf(id):
    resume = Resume.query.get_or_404(id)
    if resume.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    from utils.pdf_generator import ResumePDF
    pdf_path = f"static/uploads/resume_{id}.pdf"
    os.makedirs('static/uploads', exist_ok=True)
    
    generator = ResumePDF(resume.to_dict(), resume.template_id)
    generator.generate(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

# --- Advanced Features ---
@app.route('/resume/analyze/<int:id>')
@login_required
def analyze_resume(id):
    resume = Resume.query.get_or_404(id)
    if resume.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    from utils.analyzer import ResumeAnalyzer
    analyzer = ResumeAnalyzer(resume.to_dict())
    score, keywords = analyzer.calculate_ats_score()
    questions = analyzer.generate_interview_questions()
    
    return render_template('analysis.html', resume=resume, score=score, keywords=keywords, questions=questions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
