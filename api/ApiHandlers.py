from flask_restful import Api, Resource, reqparse
from flask import request
from DbStreamer.main import DbStreamer
from uuid import uuid4


class DBAccess():
    def __init__(self):
        self.obj = DbStreamer("localhost", "root", "0000", "mydb")
        self.obj.connect_database()

    def __del__(self):
        self.obj.close_connection()


class AllQuestionsHandler(Resource, DBAccess):
    def get(self):
        data = self.obj.get_top_questions()
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler",
            'data': data
        }


class QuestionHandler(Resource, DBAccess):
    def get(self, id):
        question_data = self.obj.search_question_by_id(id)
        answers_data = self.obj.search_answers(id)

        return {
            'resultStatus': 'SUCCESS',
            'question_data': question_data,
            'answer_data': answers_data
        }


class Signup(Resource, DBAccess):
    def post(self):
        data = request.get_json()
        userid = data.get('userid', '')
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')

        self.obj.insert_into_users(userid, name, email, password)

        res = {"status": "Success",
               "message": "Account created successfully."}

        return res


class Login(Resource, DBAccess):
    def post(self):
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        # check if this username and password are good or not
        query_res = self.obj.check_user(email, password)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Login unsuccessful."}

            return res
        else:
            rand_token = uuid4()
            self.obj.insert_into_tokens(query_res[0][0], str(rand_token))

            res = {"status": "Success",
                   "message": "Login successfully.",
                   "userid": query_res[0][0],
                   "name": query_res[0][1],
                   "token": str(rand_token)}
            return res


class AddQuestion(Resource, DBAccess):
    def post(self):
        data = request.get_json()
        token = data.get('token', '')
        title = data.get('title', '')
        desc = data.get('desc', '')

        print(token, title, desc)
        query_res = self.obj.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Adding Question unsuccessful."}

            return res
        else:
            self.obj.insert_into_questions(title, desc, query_res[0][0])
            r = self.obj.find_qid(title)

            res = {"status": "Success",
                   "message": "Login successfully.",
                   "qid": r[0][0]
                   }
            return res
