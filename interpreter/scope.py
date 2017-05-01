from .types import JsUndefined

class Scope:
    def __init__(self, parent_scope=None):
        self._scopes = []

        if parent_scope is not None:
            self._scopes = [scope for scope in parent_scope._scopes]

        self._scopes.append({})

    def add_variable(self, variable_name):
        variable_data = JsUndefined()
        self._scopes[-1][variable_name] = variable_data

    def update_variable(self, variable_name, variable_data):
        for scope in reversed(self._scopes):
            if variable_name in scope:
                scope[variable_name] = variable_data
                return True
        return False

    def is_variable_exists(self, variable_name):
        for scope in reversed(self._scopes):
            if variable_name in scope:
                return True
        return False

    def add_variable_if_not_exists(self, variable_name):
        is_exists = self.is_variable_exists(variable_name)

        if is_exists:
            return False
        else:
            self.add_variable(variable_name)
            return True
