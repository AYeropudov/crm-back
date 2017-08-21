from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify
from bson.objectid import ObjectId


from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static')
CORS(app)

app.config['MONGO_DBNAME'] = 'crm'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017

mongoClient = PyMongo(app)


from Classes import Script, ScriptsList, Question, ScriptAttempt, Client, ClientsDb, Answer, AttemptsResult
from Dicts import *

@app.route('/')
def hello_world():
    return "ok"


# Получить список всех скриптов
@app.route('/scripts')
def get_scripts():
    result = ScriptsList.scripts_list()
    return jsonify(result.scripts)


# Получить содержимое скрипта по ID
@app.route("/script/<path:id>")
def get_script_by_id(id):
    result = Script.script(id)
    return jsonify(result.__dict__)


@app.route('/createattempt', methods=["POST"])
def start_attempt():
    post = request.get_json()
    client_db = ClientsDb.ClientsDb()
    script = Script.script(post['script_id'])
    client = client_db.get_client_by_id(post['client_id'])
    attempt = script.start(client=client)
    return jsonify(attempt.__dict__), 202


#запуск опроса
@app.route("/startscript/<path:id>")
def start_script_by_id(id):
    attempt = ScriptAttempt.Attempt(id=id)
    first_question = Question.question(attempt.script.questions[0])
    result = first_question.__dict__
    result["title"]= attempt.script.title
    result["client"] = attempt.client.title
    result["attempt"] = attempt.id
    return jsonify(result)


# получить вопрос по ID с содержимым (ИД, Вопрос, ответы)
@app.route('/question/<path:attempt>/<path:answer>/<path:id>')
def get_next_question(id, answer, attempt):
    answer_entry = Answer.answer(id=answer)
    attempt_entry = ScriptAttempt.Attempt(id=attempt)
    history = AttemptsResult.AttemptsResult(answer_entry, attempt_entry)
    result = Question.question(id)
    if len(result.answers) == 0:
        ScriptAttempt.Attempt.complete(id=attempt)
    return jsonify(result.__dict__)


def get_childrens_list_for_question(question):
    result = []
    childrens = mongoClient.db.answersRelations.find({"question": question})
    for children in childrens:
        for answer in children['answers']:
            result.append({"title": get_title_answer(answer), "children":[]})
    return result


def get_title_answer(id):
    answer = mongoClient.db.answers.find_one({"_id": id})
    if answer is not None:
        return answer['text']


def get_question_list(oids):
    res = []
    for item in oids:
        tmpQuestion = mongoClient.db.questions.find_one({"_id": item})
        res.append({"id": str(tmpQuestion['_id']), "title": tmpQuestion['text'], "children": get_childrens_list_for_question(tmpQuestion['_id'])})
    return res


@app.route('/getclientslist')
def get_cleints_list():
    clients_database = ClientsDb.ClientsDb();
    result = clients_database.get_all()
    return jsonify([item.__dict__ for item in result])


@app.route('/addclient', methods=['POST'])
def add_new_client():
    new_client = Client.Client()
    new_client.fill_from_dict(request.get_json())
    clients_database = ClientsDb.ClientsDb();
    clients_database.addNew(new_client)
    new_client.id = str(new_client._id)
    del new_client._id
    return jsonify(new_client.__dict__), 202


@app.route('/markroot', methods=['POST'])
def mark_node_as_root():
    return jsonify(request.get_json())


@app.route('/dictionaries', methods=['GET', 'POST'])
def dictionaries():
    if request.method == 'POST':
        postData = request.get_json()
        data = postData['dict']
        code = postData['code']

if __name__ == '__main__':
    app.run()


