import subprocess
import re

def get_args(node):
    return 2

def check(node):
    with open('./test/test.py') as program_file:
        text = program_file.read().split('\n')
        error = False
        for line_index, text_line in enumerate(text):
            error_pos = text_line.find(' / 0')
            if error_pos != -1:
                return 'Error: Division by zero at line {}, position {}'.format(line_index + 1, error_pos + 1)


    lint_result = subprocess.run(['pylint', './test/test.py', '--errors-only'], stdout=subprocess.PIPE)
    # result_strings = re.search(r'(E:.+)\r', str(result.stdout))
    lint_strings = lint_result.stdout.decode('utf8').split('\r\n')

    mypy_result = subprocess.run(['c:/Program Files/Python3/Scripts/mypy.bat', './test/test.py', '--show-column-numbers'], stdout=subprocess.PIPE)
    mypy_strings = mypy_result.stdout.decode('utf8').split('\r\n')
    if len(lint_strings) == 1 and lint_strings[0] == '' \
        and len(mypy_strings) == 1 and mypy_strings[0] == '':
        return None
    else:
        output = ''
        if lint_strings[0] != '':
            message = lint_strings[1]
            data = re.match(r'E:\s+(\d+),\s*(\d+): (.+?) \(', message)
            output = 'Error: {} at line {}, position {}'.format(data.group(3), data.group(1), data.group(2))
        else:
            message = mypy_strings[0]
            data = re.match(r'.+?:(\d+):(\d+): error: (.+)', message)
            error_message = data.group(3)

            if (error_message.startswith('No overload')):
                error_message = re.match(r'(.+?) \[', error_message).group(1)
            output = 'Error: {} at line {}, position {}'.format(error_message, data.group(1), data.group(2))

        return output