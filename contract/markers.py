"""Reserved markers and namespaces.

Implements the Gate 7 poison pill from Document 01A Part B.

Any record emitted by a test harness carries the marker field and uses the reserved
identifier namespace. Production ingestion hard-rejects both. This is the control that
assumes Gates 1 to 6 have all failed.
"""

# Field name every harness record must carry.
SYNTHETIC_MARKER_FIELD = "__synthetic_source__"

# Value that field must hold.
SYNTHETIC_MARKER_VALUE = "PSEUDOHCM-TEST-HARNESS-DO-NOT-INGEST"

# All harness identifiers begin with this. Production validation rejects the prefix.
RESERVED_ID_NAMESPACE = "PSEUDO::"


def bears_synthetic_marker(record: dict) -> bool:
    """True if a record carries the harness marker or a reserved identifier."""
    if record.get(SYNTHETIC_MARKER_FIELD) == SYNTHETIC_MARKER_VALUE:
        return True
    for key, value in record.items():
        if key.endswith("_id") or key == "id":
            if isinstance(value, str) and value.startswith(RESERVED_ID_NAMESPACE):
                return True
    return False
