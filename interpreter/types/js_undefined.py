from .js_type_base import JsTypeBase

class JsUndefined(JsTypeBase):
    def __init__(self, value=None):
        super(JsUndefined, self).__init__(value)