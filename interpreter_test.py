import colorama

from js_executor import JsExecutor

def run():
    colorama.init()

    with open('./test/test.js') as program_file:
        program_text = program_file.read()

        js_executor = JsExecutor(program_text)
        js_executor.execute()

        # try:
        #     js_executor.execute()
        # except Exception as err:
        #     print(colorama.Fore.RED + str(err))
