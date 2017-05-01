from .js_type_base import JsTypeBase

class JsObject(JsTypeBase):
    def __init__(self, value=None):
        super(JsObject, self).__init__(value)