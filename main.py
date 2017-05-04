#!/usr/bin/python3

import colorama
import sys
from js_executor.js_executor import JsExecutor

if __name__ == '__main__':
    colorama.init()

    if len(sys.argv) != 2:
        print('Must be exactly one argument with script filename')
        sys.exit()

    try:
        with open(sys.argv[1]) as program_file:
            program_text = program_file.read()

            js_executor = JsExecutor(program_text)
            result = js_executor.execute()
            if not result['success']:
                print(colorama.Fore.RED + result['error'])
    except FileNotFoundError:
        print('File not found')
    except Exception as err:
        print(str(err))