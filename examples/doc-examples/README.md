# Documentation worked examples

These are the JSON worked examples from the metamodel documentation (03 Sep 2025 edition), extracted verbatim, one instance per file. `manifest.json` records which schema (and, for element-level examples, which definition) each one should validate against, and the line in the source document it came from.

Run them with:

```bash
python scripts/validate.py --only-doc-examples
```

An example that fails means the documentation and the schema disagree. Decide which one is correct, then fix the schema or update the example (and the documentation) to match.

Not included, because the repository has no schema for them yet:

- Model Risk Management sub-domain examples (model profile, governance, validation, monitoring, regulatory framework mapping)
- Cross-domain relationship examples
