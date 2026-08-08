"""AIeConA adapter contract.

Interface specification only. No data, no logic, no implementation.

Consumers pin a version. Nothing here imports from `aiecona` or `pseudohcm` — that is
what allows the product and the test harness to depend on this without depending on
each other.
"""
from contract.version import CONTRACT_VERSION

__all__ = ["CONTRACT_VERSION"]
