from app import create_app, db
from app.models import User, Unit, Grade, MissingMarkClaim

app = create_app()

with app.app_context():
    # 1. Force drop all tables directly in MySQL bypass FK locks
    db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 0;'))
    db.session.execute(db.text('DROP TABLE IF EXISTS missing_mark_claims;'))
    db.session.execute(db.text('DROP TABLE IF EXISTS grades;'))
    db.session.execute(db.text('DROP TABLE IF EXISTS units;'))
    db.session.execute(db.text('DROP TABLE IF EXISTS users;'))
    db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 1;'))
    db.session.commit()

    # 2. Create fresh tables with updated nullable=True columns
    db.create_all()
    print("Database tables force-recreated.")

    # 3. Seed Users
    admin = User(registration_no='ADM/001', first_name='Admin', last_name='System', email='admin@university.ac.ke', role='admin')
    admin.set_password('admin123')

    lecturer = User(registration_no='LEC/101', first_name='John', last_name='Doe', email='j.doe@university.ac.ke', role='lecturer')
    lecturer.set_password('lec123')

    student = User(registration_no='BIT/2024/001', first_name='Karl', last_name='Student', email='karl@student.ac.ke', role='student')
    student.set_password('student123')

    db.session.add_all([admin, lecturer, student])
    db.session.commit()

    # 4. Seed Units assigned to Lecturer
    unit1 = Unit(code='BIT 2104', title='Web Application Development', credit_hours=3, lecturer_id=lecturer.id)
    unit2 = Unit(code='BIT 2106', title='Database Systems II', credit_hours=3, lecturer_id=lecturer.id)
    unit3 = Unit(code='BIT 2108', title='Software Engineering', credit_hours=4, lecturer_id=lecturer.id)

    db.session.add_all([unit1, unit2, unit3])
    db.session.commit()

    # 5. Seed Grades with NULLs for missing marks
    g1 = Grade(student_id=student.id, unit_id=unit1.id, academic_year='2025/2026', semester='SEM 1', cat_score=24.0, exam_score=52.0)
    g2 = Grade(student_id=student.id, unit_id=unit2.id, academic_year='2025/2026', semester='SEM 1', cat_score=20.0, exam_score=None)  # Missing Exam
    g3 = Grade(student_id=student.id, unit_id=unit3.id, academic_year='2025/2026', semester='SEM 1', cat_score=None, exam_score=48.0)  # Missing CAT

    db.session.add_all([g1, g2, g3])
    db.session.commit()

    # 6. Seed Missing Mark Claim
    claim = MissingMarkClaim(
        claim_no=MissingMarkClaim.generate_claim_no(),
        student_id=student.id,
        unit_id=unit2.id,
        academic_year='2025/2026',
        semester='SEM 1',
        assessment_type='EXAM',
        description='Sat for final exam on Dec 12 in Hall B. Mark currently shows INC.',
        status='PENDING'
    )
    db.session.add(claim)
    db.session.commit()

    print("SUCCESS // Seeded users, units, grades, and claims cleanly.")