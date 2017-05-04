import colorama

from js_executor.js_executor import JsExecutor

def run():
    colorama.init()
    with open('./test/test.py') as program_file:
        js_executor = JsExecutor(program_file.read())

        result = js_executor.execute()

        if result['success']:
            print(colorama.Fore.GREEN + 'The code is fine')
        else:
            print(colorama.Fore.RED + result['error'])