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
    """Valid time. One clock. Every entity has this.

    HALF-OPEN: `[valid_from, valid_to)`. D67.

    `valid_to` is the first instant the version is **no longer** true, not the last
    instant it was. One version ends exactly where the next begins, with no overlap and
    no gap, which is what makes the exclusion constraints in the product's migrations
    expressible at all.

    **THIS IS A RECORD WINDOW AND NOT A REAL-WORLD FACT.** The distinction cost a
    defect, so it is stated here where both the product and any harness read it.

    Real-world employment dates use the opposite convention:

        exit_date, engagement_end   the LAST day worked — inclusive
        valid_to                    the first day the version is not true — exclusive

    So an assignment for somebody whose last day is 30 September carries
    `valid_to = 1 October`, not `valid_to = 30 September`. Mapping the exit date
    straight into `valid_to` shortens every employment by a day and makes an engagement
    that begins and ends on the same day inexpressible — `[30 Sept, 30 Sept)` contains
    no time and the product's CHECK constraint refuses it.

    Tenure in days is therefore `end - start + 1` on the real-world dates, and never
    `valid_to - valid_from` on the record window. An adapter mapping a source system's
    termination date must add a day when it writes `valid_to`.
    """
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
