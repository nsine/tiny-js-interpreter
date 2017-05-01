from .js_type_base import JsTypeBase

class JsBoolean(JsTypeBase):
    def __init__(self, value=None):
        super(JsBoolean, self).__init__(value)