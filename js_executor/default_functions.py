import math

from .types import JsString, JsNumber
from .errors import JsTypeError, JsArgumentError

class DefaultFunctionsStorage:
    def console_input(args):
        if len(args) == 0:
            input_message = ''
        else:
            input_message = args[0]

        input_raw = input(input_message.value)
        return JsString(input_raw)

    def parseInt(args):
        if len(args) != 1 or not isinstance(args[0], JsString):
            raise JsArgumentError('parseInt requires 1 string argument')

        source_string = args[0]

        try:
            raw_value = int(source_string.value)
        except:
            raise JsTypeError("Could not convert string '{}' to int".format(source_string.value))
        return JsNumber(raw_value)

    def parseFloat(args):
        if len(args) != 1 or not isinstance(args[0], JsString):
            raise JsArgumentError('parseFloat requires 1 string argument')

        source_string = args[0]

        try:
            raw_value = float(source_string.value)
        except:
            raise JsTypeError("Could not convert string '{}' to float".format(source_string.value))
        return JsNumber(raw_value)

    def console_log(args):
        if len(args) == 0:
            print()
        else:
            for arg in args:
                print(arg._js_to_string().value)

    def math_sqrt(args):
        if len(args) != 1 or not isinstance(args[0], JsNumber):
            raise JsArgumentError('Math.sqrt requires 1 number argument')

        n = args[0].value
        return JsNumber(math.sqrt(n))


default_functions = {
    'console.input': DefaultFunctionsStorage.console_input,
    'parseInt': DefaultFunctionsStorage.parseInt,
    'console.log': DefaultFunctionsStorage.console_log,
    'parseFloat': DefaultFunctionsStorage.parseFloat,
    'Math.sqrt': DefaultFunctionsStorage.math_sqrt
}
