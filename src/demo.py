# import subprocess
#
# subprocess.call(["conda", "create", "-n", "env2",
#                  "--file", "requirements.txt", "-c", "pytorch", "-c", "conda-forge"])
import os
from bot.modules.services.semantic_search import get_semantic_response
def questionsListToStr(questions: list[str]) -> str:
    s = ""
    for question in questions:
        s += f"{question}. "
    return s

def handleQuestions(questions):
    is_useful = "0"
    while is_useful == "0":
        print("questions:", questions)
        is_useful = input("Был ли этот ответ полезен? (ответьте 1 если да, 0 если нет) > ")
        if is_useful == "1":
            return
        elif is_useful == "0":
            clearer_request = input("Уточните ваш вопрос > ")
            questions.append(clearer_request)
            print("Думаем...")
            resp = get_semantic_response(questionsListToStr(questions))
            print(resp)
            if len(questions) == 3:
                return
        else:
            return


def main():
    # os.system("clear")
    while 1:
        questions = []
        user_input = input("Введите ваш вопрос > ")
        questions.append(user_input)
        print("Думаем...")
        resp = get_semantic_response(questionsListToStr(questions))
        print(resp)
        handleQuestions(questions)



if __name__ == "__main__":
    main()