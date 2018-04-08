from Models import Code


class Baumuster:

    def __init__(self, baumuster_id, codes):
        self.id = baumuster_id
        self.codes = codes

    def find_code(self, code_id):
        for code in self.codes:
            if code.id == code_id:
                return code

    def contains_code(self, code_id):
        if self.find_code(code_id) is None:
            return False
        return True
