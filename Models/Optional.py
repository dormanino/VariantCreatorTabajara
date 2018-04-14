class Optional:

    def __init__(self, optional_id, code_optionals):
        self.id = optional_id
        self.code_optionals = code_optionals

    def rectified_for_baumuster(self, baumuster):
        filtered_code_optionals = []
        for optional_id in self.code_optionals:
            if baumuster.contains_code(optional_id):
                filtered_code_optionals.append(optional_id)
        return Optional(self.id, filtered_code_optionals)
