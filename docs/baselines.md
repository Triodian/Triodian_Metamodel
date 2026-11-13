# Best-practice baselines

A **baseline profile** is a sector profile that holds in any jurisdiction: the AI governance a well-run organisation in that sector would have, whatever its own regulator asks. Baselines draw on international standard setters (BCBS, FSB, IAIS, IOSCO, WHO, FATF, OECD) and adopted standards (ISO/IEC 42001, ISO/IEC 42005, NIST AI RMF, IEC 62443), never on one country's rules.

They are published as reference data:

- [`reference-data/baseline-profiles.json`](../reference-data/baseline-profiles.json), validated by `schemas/baseline-profile.schema.json`;
- [`reference-data/baseline-controls.json`](../reference-data/baseline-controls.json), validated by `schemas/baseline-control.schema.json`.

A jurisdiction's sectors point to the baselines they build on (`baselineProfiles` in `regulated-sectors.json`). The jurisdiction's own obligations, from the Atlas, are the **overlay**. See [adding a jurisdiction](adding-a-jurisdiction.md).

## The eight profiles

| ID | Profile | Governing body | Main sources |
| --- | --- | --- | --- |
| BP-BANKING | Banking | Board | BCBS third-party principles (Dec 2025); FSB third-party toolkit (2023) and AI monitoring report (Oct 2025) |
| BP-INSURANCE | Insurance | Board | IAIS Application Paper on the supervision of AI (Jul 2025) |
| BP-SECURITIES | Securities and investment advice | Board | IOSCO Supervisory Toolkit for AI use in Capital Markets (May 2026); IOSCO reports of 2021 and 2025 |
| BP-HEALTH | Health care | Board | WHO guidance on AI for health (2021) and on large multi-modal models (2024); ISO 14971 and IEC 62304 where AI is a device |
| BP-PAYMENTS | Payments and money transmission | Board | FATF Recommendations 15 and 16; CPMI-IOSCO PFMI for systemic systems; FSB toolkit. No AI-specific international source yet; the profile says so |
| BP-CI-GOVERNMENT | Critical infrastructure, government-managed | Accountable authority | Principles for the Secure Integration of AI in Operational Technology (Dec 2025); IEC 62443; NIST critical infrastructure profile (in development); OECD *Governing with AI* (2025) |
| BP-CI-CORPORATE | Critical infrastructure, corporate-managed | Board | As above, without the public-sector source |
| BP-GOVERNMENT | Government in general | Accountable authority | OECD *Governing with AI* (2025); OECD AI Principles; ISO/IEC 42005 |

Every profile also draws on ISO/IEC 42001 and the NIST AI RMF. Each gives areas of the business, critical operations, typical uses with their authority level, failure cases for the director briefing, and uses boards commonly consider ruling out (shown only if asked; never a recommendation).

**Governing body.** Where it is the accountable authority, the apps say "accountable authority" where they would say "board".

## The four controls every baseline carries

| ID | Control | What the apps hold |
| --- | --- | --- |
| BC1 | Agent controls | For each use at A3 and above: permission scope, an action log, a human checkpoint before actions at A4 and above, a way to stop it |
| BC2 | Fast path | A position set by the board or accountable authority: uses at A1 and A2 with consequence C1 or C2 approved by management within a stated number of days |
| BC3 | One evidence register | Each provider's evidence (E0 to E6) recorded once and cross-walked to every regime in the matter brief |
| BC4 | Productivity measures | Days from request to approval for a new AI use; share of AI use on sanctioned tools; both in the board view |

BC2 and BC4 exist because unapproved AI use falls when the approved route is quick, and an organisation should be able to measure that for itself.

## Rules

- A baseline source is guidance or an adopted standard. Nothing in a baseline says an organisation is obliged to follow it.
- Sources marked `draft` or `inDevelopment` are re-checked each quarter.
- Changes to a profile raise its `version`.
