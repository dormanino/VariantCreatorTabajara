import json
from Data.DataPoint import DataPoint
from Models.Optional import Optional
from Models.Optionals import Optionals
from Models.Baumuster import Baumuster
from Models.Code import Code
from Models.Variant import Variant


class DataProvider:

    def __init__(self):
        self.optionals = self.load_optionals()

    @staticmethod
    def load_optionals():
        # TODO: fetch from external data provider
        data = json.load(open(DataPoint.data_optionals))
        optionals = []
        for optional_data in data:
            optional = Optional(optional_data['id'], optional_data['neg'])
            optionals.append(optional)
        return Optionals(optionals)

    def load_baumuster(self, baumuster_id):
        # TODO: fetch from external data provider by baumuster_id
        data = json.load(open(DataPoint.data_baumuster))
        codes = []
        for code_data in data:
            code_id = code_data['id']
            optionals = self.optionals.find(code_id)
            code = Code(code_id, optionals, code_data['isbasic'], code_data['rule'])
            codes.append(code)

        return Baumuster(baumuster_id, codes)

    # FIXME: Remove this in favor of self-analysis in Baumuster - THIS IS JUST A SAMPLE!!!!!
    @staticmethod
    def load_sample_variant(baumuster: Baumuster) -> Variant:
        data = json.load(open(DataPoint.data_basic_variant))
        optionals = DataProvider.load_optionals()
        codes: [Variant] = []
        for code_data in data:
            code_id = code_data['id']
            optional = optionals.find(code_id)
            if optional is not None:
                optional = optional.rectified_for_baumuster(baumuster)
            code = Code(code_id, optional, code_data['isbasic'], code_data['rule'])
            codes.append(code)

        return Variant("Basic", codes)
