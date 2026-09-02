"""The adapter interface.

READ-ONLY BY CONSTRUCTION.

There is deliberately no write, update, delete or upsert operation defined here.
This is not a permission an administrator can loosen — the capability is absent
from the interface. See Document 01 §3.3.
"""

from typing import Iterator, Protocol, runtime_checkable


class Page(Protocol):
    """One page of records from a source system."""

    records: list[dict]
    cursor: str | None
    has_more: bool


@runtime_checkable
class SourceReader(Protocol):
    """What a source system must offer to be readable.

    Every method reads. None writes. Adding a write method to this Protocol
    is a change that requires owner sign-off (Document 01 §3.3).
    """

    def describe(self) -> dict:
        """Return capability metadata: entities offered, delta support, limits."""
        ...

    def read_full(self, entity: str, *, page_size: int) -> Iterator[Page]:
        """Full extract of one canonical entity."""
        ...

    def read_delta(self, entity: str, *, since: str, page_size: int) -> Iterator[Page]:
        """Records changed since a watermark. Raises if delta is unsupported."""
        ...


# Enumerated so a profile cannot declare a target outside the model.
CANONICAL_ENTITIES = (
    "Person", "Position", "Job", "LevelEquivalence", "CompensationBand",
    "BandPositionDistribution", "OrgUnit", "Assignment", "MovementEvent",
    "ContingentWorker", "CustomerSkillTerm", "SkillAssertion",
    "PerformanceEvent", "RatingScale", "PerformanceCycle",
    "Requisition", "Candidate", "Application", "PipelineStage",
    "BusinessUnitMetric", "Offering", "StrategicPriority",
    # D90. `RoleRequiredTerm` was in the schema, in the HCM partition's remit and
    # ABSENT HERE — so an adapter author reading this list would not know a job
    # description's required skills could be supplied at all, and the partition
    # allowlist refused the target because this list is what it validates against.
    #
    # Two guards agreeing on a wrong answer looked like a boundary and was a gap.
    "RoleRequirement", "RoleRequiredTerm", "RoleInteraction",
)
