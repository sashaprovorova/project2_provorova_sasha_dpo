import prompt


def welcome():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ").strip()

        if command == "exit":
            return

        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            pass