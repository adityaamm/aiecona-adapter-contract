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
    # D95(b). `ProficiencyScale` is the direct twin of `RatingScale` — one says what a
    # rating of 3 means, the other says what a proficiency of 3 means. `RatingScale` was
    # here and its twin was not, which was an oversight rather than a boundary. Without
    # it we would have to assume a scale, and an assumed scale is a confident wrong
    # answer about a named person's capability.
    "ProficiencyScale",
    # D95(a). RENAMED from `PipelineStage`. The schema holds `pipeline_stage_event` and
    # always did; this list advertised a name no table carried, so a talent-acquisition
    # profile declaring the advertised target passed the allowlist and could never land.
    # The event form is also the correct model: time-to-hire and funnel drop-off are
    # computed from movements and their dates, neither of which a bare state supports.
    "Requisition", "Candidate", "Application", "PipelineStageEvent",
    # D95(c). Permitted ONLY where the deployment has opted in — see
    # DEPLOYMENT_OPTIONAL_ENTITIES below.
    "CandidatePersonLink",
    # D95(d). A customer's stated workforce demand. Supplying it is permitted; supplying
    # it under a basis we should be deriving is not. Ingestion accepts this entity only
    # with basis CUSTOMER_STATED, so a customer's own inference cannot arrive wearing
    # the label of ours. Our derived signals carry the other five bases and are
    # supplementary, Master-only and liability-acknowledged under D76.
    "LatentDemandSignal",
    "BusinessUnitMetric", "Offering", "StrategicPriority",
    # D90. `RoleRequiredTerm` was in the schema, in the HCM partition's remit and
    # ABSENT HERE — so an adapter author reading this list would not know a job
    # description's required skills could be supplied at all, and the partition
    # allowlist refused the target because this list is what it validates against.
    #
    # Two guards agreeing on a wrong answer looked like a boundary and was a gap.
    "RoleRequirement", "RoleRequiredTerm", "RoleInteraction",
)


# Entities an adapter may supply ONLY where the deployment has explicitly enabled the
# named option. Listed in the interface specification rather than left to the engine,
# because an integration team needs to know before they build a connector that the
# target will be refused unless the option was taken at deployment.
#
# D95(c). `CandidatePersonLink` asserts that a named candidate and a named employee are
# the same human being. That assertion has consequences — it attributes one person's
# performance to the source that hired them — and D56 put cross-system entity matching
# out of scope precisely so that we do not make it by inference.
#
# So the default is silence: we hold the link only where it can be established without
# guessing, and report nothing where it cannot. A customer who holds an authoritative
# link may supply it, as a decision taken once at deployment and recorded, rather than
# as a default nobody chose.
#
# The value is the option key the deployment must enable.
DEPLOYMENT_OPTIONAL_ENTITIES: dict[str, str] = {
    "CandidatePersonLink": "customer_supplied_candidate_person_link",
}
