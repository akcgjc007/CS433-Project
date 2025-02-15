from flask_restful import Api, Resource, reqparse
from flask import request
from DbStreamer.main import DbStreamer
from uuid import uuid4


class AllQuestionsHandler(Resource, DbStreamer):
    def get(self):
        data = self.get_top_questions()
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler",
            'data': data
        }


class QuestionHandler(Resource, DbStreamer):
    def get(self, id):
        question_data = self.search_question_by_id(id)
        answers_data = self.search_answers(id)
        tag_data = self.tags_of_a_question(id)
        tag_arr = []
        for i in tag_data:
            tag_arr.append(i[0])

        return {
            'resultStatus': 'SUCCESS',
            'question_data': question_data,
            'answer_data': answers_data,
            'tag_data': tag_arr
        }


class Signup(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        userid = data.get('userid', '')
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')

        self.insert_into_users(userid, name, email, password)

        res = {"status": "Success",
               "message": "Account created successfully."}

        return res


class Login(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        # check if this username and password are good or not
        query_res = self.check_user(email, password)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Login unsuccessful."}

            return res
        else:
            rand_token = uuid4()
            self.insert_into_tokens(query_res[0][0], str(rand_token))

            res = {"status": "Success",
                   "message": "Login successfully.",
                   "userid": query_res[0][0],
                   "name": query_res[0][1],
                   "token": str(rand_token)}
            return res


class AddQuestion(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        token = data.get('token', '')
        title = data.get('title', '')
        desc = data.get('desc', '')
        tags = data.get('tags', '')
        print(tags)

        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Adding Question unsuccessful."}

            return res
        else:
            self.insert_into_questions(title, desc, query_res[0][0])
            r = self.find_qid(title)
            for tag in tags:
                self.insert_into_tags(tag, r[0][0])

            res = {"status": "Success",
                   "message": "Question added successfully.",
                   "qid": r[0][0]
                   }
            return res


class AddAnswer(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        token = data.get('token', '')
        desc = data.get('desc', '')
        qid = data.get('qid', '')
        # print(token, desc, qid)
        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Adding Question unsuccessful."}

            return res
        else:
            self.insert_into_answers(desc, qid, query_res[0][0])
            r = self.search_answer_by_desc(qid, desc)
            res = {"status": "Success",
                   "message": "Answer added successfully.",
                   "aid": r[0][0]
                   }

            return res


class DeleteQuestion(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        token = data.get('token', '')
        qid = data.get('qid', '')
        print(token, qid)
        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Adding Question unsuccessful."}

            return res
        else:
            qInfo = self.search_question_by_id(qid)
            assert(qInfo[0][3] == query_res[0][0])

            self.delete_question(qid)
            res = {"status": "Success",
                   "message": "Question deleted added successfully."
                   }
            return res


class DeleteAnswer(Resource, DbStreamer):
    def post(self):
        print("Coming here.")
        data = request.get_json()
        token = data.get('token', '')
        aid = data.get('aid', '')
        print(token, aid)
        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Deleting answer unsuccessful."}

            return res
        else:
            aInfo = self.search_answer_by_id(aid)
            assert(aInfo[0][3] == query_res[0][0])

            self.delete_answer(aid)
            res = {"status": "Success",
                   "message": "Answer deleted successfully."
                   }
            return res


class UpvoteQuestion(Resource, DbStreamer):
    def post(self):
        data = request.get_json()
        token = data.get('token', '')
        qid = data.get('qid', '')
        print(token, qid)
        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Adding Question unsuccessful."}

            return res
        else:
            # qInfo = self.search_question_by_id(qid)
            # assert(qInfo[0][1] == query_res[0][0])

            self.upvote_question(query_res[0][0], qid)
            res = {"status": "Success",
                   "message": "Question upvoted added successfully."
                   }
            return res


class UpvoteAnswer(Resource, DbStreamer):
    def post(self):
        print("Coming here.")
        data = request.get_json()
        token = data.get('token', '')
        aid = data.get('aid', '')
        print(token, aid)
        query_res = self.check_token(token)

        if len(query_res) == 0:
            res = {"status": "Fail",
                   "message": "Deleting answer unsuccessful."}

            return res
        else:
            # aInfo = self.search_answer_by_id(aid)
            # assert(aInfo[0][3] == query_res[0][0])

            self.upvote_answer(query_res[0][0], aid)
            res = {"status": "Success",
                   "message": "Answer upvoted successfully."}
            return res


class SearchTagHandler (Resource, DbStreamer):
    def get(self, name):
        res = self.search_by_tag(name)
        title_array = []
        for question_id, in res:
            title_array.append(
                (question_id, self.search_question_by_id(question_id)[0][1]))

        return {
            'resultStatus': 'SUCCESS',
            'title_array': title_array,
        }


class UserProfileHandler(Resource, DbStreamer):
    def get(self, userid):
        res = self.calc_reputation(userid)

        return {
            'resultStatus': 'SUCCESS',
            'reputation': res,
            'qData': self.get_questions_by_user(userid)
        }
