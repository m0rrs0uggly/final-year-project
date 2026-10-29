import os
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'super-secret-dev-key'


    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/university_portal'
    SQLALCHEMY_TRACK_MODIFICATIONS = False