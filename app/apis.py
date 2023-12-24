from app.models import *
from app import *
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from app.schemas import *
from app.services import *
from schemas import *

"""
[Sign Up API] : Its responsibility is to perform the signup activity for the user.
"""
#  Restful way of creating APIs through Flask Restful
class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign Up Api', tags=['SignUp API'])
    @use_kwargs(SignupRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            create_user(**kwargs)
            return APIResponse().dump(dict(message='User is successfully registered')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to register user : {str(e)}')), 400

api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)

"""
[Login API] : Its responsibility is to perform the login activity for the user and 
create session id which will be used for all subsequent operations.
"""
class LoginAPI(MethodResource, Resource):
    @doc(description='Login Api', tags=['Login API'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_logged_in, session_id = login_user(**kwargs)
            if is_logged_in:
                return APIResponse().dump(dict(message='User is successfully logged in')), 200
                # return jsonify({'message':'User is successfully logged in'}), 200
            else:
                return APIResponse().dump(dict(message='User not found')), 404
                # return jsonify({'message':'User not found'}), 404
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to login user : {str(e)}')), 400
            # return jsonify({'message':f'Not able to login user : {str(e)}'}), 400


api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)

"""
[Logout API] : Its responsibility is to perform the logout activity for the user.
"""
class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                session['user_id'] = None
                print('logged out')
                return APIResponse().dump(dict(message='User is successfully logged out')), 200
                # return jsonify({'message':'User is successfully logged out'}), 200
            else:
                print('user not found')
                return APIResponse().dump(dict(message='User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to logout user : {str(e)}')), 400
            # return jsonify({'message':f'Not able to logout user : {str(e)}'}), 400
          
api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)

"""
[Add Question API] : Its responsibility is to add question to the question bank.
Admin has only the rights to perform this activity.
"""
class AddQuestionAPI(MethodResource, Resource):
    @doc(description='Add Question Api', tags=['Questions'])
    @use_kwargs(AddQuestionsRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            add_question(**kwargs)

            return APIResponse().dump(dict(message='Question is successfully logged out')), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to add question : {str(e)}')), 400
           

api.add_resource(AddQuestionAPI, '/add.question')
docs.register(AddQuestionAPI)

"""
[List Questions API] : Its responsibility is to list all questions present activly in the question bank.
Here only Admin can access all the questions.
"""
class ListQuestionAPI(MethodResource, Resource):
    @doc(description='List Question Api', tags=['Questions'])
    @use_kwargs(ListQuestionsRequest, location=('json'))
    @marshal_with(APIResponse)
    def get(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            questions = list_question()

            return ListQuestionsRequest().dump(dict(quiz=questions)), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list question : {str(e)}')), 400
           

api.add_resource(ListQuestionAPI, '/list.questions')
docs.register(ListQuestionAPI)

"""
[Create Quiz API] : Its responsibility is to create quiz and only admin can create quiz using this API.
"""
class CreateQuizAPI(MethodResource, Resource):
    @doc(description='Create Quiz Api', tags=['Quiz'])
    @use_kwargs(CreateQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            add_quiz(**kwargs)

            return APIResponse().dump(dict(message='Quiz is created successfully')), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to add quiz : {str(e)}')), 400
           


api.add_resource(CreateQuizAPI, '/create.quiz')
docs.register(CreateQuizAPI)

"""
[Assign Quiz API] : Its responsibility is to assign quiz to the user. Only Admin can perform this API call.
"""
class AssignQuizAPI(MethodResource, Resource):
    @doc(description='Assign Quiz Api', tags=['Quiz'])
    @use_kwargs(AssignQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            assign_quiz(**kwargs)

            return APIResponse().dump(dict(message='Quiz assigned successfully')), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to asign quiz : {str(e)}')), 400
           

api.add_resource(AssignQuizAPI, '/assign.quiz')
docs.register(AssignQuizAPI)

"""
[View Quiz API] : Its responsibility is to view the quiz details.
Only Admin and the assigned users to this quiz can access the quiz details.
"""
class ViewQuizAPI(MethodResource, Resource):
    @doc(description='List Quiz Api', tags=['Quiz'])
    @use_kwargs(ViewQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if is_admin:
                quizzes = list_all_quiz()
            else:
                quizzes = list_quiz(user_id)
                
            return ListQuizRequest().dump(dict(quiz=quizzes)), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list quiz : {str(e)}')), 400
           


api.add_resource(ViewQuizAPI, '/view.quiz')
docs.register(ViewQuizAPI)

"""
[View Assigned Quiz API] : Its responsibility is to list all the assigned quizzes 
                            with there submission status and achieved scores.
"""
class ViewAssignedQuizAPI(MethodResource, Resource):
    @doc(description='List Assigned Quiz Api', tags=['Quiz'])
    @use_kwargs(ViewAssignedQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def get(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            quizzes = list_assigned_quiz()

            return ListAssignedQuizRequest().dump(dict(quiz=quizzes)), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list assigned quiz : {str(e)}')), 400
           


api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
docs.register(ViewAssignedQuizAPI)


"""
[View All Quiz API] : Its responsibility is to list all the created quizzes. Admin can only list all quizzes.
"""
class ViewAllQuizAPI(MethodResource, Resource):
    @doc(description='List All Quiz Api', tags=['Quiz'])
    @use_kwargs(ViewAllQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            quizzes = list_all_quiz()

            return ListQuizRequest().dump(dict(quiz=quizzes)), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list quiz : {str(e)}')), 400
           

api.add_resource(ViewAllQuizAPI, '/all.quizzes')
docs.register(ViewAllQuizAPI)

"""
[Attempt Quiz API] : Its responsibility is to perform quiz attempt activity by 
                        the user and the score will be shown as a result of the submitted attempt.
"""
class AttemptQuizAPI(MethodResource, Resource): #user response
    @doc(description='Attempt Quiz Api', tags=['Quiz'])
    @use_kwargs(ViewAllQuizRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            attempt_quiz(user_id, **kwargs)
            score = user_score(user_id, **kwargs)

            return APIResponse().dump(dict(message=f'User Scored : {str(score)}')), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to attempt quiz : {str(e)}')), 400
           

api.add_resource(AttemptQuizAPI, '/attempt.quiz')
docs.register(AttemptQuizAPI)

"""
[Quiz Results API] : Its responsibility is to provide the quiz results in which the users 
                        having the scores sorted in descending order are displayed, 
                        also the ones who have not attempted are also shown.
                        Admin has only acess to this functionality.
"""
class QuizResultAPI(MethodResource, Resource): #view quiz instance
    @doc(description='List Quiz Result Api', tags=['Quiz'])
    @use_kwargs(QuizResultRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:

            is_active, user_id = check_user_session_is_active(kwargs['session_id']) 

            if not is_active:
                return APIResponse().dump(dict(message='User is not logged in')), 404

            is_admin = check_user_is_admin(user_id)

            if not is_admin:
                return APIResponse().dump(dict(message='User is not admin')), 401

            quizzes = quiz_result()

            return QuizResultResponse().dump(dict(quiz=quizzes)), 200

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list quiz result : {str(e)}')), 400


api.add_resource(QuizResultAPI, '/quiz.results')
docs.register(QuizResultAPI)


