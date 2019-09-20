from base64 import b64encode


class IntrinsicFunctionResolver(object):

    def __init__(self, params, mappings):
        self.params = params
        self.mappings = mappings

    def resolve(self, function):
        if not isinstance(function, dict):
            return function

        (function, function_body), = function.items()

        if function in ["Ref", "Fn::ImportValue"]:
            return self.params.get(function_body)

        elif function == "Fn::Join":
            delimiter, values = function_body
            return delimiter.join([self.resolve(value) for value in values])

        elif function == "Fn::FindInMap":
            map_name, top_level_key, second_level_key = function_body
            return self.mappings[self.resolve(map_name)][self.resolve(top_level_key)][self.resolve(second_level_key)]

        elif function == "Fn::Sub":
            replacements = self.params
            if type(function_body) is list:
                string, custom_replacements = function_body
                replacements.update(custom_replacements)
            else:
                string = function_body
            for var_name, var_value in replacements.items():
                var_value = self.resolve(var_value)
                if isinstance(var_value, str):
                    string = string.replace(f"${{{var_name}}}", var_value)
            return string

        elif function == "Fn::Select":
            index, list_values = function_body
            return self.resolve(list_values)[int(index)]

        elif function == "Fn::Split":
            delimeter, source_string = function_body
            return self.resolve(source_string).split(delimeter)

        elif function == "Fn::And":
            part_1, part_2 = function_body
            return self.resolve(part_1) and self.resolve(part_2)

        elif function == "Fn::Or":
            part_1, part_2 = function_body
            return self.resolve(part_1) or self.resolve(part_2)

        elif function == "Fn::Not":
            return not self.resolve(function_body[0])

        elif function == "Fn::Equals":
            part_1, part_2 = function_body
            return self.resolve(part_1) == self.resolve(part_2)

        # TODO: Implement condition resolver
        # elif function == "Condition":
        # {"Condition": "SomeOtherCondition"}
        # TODO:Conditions aren't supported yet, so this code can't be evaluated
        # elif function == "Fn::If":
        #     condition, true_section, false_section = function_body
        #     if self.resolve(condition):
        #         return self.resolve(true_section)
        #     else:
        #         return self.resolve(false_section)

        elif function == "Fn::Base64":
            return str(b64encode(self.resolve(function_body).encode("utf-8")), "utf-8")
