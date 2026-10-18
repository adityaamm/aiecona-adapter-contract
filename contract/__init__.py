"""AIeConA adapter contract.

Interface specification only. No data, no logic, no implementation.

Consumers pin a version. Nothing here imports from the product or from any test
harness — that is what allows the product and the harnesses to depend on this without
depending on each other. (Names no harness, so a release carrying this package passes
the product's artefact scan, gate 5 — D204.)
"""
from contract.version import CONTRACT_VERSION

__all__ = ["CONTRACT_VERSION"]
