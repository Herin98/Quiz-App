from sqlalchemy.orm.session import sessionmaker
from app.models import QuestionMaster, QuizInstance, QuizMaster, QuizQuestions, UserMaster, UserResponses, UserSession
from app import db
import uuid
from flask import session
import datetime
from typing import List

"""
[Services Module] Implement various helper functions here as a part of api
                    implementation using MVC Template
"""

def create_user(**kwargs):
    try:
        user = UserMaster(
            uuid.uuid4(),
            kwargs['name'],
            kwargs['username'],
            kwargs['password'],
            kwargs['is_active']
        )

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise e


def check_user_session_is_active(user_id):
    try: 
        user_session = UserSession.query.filter_by(user_id=user_id, is_active=1).first()
        if user_session:
            return True, user_session.session_id
        else:
            return False, None

    except Exception as e:
        raise e    

def check_user_is_admin(user_id):
    try: 
        user_admin = UserMaster.query.filter_by(user_id=user_id, is_admin=1).first()
        if user_admin:
            return True
        else:
            return False

    except Exception as e:
        raise e    

def login_user(**kwargs):
    try:
        user = UserSession.query.filter_by(username=kwargs['username'], password = kwargs['password']).first()
        if user:
            print('logged in')

            is_active, session_id = check_user_session_is_active(user.id) 
            
            if not is_active:
                session_id = uuid.uuid4()
                user_session = UserSession(uuid.uuid4(), user.id, session_id)
                db.session.add(user_session)
                db.session.commit()
            else:
                session['session_id'] = session_id

            session['session_id'] = session_id
            return True, session_id

        else:
            return False, None
    except Exception as e:
        print(str(e))
        raise e

def add_question(**kwargs):
    try:
        question = QuestionMaster(
            uuid.uuid4(),
            kwargs['question'],
            kwargs['choice1'],
            kwargs['choice2'],
            kwargs['choice3'],
            kwargs['choice4'],
            kwargs['answer'],
            kwargs['marks'],
            kwargs['remarks']
        )
        db.session.add(question)
        db.session.commit()

    except Exception as e:
        raise e

def list_question():
    try:
        questions = QuestionMaster.query.filter_by(is_active=1)
        questions_list = list()
        for question in questions:
            question_dict = {}
            question_dict['question_id'] = question.id
            question_dict['question'] = question.question
            question_dict['choice1'] = question.choice1
            question_dict['choice2'] = question.choice2
            question_dict['choice3'] = question.choice3
            question_dict['choice4'] = question.choice4
            question_dict['answer'] = question.answer
            question_dict['marks'] = question.marks
            question_dict['remarks'] = question.remarks

            questions_list.append(question_dict)
        print(questions_list)
        return questions_list
    except Exception as e:
        raise e

def add_quiz(**kwargs):
    try: 
        quizzes = QuizMaster.query.filter_by(quiz_name = kwargs['quiz_name'])
        if quizzes != None:
            quiz = QuizMaster(
                uuid.uuid4(),
                kwargs['quiz_name']
            )
            db.session.add(quiz)
            db.session.commit()

        quiz_id = None
        for quiz in quizzes:
            quiz_id = quiz.id

        quiz_q = QuizQuestions(
            uuid.uuid4(),
            quiz_id,
            kwargs['question_id']
        )

        db.session.add(quiz_q)
        db.session.commit()
    except Exception as e:
        raise e

def list_quiz(userId):
    try:
        quizInstances = QuizInstance.query.filter_by(user_id = userId, is_active=1)
        quiz_list = list()
        for quizInstance in quizInstances:
            quizzes = QuizMaster.query.filter_by(id = quizInstance.quiz_id) 
            for quiz in quizzes:
                quiz_dict = {}
                quiz_dict['quiz_id'] = quiz.id
                quiz_dict['quiz_name'] = quiz.question
                quiz_list.append(quiz_dict)

        print(quiz_list)
        return quiz_list
    except Exception as e:
        raise e

def list_all_quiz():
    try:
        quizzes = QuizMaster.query.filter_by(is_active=1)
        quiz_list = list()
        for quiz in quizzes:
            quiz_dict = {}
            quiz_dict['quiz_id'] = quiz.id
            quiz_dict['quiz_name'] = quiz.question

            quiz_list.append(quiz_dict)

        print(quiz_list)
        return quiz_list
    except Exception as e:
        raise e

def assign_quiz(**kwargs):
    try:
        quiz = QuizInstance(
            uuid.uuid4(),
            kwargs['quiz_id'],
            kwargs['user_id'],
            0,
            0
        )
        db.session.add(quiz)
        db.session.commit()

    except Exception as e:
        raise e

def list_assigned_quiz():
    try:
        quizzes = QuizInstance.query.filter_by(is_active=1)
        quiz_list = list()
        for quiz in quizzes:
            quiz_dict = {}
            quiz_dict['quiz_id'] = quiz.id
            quiz_dict['user_id'] = quiz.user_id
            quiz_dict['is_submitted'] = quiz.is_submitted
            quiz_dict['score_achieved'] = quiz.score_achieved

            quiz_list.append(quiz_dict)
        print(quiz_list)
        return quiz_list
    except Exception as e:
        raise e

def quiz_result():
    try:
        quizzes = QuizInstance.query.filter_by(is_active=1).order_by(QuizInstance.score_achieved.desc())
        quiz_list = list()
        for quiz in quizzes:
            quiz_dict = {}
            quiz_dict['quiz_id'] = quiz.id
            quiz_dict['user_id'] = quiz.user_id
            quiz_dict['score_achieved'] = quiz.score_achieved

            quiz_list.append(quiz_dict)
        print(quiz_list)
        return quiz_list
    except Exception as e:
        raise e

def attempt_quiz(user_id, **kwargs):
    try:
        userResponses = UserResponses(
            uuid.uuid4(),
            kwargs['quiz_id'],
            user_id,
            kwargs['question_id'],
            kwargs['response']
        )
        db.session.add(userResponses)
        db.session.commit()

    except Exception as e:
        raise e

def user_score(user_id, **kwargs):
    try:
        questions = QuestionMaster.query.filter_by(id=kwargs['question_id'])
        score = 0
        for question in questions:
            if question.answer == kwargs['response']:
                score = score + 1

        quiz = QuizInstance(
            uuid.uuid4(),
            kwargs['quiz_id'],
            user_id,
            score,
            1
        )
        db.session.add(quiz)
        db.session.commit()

        return score

    except Exception as e:
        raise e