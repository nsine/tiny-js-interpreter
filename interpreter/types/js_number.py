from .js_type_base import JsTypeBase

class JsNumber(JsTypeBase):
    def __init__(self, value=None):
        super(JsNumber, self).__init__(value)