# Coding and documentation

- Keep the API/backend boundary and manual default explicit. No parent checkout.
- Rust source, tests and examples start with SPDX copyright and MIT identifiers.
- Explain unsafe invariants with `// SAFETY:`; compilation alone does not prove them.
- Keep allocation, locks, file I/O and decoding off the data-mixing callback.
- Prefer structured `AudioError` results; do not silently discard control failures.
- Use rustfmt and strict Clippy; avoid unrelated formatting and dependency changes.
- Use English documentation. Rustdoc describes public signatures, errors, units,
  costs and ownership. The book connects contracts to practical workflows.
- Reference pages follow the [audio template](api/maintenance/reference_page_template.md).
- Generate inventories explicitly; never edit them by hand or hide undocumented API.
- Record performance only with a reproducible workload and measurement scope.

The [contribution guide](../CONTRIBUTING.md) defines validation order and PR format.
