from .types import JsString, JsNumber
from .errors import JsTypeError

class DefaultFunctionsStorage:
    def input(args):
        if len(args) == 0:
            input_message = ''
        else:
            input_message = args[0]

        print(input_message.value)
        input_raw = '5 4 3'
        return JsString(input_raw)

    def parseInt(source_string):
        if not isinstance(source_string, JsString):
            raise JsTypeError('string')

        raw_value = int(source_string)
        return JsNumber(raw_value)

    def print(args):
        if len(args) == 0:
            string = ''
        else:
            string = args[0]

        print(string.value)


default_functions = {
    'input': DefaultFunctionsStorage.input,
    'parseInt': DefaultFunctionsStorage.parseInt,
    'print': DefaultFunctionsStorage.print
}
