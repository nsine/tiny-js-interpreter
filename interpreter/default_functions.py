import math

from .types import JsString, JsNumber
from .errors import JsTypeError, JsArgumentError

class DefaultFunctionsStorage:
    def input(args):
        if len(args) == 0:
            input_message = ''
        else:
            input_message = args[0]

        input_raw = input(input_message.value)
        return JsString(input_raw)

    def parseInt(args):
        source_string = args[0]
        if not isinstance(source_string, JsString):
            raise JsTypeError('string')

        raw_value = int(source_string.value)
        return JsNumber(raw_value)

    def parseFloat(args):
        source_string = args[0]
        if not isinstance(source_string, JsString):
            raise JsTypeError('string')

        raw_value = float(source_string.value)
        return JsNumber(raw_value)

    def print(args):
        if len(args) == 0:
            string = ''
        else:
            string = args[0]._js_to_string().value

        print(string)

    def math_sqrt(args):
        if len(args) == 0 or not isinstance(args[0], JsNumber):
            raise JsArgumentError('Math.sqrt requires 1 number argument')

        n = args[0].value
        return JsNumber(math.sqrt(n))


default_functions = {
    'input': DefaultFunctionsStorage.input,
    'parseInt': DefaultFunctionsStorage.parseInt,
    'print': DefaultFunctionsStorage.print,
    'parseFloat': DefaultFunctionsStorage.parseFloat,
    'Math.sqrt': DefaultFunctionsStorage.math_sqrt
}
