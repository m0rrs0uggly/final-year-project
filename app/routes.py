from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.decorators import requires_role
from app.models import (
    User,
    Unit,
    Grade,
    MissingMarkClaim,
    UnitEnrollment,
    AttendanceSession,
    AttendanceRecord
)

main_bp = Blueprint('main', __name__)

def redirect_by_role(role):
    if role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    elif role == 'lecturer':
        return redirect(url_for('main.lecturer_dashboard'))
    elif role == 'student':
        return redirect(url_for('main.student_dashboard'))
    return redirect(url_for('main.login'))  # Safely fall back to login if role is unassigned


@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect_by_role(current_user.role)  # FIXED HERE
    return redirect(url_for('main.login'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("\n--- STRAWBERRY PARK LOGIN DEBUG ---")
    print("Request method:", request.method)

    if current_user.is_authenticated:
        print("Already authenticated:", current_user.registration_no)
        return redirect_by_role(current_user.role)

    if request.method == 'POST':
        registration_no = request.form.get('registration_no', '').strip()
        password = request.form.get('password', '')

        print("Registration number received:", repr(registration_no))
        print("Password field received:", bool(password))

        user = User.query.filter_by(
            registration_no=registration_no
        ).first()

        print("User found:", user is not None)

        if user:
            password_matches = user.check_password(password)
            print("Password matches:", password_matches)
        else:
            password_matches = False

        if user and password_matches:
            print("LOGIN SUCCESS")
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect_by_role(user.role)

        print("LOGIN FAILED")
        flash('Invalid registration number or password.', 'danger')

    return render_template('login.html')



@main_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    return "Registration page coming soon!"

@main_bp.route('/student/dashboard')
@login_required
@requires_role('student')
def student_dashboard():

    grades = Grade.query.filter_by(student_id=current_user.id).all()

    claims = MissingMarkClaim.query.filter_by(student_id=current_user.id).all()

    units = Unit.query.all()# claim submission dropdwon

    #retrive this student attendance records
    attendance_records = AttendanceRecord.query.filter_by(
        student_id=current_user.id
    ).all
    return render_template('student_dashboard.html', user=current_user, grades=grades, claims=claims, units=units)

@main_bp.route('/student/submit_claim', methods=['POST'])
@login_required
@requires_role('student')
def submit_claim():
    unit_id = request.form.get('unit_id')
    academic_year = request.form.get('academic_year')
    semester = request.form.get('semester')
    assessment_type = request.form.get('assessment_type')
    description = request.form.get('description')

    if not unit_id or not academic_year or not semester or not assessment_type or not description:
        flash('All fields are required to submit a claim.', 'danger')
        return redirect(url_for('main.student_dashboard'))

    new_claim = MissingMarkClaim()
    new_claim.claim_no = MissingMarkClaim.generate_claim_no()
    new_claim.unit_id = unit_id
    new_claim.academic_year = academic_year
    new_claim.semester = semester
    new_claim.assessment_type = assessment_type
    new_claim.description = description
    new_claim.status = 'PENDING'
    new_claim.student_id = current_user.id
    db.session.add(new_claim)
    db.session.commit()
    flash('Your missing mark claim has been submitted successfully!', 'success')
    return redirect(url_for('main.student_dashboard'))

@main_bp.route('/lecturer/dashboard')
@login_required
@requires_role('lecturer')
def lecturer_dashboard():
    return render_template('lecturer_dashboard.html', user=current_user)

@main_bp.route('/admin/dashboard')
@login_required
@requires_role('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', user=current_user)



