from Models import Code


class Variant:

    def __init__(self, variant_id: str, codes: [Code]):
        self.id = variant_id
        self.codes = codes

    def parsable_string(self):
        return '+'.join(self.codes)
