"""Reserved markers and namespaces.

Implements the Gate 7 poison pill from Document 01A Part B.

Any record emitted by a test harness carries the marker field and uses the reserved
identifier namespace. Production ingestion hard-rejects both. This is the control that
assumes Gates 1 to 6 have all failed.

THE VALUE AND THE REFUSAL LIVE IN ONE FILE, DELIBERATELY — D122
---------------------------------------------------------------

`bears_synthetic_marker` is defined below `REFUSED_MARKER_VALUES`, in the same module,
installed as one unit. **A deployment therefore cannot hold the new value without also
holding the refusal for the old one.** That is what makes renaming this value safe at
all: the dangerous skew — a product that has forgotten an older marker meeting a harness
that still stamps it — cannot be assembled from these parts.

WHY THE OLD VALUE IS NEVER REMOVED
----------------------------------

`REFUSED_MARKER_VALUES` only ever grows. Removing a superseded value would mean a
corpus generated before the change, replayed afterwards, is no longer recognised as
synthetic — **and is therefore accepted into a production store.**

The failure is entirely one-directional. Keeping an extra string costs one frozenset
entry and refuses a little more than strictly necessary; dropping one accepts fabricated
employee records as real. The instinct to tidy this list is the hazard, so it is named
here rather than left to somebody's judgement at the time.
"""

# Field name every harness record must carry.
SYNTHETIC_MARKER_FIELD = "__synthetic_source__"

# Value that field must hold, and the ONLY value emitters stamp.
#
# **RENAMED FROM `PSEUDOHCM-...` BY D122**, for two reasons.
#
# It named one harness when there are four: a financial metric and a supply-chain
# measure both arrived stamped `PSEUDOHCM`, sending anyone investigating a rejected
# record to the wrong repository.
#
# And `PSEUDO` was the wrong word for an HR product. **"Pseudonymised data" is a term of
# art — GDPR Article 4(5) — meaning REAL personal data with identifiers replaced, which
# remains personal data and must be PROTECTED.** This marker means fabricated data that
# must be REFUSED. A privacy officer reading `PSEUDO...-DO-NOT-INGEST` in a rejection log
# could reasonably conclude the system was refusing pseudonymised production records,
# and the misreading runs in the dangerous direction.
#
# `SYNTHETIC` is the word the rest of this machinery already uses: the field above, the
# function below, and the constant's own name. Only the value disagreed.
SYNTHETIC_MARKER_VALUE = "SYNTHETIC-TEST-HARNESS-DO-NOT-INGEST"

# Every value production must refuse. **Grows, never shrinks** — see the module
# docstring. The current value is included by reference rather than repeated, so the two
# cannot fall out of step.
REFUSED_MARKER_VALUES = frozenset({
    SYNTHETIC_MARKER_VALUE,
    # D122. Stamped by every harness corpus generated before 20 September 2026. Files
    # on disk still carry it, and a replayed corpus must still be refused.
    "PSEUDOHCM-TEST-HARNESS-DO-NOT-INGEST",
})

# All harness identifiers begin with this. Production validation rejects the prefix.
#
# **NOT RENAMED, AND THE REASON IS COST RATHER THAN PRINCIPLE — D122.** The same
# objection applies: `PSEUDO::` prefixes every identifier in every corpus, so it is far
# more visible than the marker field, and it reads as *pseudonymised* more readily.
#
# But unlike the marker value, this prefix is written as a LITERAL in roughly twenty
# assertions across all four emulator test suites and in one emulator's CI workflow.
# Renaming it is a five-repository change that would put four public repositories red
# at once if anything were missed — a different size of decision from the one taken
# here, and one that deserves to be taken on its own.
RESERVED_ID_NAMESPACE = "PSEUDO::"


def bears_synthetic_marker(record: dict) -> bool:
    """True if a record carries any refused harness marker or a reserved identifier.

    **MEMBERSHIP, NOT EQUALITY — D122.** This read

        record.get(SYNTHETIC_MARKER_FIELD) == SYNTHETIC_MARKER_VALUE

    which is exact equality against whatever value happened to be current. A record
    stamped with a superseded marker returned False and would have been **accepted into
    production**. The rename is what surfaced it; the defect was latent from the moment
    a second value became possible.
    """
    if record.get(SYNTHETIC_MARKER_FIELD) in REFUSED_MARKER_VALUES:
        return True
    for key, value in record.items():
        if key.endswith("_id") or key == "id":
            if isinstance(value, str) and value.startswith(RESERVED_ID_NAMESPACE):
                return True
    return False
