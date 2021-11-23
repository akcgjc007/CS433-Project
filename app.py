from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from api.ApiHandlers import AllQuestionsHandler, QuestionHandler, Signup, Login, AddQuestion, AddAnswer

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(AllQuestionsHandler, '/flask/all')
api.add_resource(QuestionHandler, '/flask/question/<int:id>')
api.add_resource(Signup, '/flask/signup')
api.add_resource(Login, '/flask/login')
api.add_resource(AddQuestion, '/flask/add_question')
api.add_resource(AddAnswer, '/flask/add_answer')
