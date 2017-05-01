import colorama

from interpreter.interpreter import Interpreter

def run():
    colorama.init()
    with open('./test/test.py') as program_file:
        interpreter = Interpreter(program_file.read())

        result = interpreter.execute()

        if result['success']:
            print(colorama.Fore.GREEN + 'The code is fine')
        else:
            print(colorama.Fore.RED + result['error'])