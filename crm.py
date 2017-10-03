from bson.errors import InvalidId
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify
import json
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin



class ObjectIdEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return  str(o)
        return  json.JSONEncoder.default(self, o)


app = Flask(__name__, static_url_path='/static')
CORS(app)

app.config['MONGO_DBNAME'] = 'crm'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
mongo_client = PyMongo(app)
from Classes import Script, ScriptsList, Question, ScriptAttempt, Client, ClientsDb, Answer, AttemptsResult
from References.references import References
from References.base_reference import BaseReference
from References.references_types import ReferencesTypes




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


def get_childs_list_for_question(question):
    result = []
    childrens = mongo_client.db.answersRelations.find({"question": question})
    for children in childrens:
        for answer in children['answers']:
            result.append({"title": get_title_answer(answer), "children":[]})
    return result


def get_title_answer(id):
    answer = mongo_client.db.answers.find_one({"_id": id})
    if answer is not None:
        return answer['text']


def get_question_list(oids):
    res = []
    for item in oids:
        tmpQuestion = mongo_client.db.questions.find_one({"_id": item})
        res.append({"id": str(tmpQuestion['_id']), "title": tmpQuestion['text'], "children": get_childs_list_for_question(tmpQuestion['_id'])})
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


# Получение и создание справочников
@app.route('/references', methods=['GET', 'POST'])
def references():
    if request.method == 'POST':
        postData = request.get_json()
        new_ref = BaseReference()
        new_ref.from_json(postData)
        return jsonify({"result": new_ref.save_reference_to_db})
    if request.method == 'GET':
        refs_collection = References()
        refs_types = ReferencesTypes()
        return  jsonify(references = prepare_jsonify(dict(refs_collection.fill_collection().collection)), types = list(prepare_jsonify(refs_types.get_types_from_db().collection)))


@app.route('/references/<string:ref_id>', methods=['PUT', 'DELETE'])
def modify_references(ref_id):
    try:
        ObjectId(ref_id)
    except InvalidId:
        return jsonify(message="Not valid ID"), 404
    if request.method == 'PUT':
        ref = BaseReference()
        request.json['_id'] = ref_id
        ref.from_json(request.json)
        result = ref.update_reference_in_db
        return jsonify(result = result), 200 if result is True else 404
    if request.method == 'DELETE':
        ref = BaseReference()
        ref.from_json({"_id":ref_id})
        return jsonify({"result": ref.remove_reference_from_db})


# def process_dicts(data, code, type):
#     dict_module = importlib.import_module("References."+type)
#     dict_class = getattr(dict_module,type.title())
#     instance = dict_class(data)
#     result = instance.save(code)
#     if isinstance(result, list):
#         return [str(itm) for itm in result]
#     return [str(result)]

def prepare_jsonify(data):
    return json.loads(json.dumps(data, separators=(",", ": "), cls=ObjectIdEncoder))

if __name__ == '__main__':
    app.run()


