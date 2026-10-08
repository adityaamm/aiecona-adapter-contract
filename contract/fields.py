"""Declared fields an adapter may supply, where the contract must say more than the
entity name — D159, D166.

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


# ---------------------------------------------------------------------------
# THE HR SYSTEM'S OCCUPATION CODE — D166 (contract 0.3.0)
#
# Some HR systems hold, on the JOB, the code of a standard occupation the job is — an
# O*NET-SOC code, or an ESCO occupation URI. An adapter may supply it as
# `hr_occupation_code`, always together with `hr_occupation_standard` saying which of
# the two it is: both, or neither. The product does not take it as the link on trust:
# it becomes the job's occupation once a Master confirms it (D165 ruling 1).
#
# Only ESCO and O*NET. A code from any other classification (ISCO-08, a national
# scheme, SOC on its own) is not one of them and must not be supplied as one (D164).
# ---------------------------------------------------------------------------

HR_OCCUPATION_CODE = "hr_occupation_code"
HR_OCCUPATION_STANDARD = "hr_occupation_standard"

# The one entity that may carry them.
HR_OCCUPATION_ENTITIES = ("Job",)

# The values `hr_occupation_standard` may take — the names the product's own
# `skill_standard` type uses.
HR_OCCUPATION_STANDARDS = ("ESCO", "ONET")


# ---------------------------------------------------------------------------
# THE HR SYSTEM'S LEGAL-ENTITY CODE — D171 (contract 0.4.0)
#
# An org unit may carry, as `legal_entity_code`, the code the customer's HR system
# gives the legal entity the unit belongs to — text, exactly as the HR system holds it.
# The customer records the same code beside each legal entity at onboarding, which is
# how the product knows which entity, and so which occupation standard (ESCO or O*NET,
# D165 ruling 2), a job's positions sit in. Absent when the system does not hold one;
# the product then asks a Master rather than guessing.
# ---------------------------------------------------------------------------

HR_LEGAL_ENTITY_CODE = "legal_entity_code"

# The one entity that may carry it.
HR_LEGAL_ENTITY_ENTITIES = ("OrgUnit",)


# ---------------------------------------------------------------------------
# SUCCESSION NOMINATIONS FROM THE HCM — D172 (contract 0.5.0)
#
# `SuccessionNomination`: one named successor for one position, as the customer's HCM
# succession module holds it — the position, the person, and the customer's own
# readiness band for them ("Ready now", "1-2 years" ...), text exactly as the HCM holds
# it, or absent. A valid window like any other record.
#
# WHAT THE PRODUCT DOES WITH IT (the owner's rulings, D134, D135, D172):
#   * held only for positions the customer has designated critical, and only for
#     current employees — anything else is not stored, only counted;
#   * a Master's own statement in the product prevails over the feed;
#   * the readiness band is the customer's judgement, shown as theirs, never fed into
#     the product's scoring;
#   * a person's nominations are deleted at the next refresh after they are on no
#     pipeline (R1, D151).
# ---------------------------------------------------------------------------

SUCCESSION_NOMINATION = "SuccessionNomination"
SUCCESSION_NOMINATION_FIELDS = ("nomination_id", "position_id", "person_id",
                                "readiness_band")
