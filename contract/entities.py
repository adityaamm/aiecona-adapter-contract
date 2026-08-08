"""Canonical entity shapes the contract covers.

Shapes only — no behaviour, no persistence, no validation logic. The product owns
those. This exists so a harness can conform without importing the product.
"""

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(frozen=True)
class Provenance:
    """The _prov block. Present on every entity. Document 03A §2.4."""
    src_system: str
    src_id: str
    src_object: str
    sync_id: str
    sync_at: datetime
    derived: bool = False
    derivation: str | None = None
    confidence: float | None = None


@dataclass(frozen=True)
class ValidPeriod:
    """Valid time. One clock. Every entity has this."""
    valid_from: date
    valid_to: date | None = None


@dataclass(frozen=True)
class TransactionPeriod:
    """Transaction time. The second clock.

    ONLY on Assignment and PerformanceEvent, per D7 Option B.
    """
    tx_from: datetime
    tx_to: datetime | None = None


# Which entities carry both clocks. Consumers must not widen this without D7 revision.
BITEMPORAL_ENTITIES = frozenset({"Assignment", "PerformanceEvent"})

# Which entities are append-only and carry neither period.
APPEND_ONLY_ENTITIES = frozenset({"SnapshotLedger", "AuditEvent", "RestatementMap"})


@dataclass
class CanonicalRecord:
    """A record as it crosses the contract boundary."""
    entity: str
    payload: dict
    valid: ValidPeriod
    prov: Provenance
    transaction: TransactionPeriod | None = None
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.entity in BITEMPORAL_ENTITIES and self.transaction is None:
            self.warnings.append(
                f"{self.entity} is bi-temporal but no transaction period was supplied. "
                "Backtests over this entity will carry look-ahead bias (Doc 08 §1.1a)."
            )
