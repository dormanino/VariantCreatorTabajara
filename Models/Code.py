from Models import Optional


class Code:

    def __init__(self, code_id, optional, flag, rule):
        self.id = code_id
        self.optional = optional
        self.rule = rule

        if not flag:
            self.flag = None
        else:
            self.flag = flag
