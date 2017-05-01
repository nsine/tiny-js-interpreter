import colorama

from interpreter.interpreter import Interpreter

def run():
    colorama.init()

    with open('./test/test.js') as program_file:
        program_text = program_file.read()

        interpreter = Interpreter(program_text)
        interpreter.execute()

        # try:
        #     interpreter.execute()
        # except Exception as err:
        #     print(colorama.Fore.RED + str(err))
