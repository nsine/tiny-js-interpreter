from.js_type_base import JsTypeBase

class JsArray(JsTypeBase):
    def __init__(self, value=None):
        super(JsArray, self).__init__(value)

        if isinstance(value, list):
            self.length = len(value)
        else:
            self.value = []
            self.length = 0

    def push(self, item):
        self.value.append(item)
        self.length += 1

    def pop(self):
        if len(self.value > 0):
            popped_value = self.value.pop()

            self.length -= 1
        return popped_value
