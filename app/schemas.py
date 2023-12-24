from marshmallow import Schema, fields, base


"""
This module aims at providing the request and response format for the various api calls.
This also helpful for creating swagger docs for apis testing.
"""

class APIResponse(Schema):
    message = fields.Str(default="Success")

class SignupRequest(Schema):
    username = fields.Str(default="username")
    password = fields.Str(default="password")
    name = fields.Str(default="name")
    is_admin = fields.Str(default=0)

class LoginRequest(Schema):
    username = fields.Str(default="username")
    password = fields.Str(default="password")

class LogoutRequest(Schema):
    session_id = fields.Str(default="session_id")

class QuestionsRequest(Schema):
    session_id = fields.Str(default="session_id")

class ListQuestionsRequest(Schema):
    questions = fields.Str(fields.Dict())

class ViewQuizRequest(Schema):
    session_id = fields.Str(default="session_id")

class ViewAllQuizRequest(Schema):
    session_id = fields.Str(default="session_id")

class ListQuizRequest(Schema):
    quizzes = fields.Str(fields.Dict())

class ViewAssignedQuizRequest(Schema):
    session_id = fields.Str(default="session_id")

class ListAssignedQuizRequest(Schema):
    quizzes = fields.Str(fields.Dict())

class QuizResultRequest(Schema):
    session_id = fields.Str(default="session_id")

class QuizResultResponse(Schema):
    quizzes = fields.Str(fields.Dict())

class AddQuestionsRequest(Schema):
    session_id = fields.Str(default="session_id")
    question = fields.Str(default="question")
    choice1 = fields.Str(default="choice1")
    choice1 = fields.Str(default="choice2")
    choice1 = fields.Str(default="choice3")
    choice1 = fields.Str(default="choice4")
    answer = fields.Int(default=0)
    marks = fields.Int(default=0)
    remarks = fields.Str(default="remarks")

class CreateQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_name = fields.Str(default="quiz_name")
    question_id = fields.Str(default="question_id")

class AssignQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    user_id = fields.Str(default="user_id")
    is_submitted = 0

class AssignQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    user_id = fields.Str(default="user_id")
    question_id = fields.Str(default="question_id")
    response = fields.Int(default=0)