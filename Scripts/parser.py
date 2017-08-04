import Scripts.dataQ as questions
import Scripts.dataANS as answers

qList = []
answerList = []
isset = True


def collect_q():
    for x in range(1, 300):
        question = getattr(questions, "q{}".format(x), None)
        if question is None:
            break
        if question is not None:
            qList.append(question)
        x += 1
    return qList


def collect_answ():
    for x in range(1, 300):
        answer = getattr(answers, "ans{}".format(x), None)
        if answer is None:
            break
        if answer is not None:
            answerList.append(answer)
        x += 1
    return answerList
