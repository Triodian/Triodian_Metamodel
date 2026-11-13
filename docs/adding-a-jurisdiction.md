# Adding a jurisdiction

This is how a jurisdiction is added to the Triodian app suite: the Metamodel's reference data, the AI Obligations Atlas, and the engagement apps (AI Board Direction, AI Risk Appetite, AI Use Assessment). Anyone running the suite can follow it. It covers the suite only; it says nothing about any organisation's legal position, which is for counsel admitted in the jurisdiction.

## Depth: five main sectors at most

A jurisdiction has at most **five main sectors**. A main sector gets:

- Atlas records for its own obligations, by tier;
- a sector pack in each engagement app;
- a worked example.

Every other sector stays selectable. It uses its [baseline profile](baselines.md), if it has one, or the general path (listed companies, or organisations outside financial regulation). Main sectors differ by jurisdiction: superannuation is a main sector in Australia and nowhere else.

The validator enforces the cap: a jurisdiction with more than five sectors marked `mainSector` fails.

## Choosing the five

Score each candidate sector 0, 1 or 2 on five tests. The highest five are the main sectors; a tie goes to the sector with binding instruments.

| Test | Scores 2 when |
| --- | --- |
| Reach | A supervisor's binding or expected instruments reach AI use or the supplier chain |
| Accountability | Boards or named executives answer for third-party or model risk by statute, rule or supervisory expectation |
| Buyers | Enough organisations in the sector's upper tier to support the engagements |
| Route to market | Advisers who serve the sector (law firms, board advisers) can run the engagements |
| Fit | The sector maps onto the suite's scales (authority A1 to A6, consequence C1 to C5, evidence E0 to E6) without new code |

## Steps

| # | Step | Where | Done when |
| --- | --- | --- | --- |
| J.1 | Scope: the jurisdiction's regulators and instruments by tier; the candidate sectors scored; the five chosen | A research note | The five are recorded with their scores |
| J.2 | Reference data: every selectable sector in `reference-data/regulated-sectors.json`, with its entity types, its regulators, `mainSector: true` on the five, and `baselineProfiles` naming the baselines it builds on | This repository; then the apps' copies (Board Direction: `node tools/sync-sectors.mjs`) | `python3 scripts/validate.py` passes; the apps list the sectors |
| J.3 | Atlas research round: obligations for each main sector, each with its source and tier (binding, expected, anticipated, adopted) | obligations-atlas `data/research` and `data/seed`; submitted through the review queue | Records reviewed; a matter brief for each main sector lists its obligations |
| J.4 | Sector packs: Board Direction (areas of the business, failure cases for the director briefing, uses boards commonly consider ruling out); Risk Appetite (functions, critical operations, starting consequence thresholds); Use Assessment (arrangement types, document list). Start each pack from its baseline profile and add the jurisdiction's overlay | the apps' content files | Each main sector opens with its pack |
| J.5 | Worked examples: one fictional organisation per main sector, labelled fictional on every screen, run through the apps | the apps' example files; the suite's chain test | Each example runs end to end; the suite's tests pass |
| J.6 | Installer and configuration: the jurisdiction code, its default sector and currency | triodian-install; each app's `wrangler.jsonc` defaults | A test deployment installs with the new jurisdiction |

## Rules

- **Overlay, not replacement.** A main sector's pack is its baseline plus the jurisdiction's obligations. A sector with no baseline (such as Australian superannuation) carries its pack as an overlay alone.
- **Tiers stay honest.** Guidance stays *expected*, proposals stay *anticipated*, standards an organisation chooses stay *adopted*. Only law and binding instruments are *binding*.
- **No legal conclusions.** Packs and examples describe what an organisation might set and record. Whether an obligation applies is counsel's question.
- **Re-check each quarter.** Instruments change; the research note carries the date it was checked.
