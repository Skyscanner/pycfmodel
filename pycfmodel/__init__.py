from pycfmodel.model.cf_model import CFModel


def parse(template):
    return CFModel(**template)
