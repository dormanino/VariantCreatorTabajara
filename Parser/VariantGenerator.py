import sys
from Data.DataProvider import DataProvider
from Helper.Utils import Utils
from Models.Variant import Variant
from Parser.CodeRuleParser import CodeRuleParser
import itertools


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
    def basic_combinations_generator(code_groups):
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
    def extra_suffixes_generator(code_groups):
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
    def extra_combinations_generator(basic_combination, extra_code_groups):
        for extra_suffix in VariantGenerator.extra_suffixes_generator(extra_code_groups):
            extra_combination = basic_combination.copy()
            extra_combination.extend(extra_suffix)
            yield extra_combination

    @staticmethod
    def remove_prefix(codes):
        for code in codes:
            yield code.id[2:]

    @staticmethod
    def validate(combination, baumuster):

        if not combination:
            return False

        noprefix_codes = list(VariantGenerator.remove_prefix(combination))
        for code in combination:
            baumuster_code = baumuster.find_code(code.id)
            if baumuster_code is None:
                return False  # check if code is in baumuster
            elif not CodeRuleParser.validate(baumuster_code.rule, noprefix_codes):
                return False  # validate code rules against baumuster

        return True

    @staticmethod
    def variant_description(baumuster, basic_index, extra_index):
        return baumuster.id + '-' + str(basic_index) + '-' + str(extra_index)

    @staticmethod
    def variants_generator(baumuster):
        codes_analysis = VariantGenerator.codes_analysis(baumuster)
        basic_code_groups = codes_analysis[1]
        extra_code_groups = codes_analysis[2]

        basic_index = 0
        for basic_combination in VariantGenerator.basic_combinations_generator(basic_code_groups):
            extra_index = 0
            if VariantGenerator.validate(basic_combination, baumuster):
                basic_index += 1
                yield Variant(VariantGenerator.variant_description(baumuster, basic_index, extra_index), basic_combination)
                for extra_combination in VariantGenerator.extra_combinations_generator(basic_combination, extra_code_groups):
                    if VariantGenerator.validate(extra_combination, baumuster):
                        extra_index += 1
                        yield Variant(VariantGenerator.variant_description(baumuster, basic_index, extra_index), extra_combination)
