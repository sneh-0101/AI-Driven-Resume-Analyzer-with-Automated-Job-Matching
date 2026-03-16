from functools import wraps
import os
import secrets
import string

from flask import Blueprint, abort, flash, redirect, render_template, send_file, url_for
from flask_login import current_user, login_required

from flask_app import db
from flask_app.models import Analysis, JobPosting, Resume, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    total_analyses = Analysis.query.count()
    total_jobs = JobPosting.query.count()
    users = User.query.all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_resumes=total_resumes,
        total_analyses=total_analyses,
        total_jobs=total_jobs,
        users=users,
    )


@admin_bp.route('/user_resumes/<string:user_id>')
@login_required
@admin_required
def user_resumes(user_id):
    user = User.query.get_or_404(user_id)
    resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.created_at.desc()).all()
    return render_template('admin/user_resumes.html', user=user, resumes=resumes)


@admin_bp.route('/user/<string:user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)

    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))

    user.set_password(temp_password)
    db.session.commit()

    flash(
        f'Temporary password for {user.username}: {temp_password}.',
        'warning'
    )
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/download_resume/<string:resume_id>')
@login_required
@admin_required
def download_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)

    from flask import current_app

    uploads_dir = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    user_upload_dir = os.path.join(uploads_dir, resume.user_id)
    actual_file_path = None

    if os.path.exists(user_upload_dir):
        search_patterns = [
            resume.filename.replace(' ', '_'),
            resume.filename.replace(' ', '_').replace('(', '').replace(')', ''),
            resume.filename.replace(' ', '_').replace('(', '_').replace(')', '_'),
            resume.filename.replace('(', '').replace(')', ''),
        ]

        for filename in os.listdir(user_upload_dir):
            if filename.endswith('.pdf'):
                for pattern in search_patterns:
                    if pattern in filename:
                        actual_file_path = os.path.join(user_upload_dir, filename)
                        break
                if actual_file_path:
                    break

    if not actual_file_path:
        possible_paths = [
            resume.filepath,
            os.path.join(uploads_dir, resume.filename),
            os.path.join(user_upload_dir, resume.filename),
            os.path.join(user_upload_dir, f"{resume.id}_{resume.filename}"),
            os.path.join(user_upload_dir, f"{resume.id}_{resume.filename.replace(' ', '_')}"),
        ]

        for path in possible_paths:
            if path and os.path.exists(path):
                actual_file_path = path
                break

    if not actual_file_path:
        flash(f'Resume file not found for: {resume.filename}', 'error')
        return redirect(url_for('admin.user_resumes', user_id=resume.user_id))

    return send_file(actual_file_path, as_attachment=True, download_name=resume.filename)
