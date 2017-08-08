from flask import Flask
from flask import request
#from flask import render_template
from flask_pymongo import PyMongo
from flask import jsonify
from bson.objectid import ObjectId
#from bson import json_util
#from Scripts import parser

from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static')
CORS(app)

app.config['MONGO_DBNAME'] = 'crm'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017

mongoClient = PyMongo(app)

from Classes import Script, ScriptsList, Question

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


@app.route("/startscript/<path:id>")
def start_script_by_id(id):
    script =Script.script(id)
    attempt = script.start()
    firstQuestion = Question.question(script.questions[0])
    return jsonify({})
    #script = mongoClient.db.scripts.find_one({'_id': ObjectId(id)})
    #question = mongoClient.db.questions.find_one({"_id": script['questions'][0]})
    #answers = mongoClient.db.answersToQuestionRelations.find({"question": question['_id']})
    #answersList=[]
    #for answer in answers:
    #    answersList.append({'text':get_title_answer(answer['answer']), 'next': str(answer['relQuestion'])})
    #return jsonify({"title": script['title'], "key":str(question["_id"]),"text": question['text'], "answers": answersList})
    pass


# получить вопрос по ID с содержимым (ИД, Вопрос, ответы)
@app.route('/question/<path:id>')
def get_next_question(id):
    result = Question.question(id)
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


@app.route('/markroot', methods=['POST'])
def mark_node_as_root():
    return jsonify(request.get_json())

# @app.route('/scripts/<path:id>')
# def get_script_graph(id):
#     x = mongoClient.db.scripts.find_one({'_id': ObjectId(id)})
#     result = {}
#     for questtion in x['questions']:
#         res = []
#         tmpQuests = mongoClient.db.answersToQuestionRelations.find({'question': questtion})
#         for q in tmpQuests:
#             res.append({
#                 'id': str(q['_id']),
#                 'relQuestion': str(q['relQuestion']),
#                 'answer': str(q["answer"])
#             })
#         result[str(questtion)] = res
#     questions = get_question_list(x['questions'])
#     answers = get_answer_dict()
#     relationsNodes = []
#     relationsEdges = [{
#             "from": "5982cd6b09531125704c8028",
#             "to": "598335de09531177d4d73cf1"
#         },
#         {
#             "from": "5982cd6b09531125704c8028",
#             "to": "598335de09531177d4d73cf2"
#         },
#         {
#             "from": "598335de09531177d4d73cf1",
#             "to": "5982cd6b09531125704c8029"
#         },
#         {
#             "from": "598335de09531177d4d73cf2",
#             "to": "5982cd6b09531125704c8031"
#         }]
#     for item in questions:
#         tmp = result[item['id']]
#         for rel in tmp:
#             #relationsEdges.append({"from": item['id'], "to": rel['id']})
#             #relationsEdges.append({"from": rel['id'], "to": rel['relQuestion']})
#             relationsNodes.append({"id": rel['id'], "label": answers[rel['answer']]})
#     graph = {}
#     # relationsEdges.append({"from": "598335de09531177d4d73cf1", "to": "5982cd6b09531125704c8029"})
#     # relationsEdges.append({"from": "598335de09531177d4d73cf2", "to": "5982cd6b09531125704c8031"})
#     graph['edges'] = relationsEdges
#     graph['nodes'] = []
#     graph['nodes'] += get_question_list(x['questions'])
#     graph['nodes'] += relationsNodes
#     # graph['nodes'] += get_answer_list()
#
#     return jsonify(graph)

# def get_question_list(oids):
#     res = []
#     for item in oids:
#         tmpQuestion = mongoClient.db.questions.find_one({"_id": item})
#         res.append({"id": str(tmpQuestion['_id']), "label": tmpQuestion['text']})
#     return res
#
# def get_question_dict(oids):
#     res = {}
#     for item in oids:
#         tmpQuestion = mongoClient.db.questions.find_one({"_id": item})
#         res[str(tmpQuestion['_id'])] = tmpQuestion['text']
#     return res
#
# def get_answer_list():
#     answers = mongoClient.db.answers.find({})
#     a = []
#     for answer in answers:
#         a.append({'id': str(answer['_id']), 'label': answer['text']})
#     return a
#
# def get_answer_dict():
#     answers = mongoClient.db.answers.find({})
#     a = {}
#     for answer in answers:
#         a[str(answer['_id'])] = answer['text']
#     return a


# @app.route('/answers')
# def get_answers():
#     answers = mongoClient.db.answers.find({})
#     a = []
#     for answer in answers:
#         a.append({'id': str(answer['_id']), 'label': answer['text']})
#     return jsonify(a)
"""
@app.route('/putanswers')
def put_answers_to_db():
    answersList = parser.collect_answ()
    for answer in answersList:
        new_json = {'text': answer, 'type': 'answer'}
        mongoClient.db.answers.insert_one(new_json)
    return 'Inserted'


@app.route('/putquestions')
def put_questions_to_db():
    questionList = parser.collect_q()
    for question in questionList:
        new_json = {'text': question[0], 'type': 'question'}
        mongoClient.db.questions.insert_one(new_json)
    return 'Inserted'
    
@app.route('/relations')
def make_relations_q_to_answ():
    questionList = parser.collect_q()

    for question in questionList:
        retrived = []
        relatedAnswers = question[1]
        questionInDb = mongoClient.db.questions.find_one({"text": question[0]})
        for answer in relatedAnswers:
            answerInDb = mongoClient.db.answers.find_one({'text': answer})
            retrived.append(answerInDb['_id'])
        t = mongoClient.db.answersRelations.insert_one({"question": questionInDb['_id'], "answers": retrived})
    return "Inserted"

@app.route('/relationsa')
def make_relations_q_to_quest_from_answers():
    questionList = parser.collect_q()

    for question in questionList:
        relatedAnswers = question[1]
        relatedQuestions = question[2]
        questionInDb = mongoClient.db.questions.find_one({"text": question[0]})
        for i in range(0, len(relatedAnswers)):
            answerInDb = mongoClient.db.answers.find_one({'text': relatedAnswers[i]})
            relQuesForAnswer = mongoClient.db.questions.find_one({'text': relatedQuestions[i][0]})
            mongoClient.db.answersToQuestionRelations.insert_one(
                {
                    "question": questionInDb['_id'],
                    "answer": answerInDb['_id'],
                    "relQuestion": relQuesForAnswer['_id']
                })
    return "Inserted"


@app.route('/makefirstscr')
def make_first_scr():
    questionList = parser.collect_q()
    retrived = []
    for question in questionList:
        questionInDb = mongoClient.db.questions.find_one({"text": question[0]})
        retrived.append(questionInDb['_id'])
    scriptID = mongoClient.db.scripts.insert_one({'title':'Скрипт КП', 'questions': retrived}).inserted_id
    return str(scriptID)

"""
# @app.route('/relationsa')
# def make_relations_q_to_quest_from_answers():
#     questionList = parser.collect_q()
#
#     for question in questionList:
#         relatedAnswers = question[1]
#         relatedQuestions = question[2]
#         questionInDb = mongoClient.db.questions.find_one({"text": question[0]})
#         for i in range(0, len(relatedAnswers)):
#             answerInDb = mongoClient.db.answers.find_one({'text': relatedAnswers[i]})
#             relQuesForAnswer = mongoClient.db.questions.find_one({'text': relatedQuestions[i][0]})
#             mongoClient.db.answersToQuestionRelations.insert_one(
#                 {
#                     "question": questionInDb['_id'],
#                     "answer": answerInDb['_id'],
#                     "relQuestion": relQuesForAnswer['_id']
#                 })
#     return "Inserted"

if __name__ == '__main__':
    app.run()


