from enum import unique
from marshmallow.schema import Schema
from sqlalchemy.orm import session
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
username = 'root'
password = 'root'
database_name = 'quiz_app'
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@localhost/{database_name}"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class UserMaster(db.Model):
        __tablename__ = 'user_master'

        pass

        def __init__(self, id, name, username, password, is_admin):
            pass
            
class UserSession(db.Model):
        __tablename__ = 'user_session'
        
        pass
        
        def __init__(self, id, user_id, session_id):
            pass
        
class QuestionMaster(db.Model):
        
        __tablename__ = 'question_master'
        
        pass
        
        def __init__(self, id, question, choice1, 
                     choice2, choice3, choice4, answer, marks, remarks):
            pass
            
class QuizMaster(db.Model):
    
        __tablename__ = 'quiz_master'
        
        pass
        
        def __init__(self, id, quiz_name):
            pass
            
class QuizQuestions(db.Model):
        
        __tablename__ = 'quiz_questions'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'question_id', name='unique_quiz_question'),
        )
        
        pass
        
        def __init__(self, id, quiz_id, question_id):
            pass
     
class QuizInstance(db.Model):
        __tablename__ = 'quiz_instance'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', name='unique_quiz_user'),
        )
        
        pass
        
        def __init__(self, id, quiz_id, user_id):
            pass
            
class UserResponses(db.Model):
        __tablename__ = 'user_responses'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', 'question_id', name='unique_quiz_user_question'),
        )
        
        pass
        
        def __init__(self, id, quiz_id, user_id, question_id, response):
            pass
        
    
db.create_all()
db.session.commit()