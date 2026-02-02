from pycfmodel.model.cf_model import CFModel
from pycfmodel.model.resources.dynamic_resource import (
    clear_dynamic_model_cache,
    disable_dynamic_generation,
    enable_dynamic_generation,
    is_dynamic_generation_enabled,
)


def parse(template):
    return CFModel.model_validate(template)


__all__ = [
    "CFModel",
    "parse",
    "enable_dynamic_generation",
    "disable_dynamic_generation",
    "is_dynamic_generation_enabled",
    "clear_dynamic_model_cache",
]
