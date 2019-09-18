from base64 import b64encode


class IntrinsicFunctionResolver(object):

    def __init__(self, params, mappings):
        self.params = params
        self.mappings = mappings

    def resolve(self, function):
        if type(function) is not dict:
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
            if type(function_body) is list:
                string, replaces = function_body
                for var_name, var_value in replaces.items():
                    string = string.replace(f"${{{var_name}}}", self.resolve(var_value))
            else:
                string = function_body
                for var_name, var_value in self.params.items():
                    string = string.replace(f"${{{var_name}}}", self.resolve(var_value))
            return string

        elif function == "Fn::Select":
            index, list_values = function_body
            return self.resolve(list_values)[int(index)]

        elif function == "Fn::Split":
            delimeter, source_string = function_body
            return self.resolve(source_string).split(delimeter)

        elif function == "Fn::If":
            condition, true_section, false_section = function_body

            if self.resolve(condition):
                return self.resolve(true_section)
            else:
                return self.resolve(false_section)

        elif function == "Fn::Base64":
            return b64encode(self.resolve(function_body))
