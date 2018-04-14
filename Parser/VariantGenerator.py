import sys
from Data.DataProvider import DataProvider
from Helper.Utils import Utils
from Models.Variant import Variant
from Parser.CodeRuleParser import CodeRuleParser


class VariantGenerator:

    @staticmethod
    def extract_base_variant(baumuster):
        # TODO: Extract basic variant through self-analysis
        return DataProvider.load_sample_basic_variant()

    @staticmethod
    def codes_analysis(baumuster):
        analyzed_codes = []
        inconsistent_codes = []
        basic_code_groups = []
        extra_code_groups = []

        # rectify codes optionals for baumuster
        for code in baumuster.codes:
            if code.optional is None:
                inconsistent_codes.append(code)
                analyzed_codes.append(code)
            else:
                code.optional = code.optional.rectified_for_baumuster(baumuster)

        # breakdown basic code groups
        base_variant = VariantGenerator.extract_base_variant(baumuster)
        for base_code in base_variant.codes:
            if base_code.optional is None:
                continue

            code = baumuster.find_code(base_code.id)
            basic_code_group = [code]
            analyzed_codes.append(code)

            for optional_id in code.optional.code_optionals:
                optional_code = baumuster.find_code(optional_id)
                basic_code_group.append(optional_code)
                analyzed_codes.append(optional_code)

            basic_code_groups.append(basic_code_group)

        # separate out extra codes
        extra_codes = baumuster.codes.copy()
        for code in analyzed_codes:
            if code in extra_codes:
                extra_codes.remove(code)

        # breakdown extra code groups
        for code in extra_codes:
            if code in analyzed_codes:
                continue

            extra_code_group = [code]
            analyzed_codes.append(code)

            for optional_id in code.optional.code_optionals:
                optional_code = baumuster.find_code(optional_id)
                extra_code_group.append(optional_code)
                analyzed_codes.append(optional_code)

            extra_code_groups.append(extra_code_group)

        return inconsistent_codes, basic_code_groups, extra_code_groups

    @staticmethod
    def generate_basic_combinations(code_groups):
        _code_groups = code_groups.copy()

        fixed_codes = []
        for group in code_groups:
            if len(group) == 1:
                fixed_codes.append(group[0])
                _code_groups.remove(group)

        combinations = [fixed_codes]
        for group in _code_groups:
            expanded_combinations = []
            for combination in combinations:
                for code in group:
                    expanded_combination = combination.copy()
                    expanded_combination.append(code)
                    expanded_combinations.append(expanded_combination)
            combinations = expanded_combinations

        return combinations

    @staticmethod
    def generate_extra_combinations(code_groups):
        for group in code_groups:
            for code in group:
                yield [code]

        # combinations = []
        # new_combinations = []
        #
        #     for combination in combinations:
        #         new_combination = combination.copy()
        #
        #         for code in group:
        #             new_combination.append(code)
        #             new_combinations.append(new_combination)
        #             new_combination.remove(code)
        #
        #     combinations.extend(new_combinations)

    @staticmethod
    def generate_all_combinations(basic_combinations, extra_combinations):
        for basic_combination in basic_combinations:
            yield basic_combination
            for extra_combination in extra_combinations:
                new_combination = basic_combination.copy()
                new_combination.extend(extra_combination)
                yield new_combination

    @staticmethod
    def validate(combination, baumuster):

        if not combination:
            return False

        noprefix_codes = []
        for code in combination:
            noprefix_codes.append(code.id[2:])

        for code in combination:
            baumuster_code = baumuster.find_code(code.id)
            if baumuster_code is None:
                return False  # check if code is in baumuster

            if not CodeRuleParser.validate(baumuster_code.rule, noprefix_codes):
                return False  # validate code rules against baumuster

        return True

    @staticmethod
    def generate_variants(baumuster):

        codes_analysis = VariantGenerator.codes_analysis(baumuster)
        basic_code_groups = codes_analysis[1]
        extra_code_groups = codes_analysis[2]
        basic_combinations = VariantGenerator.generate_basic_combinations(basic_code_groups)
        extra_combinations = VariantGenerator.generate_extra_combinations(extra_code_groups)
        combinations = VariantGenerator.generate_all_combinations(basic_combinations, extra_combinations)

        # Utils.print_list_info('Basic Combinations', basic_combinations)
        # Utils.print_list_info('Extra Combinations', extra_combinations)
        # Utils.print_list_info('All Combinations', combinations)

        # filter valid variants
        variant_index = 0
        for combination in combinations:
            if VariantGenerator.validate(combination, baumuster):
                variant_index += 1
                yield Variant(variant_index, combination)
