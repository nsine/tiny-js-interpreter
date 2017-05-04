from .errors import JsTypeError

class JsTypeBase:
    def __init__(self, value=None):
        self.value = value
        self.properties = {}

    def _js_to_number(self):
        raise JsTypeError()

    def _js_to_string(self):
        raise JsTypeError()

    def _js_to_boolean(self):
        raise JsTypeError()

class JsArray(JsTypeBase):
    def __init__(self, value=None):
        super(JsArray, self).__init__(value)

        if isinstance(value, list):
            self.length = len(value)
        else:
            self.value = []
            self.length = 0

        self.properties['length'] = self._js_default_length
        self.properties['push'] = self._js_default_push
        self.properties['pop'] = self._js_default_pop

    def _js_by_index(self, index):
        if not isinstance(index, JsNumber):
            raise JsTypeError('Index must be a number')

        index_raw = index.value
        if index_raw < self.length:
            return self.value[index_raw]
        else:
            return JsUndefined()

    def _js_default_length(self, args):
        return JsNumber(self.length)

    def _js_default_push(self, args):
        item = args[0]
        self.value.append(item)
        self.length += 1

    def _js_default_pop(self):
        if len(self.value > 0):
            popped_value = self.value.pop()

            self.length -= 1
        return popped_value

    def _js_to_string(self):
        string_raw = ', '.join([item._js_to_string().value for item in self.value])
        return JsString(string_raw)

class JsBoolean(JsTypeBase):
    def __init__(self, value=None):
        super(JsBoolean, self).__init__(value)

    def _js_to_number(self):
        raise JsTypeError()

    def _js_to_string(self):
        if self.value:
            return JsString('true')
        else:
            return JsString('false')

    def _js_to_boolean(self):
        return self

class JsNumber(JsTypeBase):
    def __init__(self, value=None):
        super(JsNumber, self).__init__(value)

    def __add__(self, other):
        if isinstance(other, JsNumber):
            return JsNumber(self.value + other.value)
        elif isinstance(other, JsString):
            return self._js_to_string() + other.value
        else:
            raise JsTypeError('incorrect types')

    def __sub__(self, other):
        if isinstance(other, JsNumber):
            return JsNumber(self.value - other.value)
        elif isinstance(other, JsString):
            # Need to call default parseFloat instead
            return self + other._js_to_number()
        else:
            raise JsTypeError('incorrect types')

    def __mul__(self, other):
        if isinstance(other, JsNumber):
            return JsNumber(self.value * other.value)
        else:
            raise JsTypeError('incorrect types')

    def __truediv__(self, other):
        if isinstance(other, JsNumber):
            return JsNumber(self.value / other.value)
        else:
            raise JsTypeError('incorrect types')

    def __mod__(self, other):
        if isinstance(other, JsNumber):
            return JsNumber(self.value % other.value)
        else:
            raise JsTypeError('incorrect types')

    def __lt__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value < other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __le__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value <= other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __gt__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value > other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __ge__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value >= other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __eq__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value == other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __ne__(self, other):
        if isinstance(other, JsNumber):
            return JsBoolean(self.value != other.value)
        else:
            raise JsTypeError('Incorrect type')

    def __str__(self):
        return str(self.value)

    def _js_to_number(self):
        return self

    def _js_to_string(self):
        return JsString(str(self.value))

    def _js_to_boolean(self):
        if self.value == 0:
            return JsBoolean(False)
        else:
            return JsBoolean(True)

class JsObject(JsTypeBase):
    def __init__(self, value=None):
        super(JsObject, self).__init__(value)

    def _js_to_string(self):
        return JsString('<object>')

    def _js_to_number(self):
        raise JsTypeError('Can\'t cast object to number')

    def _js_to_boolean(self):
        raise JsTypeError('Can\'t cast object to boolean')


class JsString(JsTypeBase):
    def __init__(self, value=None):
        super(JsString, self).__init__(value)
        self.properties['split'] = self._js_default_split

    def _js_default_split(self, args):
        sym = args[0]

        if not isinstance(sym, JsString):
            raise JsTypeError('string')
        splitted = self.value.split(sym.value)

        return JsArray([JsString(splitted_item) for splitted_item in splitted])

    def _js_to_string(self):
        return self

    def _js_to_number(self):
        try:
            number_raw = float(self.value)
            return JsNumber(number_raw)
        except:
            raise JsTypeError('Can\'t cast string to number')

    def _js_to_boolean(self):
        return JsBoolean(False)

class JsUndefined(JsTypeBase):
    def __init__(self, value=None):
        super(JsUndefined, self).__init__(value)

    def _js_to_string(self):
        return JsString('')

    def _js_to_number(self):
        return JsNumber(0)

    def _js_to_boolean(self):
        return JsBoolean(False)