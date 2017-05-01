from .js_type_base import JsTypeBase
from .js_array import JsArray
from interpreter.errors import JsTypeError

class JsString(JsTypeBase):
    def __init__(self, value=None):
        super(JsString, self).__init__(value)

    def split(self, sym):
        if isinstance(sym) is not JsString:
            raise JsTypeError('string')
        splitted = self.value.split(sym.value)

        return JsArray([JsString(splitted_item) for splitted_item in splitted])