from Data.DataProvider import DataProvider
from Models.Variant import Variant
from Parser.CodeRuleParser import CodeRuleParser


class VariantGenerator:

    @staticmethod
    def extract_first_variant(baumuster):
        # TODO: Extract basic variant through self-analysis
        return DataProvider.load_sample_variant(baumuster)

    @staticmethod
    def basic_variant_code_analysis(baumuster):
        inconsistent_codes = []
        fixed_codes = []
        swappable_codes = []

        first_variant = VariantGenerator.extract_first_variant(baumuster)
        for code in first_variant.codes:

            # Optional was not found on global Optionals list
            if code.optional is None:
                inconsistent_codes.append(code)

            # If Code doesn't have optionals to swap then it's fixed in all Variants from Baumster...
            elif not code.optional.code_optionals:
                fixed_codes.append(code)

            # ... else it's swappable
            else:
                swappable_codes.append(code)

        return inconsistent_codes, fixed_codes, swappable_codes

    @staticmethod
    def generate_basic_variants(baumuster):
        basic_code_analysis = VariantGenerator.basic_variant_code_analysis(baumuster)

        # simplest combination from fixed optionals
        fixed_codes = basic_code_analysis[1]
        fixed_combination = []
        for optional_code in fixed_codes:
            fixed_combination.append(optional_code)

        # generate combinations
        combinations = [fixed_combination]
        swappable_codes = basic_code_analysis[2]
        for optional_code in swappable_codes:
            swap_optionals = [optional_code]
            for optional_id in optional_code.optional.code_optionals:
                if baumuster.contains_code(optional_id):
                    optional_code = baumuster.find_code(optional_id)
                    swap_optionals.append(optional_code)

            expanded_combinations = []
            for combination in combinations:
                for swap_code in swap_optionals:
                    expanded_combination = combination.copy()
                    expanded_combination.append(swap_code)
                    expanded_combinations.append(expanded_combination)

            combinations = expanded_combinations

        # filter valid variants
        variant_list = []
        for index, combination in enumerate(combinations):
            if VariantGenerator.validate(combination, baumuster):
                name = 'Basic ' + str(index + 1)
                variant_list.append(Variant(name, combination))

        return variant_list

    @staticmethod
    def generate_extra_variants(baumuster, basic_variants):
        pass

    @staticmethod
    def generate_all_variants(baumuster):
        pass

    @staticmethod
    def validate(combination, baumuster):

        if not combination:
            return False

        noprefix_codes = []
        for code in combination:
            noprefix_codes.append(code.id[2:])

        for code in combination:
            baumuster_code = baumuster.find_code(code.id)

            # check if code is in baumuster
            if baumuster_code is None:
                return False

            # validate code rules against baumuster
            if not CodeRuleParser.validate(baumuster_code.rule, noprefix_codes):
                return False

        return True
