from Models import Optional


class Optionals:

    def __init__(self, optionals):
        self.optionals = optionals

    def find(self, optional_id):
        for optional in self.optionals:
            if optional.id == optional_id:
                return optional
        return None
