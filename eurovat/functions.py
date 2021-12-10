import logging
from typing import Optional

from eurovat.registry import VatRuleRegistry


logger = logging.getLogger(__name__)
_registry = None


def get_vat_rate(country_code: str, cn_code: Optional[str]=None):
    global _registry

    if _registry is None:
        logger.info(f"setup registry")
        _registry = VatRuleRegistry()
    
    return _registry.get_vat_rate(country_code, cn_code)
