# import subprocess
#
# subprocess.call(["conda", "create", "-n", "env2",
#                  "--file", "requirements.txt", "-c", "pytorch", "-c", "conda-forge"])
from bot.modules.services.semantic_search import get_semantic_response

def main():
    while 1:
        print(1)
        user_input = input("Введите ваш вопрос > ")
        print("Думаем...")
        resp = get_semantic_response(user_input)
        print(resp)


if __name__ == "__main__":
    print(2)
    main()