"""Declared fields an adapter may supply, where the contract must say more than the
entity name — D159.

THE HR SYSTEM'S CRITICAL FLAG

Customers' HR systems commonly hold a "critical" or "key position" indicator on the
POSITION, and some on the JOB. An adapter may supply it as `hr_critical_flag` on either
entity: true, false, or absent when the system does not say. The product never treats
it as a designation. It raises a proposal, which a Master confirms one at a time; the
designation itself lives in the product's own configuration (D134, D159).

WHAT MUST NEVER ARRIVE AS IT

The same systems hold flags about the PERSON in a seat — how likely they are to leave,
what their loss would cost, whether they are a future leader. Those are judgements about
an individual. Supplied as a position's criticality they would put a judgement about a
named person into data about a role, which the product's separation of roles from
people forbids. The names below are refused as the source of `hr_critical_flag`, and an
adapter author is told so before a connector is built.
"""

HR_CRITICAL_FLAG = "hr_critical_flag"

# The entities that may carry it.
HR_CRITICAL_FLAG_ENTITIES = ("Position", "Job")

# Flags about a person, never about a position. A source field is refused if, once
# lower-cased with every separator removed, it CONTAINS any of these with theirs
# removed — so `Risk of Loss (Rating)`, `flightRisk` and `risk_of_loss` are all caught. Deliberately
# over-inclusive: refusing a field that was innocent costs one mapping; accepting one
# that was not puts a judgement about a person into position data. Only ever grows.
PEOPLE_LEVEL_FLAGS = frozenset({
    "risk_of_loss",
    "impact_of_loss",
    "reason_for_leaving",
    "key_talent",
    "future_leader",
    "emergency_cover",
    "flight_risk",
    "retention_risk",
    "high_potential",
    "potential",
    "readiness",
})
