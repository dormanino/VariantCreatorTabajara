from enum import Enum


class ParserOperation(Enum):
    PARENTHESIS = 1
    OR = 2
    AND = 3
    ITEM = 4


class CodeRuleParser:

    @staticmethod
    def validate(code_rule, variant_codes):
        open_parenthesis = '('
        close_parenthesis = ')'
        or_operator = '/'
        and_operator = '+'
        not_operator = "-"
        true_result = '%'
        false_result = '&'

        code_rule = code_rule.replace(';', '')

        if code_rule == '':
            return True
        if code_rule == true_result:
            return True
        elif code_rule == not_operator + true_result:
            return False
        elif code_rule == false_result:
            return False
        elif code_rule == not_operator + false_result:
            return True

        if open_parenthesis in code_rule:
            operation = ParserOperation.PARENTHESIS
        elif or_operator in code_rule:
            operation = ParserOperation.OR
        elif and_operator in code_rule:
            operation = ParserOperation.AND
        else:
            operation = ParserOperation.ITEM

        if operation == ParserOperation.ITEM:
            if code_rule.startswith(not_operator):
                code_rule = code_rule[1:]
                return code_rule not in variant_codes
            return code_rule in variant_codes

        level = 0
        min_index = 0
        left_side = ''
        for index, char in enumerate(code_rule):

            if operation == ParserOperation.PARENTHESIS:
                if char == open_parenthesis:
                    level += 1
                    if level == 1:
                        min_index = index + 1

                elif char == close_parenthesis:
                    if level == 1:
                        max_index = index

                        pre_condition = code_rule[min_index:max_index]
                        pre_condition_validation = CodeRuleParser.validate(pre_condition, variant_codes)
                        symbol = true_result if pre_condition_validation else false_result

                        replace_str = open_parenthesis + pre_condition + close_parenthesis
                        code_rule = code_rule.replace(replace_str, symbol)
                        return CodeRuleParser.validate(code_rule, variant_codes)
                    else:
                        level -= 1

            elif operation == ParserOperation.OR:
                if char == or_operator:
                    is_left_valid = CodeRuleParser.validate(left_side, variant_codes)
                    right_side = code_rule[index + 1:]
                    is_right_valid = CodeRuleParser.validate(right_side, variant_codes)

                    return is_left_valid or is_right_valid
                else:
                    left_side += char

            elif operation == ParserOperation.AND:
                if char == and_operator:
                    is_left_valid = CodeRuleParser.validate(left_side, variant_codes)
                    if is_left_valid is False:
                        return False
                    else:
                        right_side = code_rule[index + 1:]
                        return CodeRuleParser.validate(right_side, variant_codes)
                else:
                    left_side += char
