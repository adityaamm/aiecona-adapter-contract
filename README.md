# AIeConA Adapter Contract

Interface specification only. **No data, no logic, no implementation.**

This repository exists so that neither the product (`aiecona-hr`) nor the test harness
(`pseudohcm`) depends on the other. Both depend on this contract; nothing here depends
on either of them.

See Document 01A Part B and Document 11 §2.

## What is here

| Path | Purpose |
|---|---|
| `contract/version.py` | Contract version. Pinned by consumers |
| `contract/interface.py` | The read-only adapter interface |
| `contract/entities.py` | Canonical entity shapes the contract covers |
| `contract/profile.schema.json` | JSON Schema for adapter profiles |
| `contract/markers.py` | Reserved marker and namespace definitions (Gate 7) |

## Rules

1. Nothing in this repository may import from `aiecona` or `pseudohcm`.
2. No write, update, delete or upsert operation may be added to the interface.
3. Changes are versioned. Consumers pin a version.
