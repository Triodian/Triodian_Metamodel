# Adding a jurisdiction

This is how a jurisdiction is added to the Triodian app suite: the Metamodel's reference data, the AI Obligations Atlas, the engagement apps (AI Board Direction, AI Risk Appetite, AI Use Assessment, AI Confidentiality Exposure Assessment), Triodian Start, the installer and the website. Anyone running the suite can follow it. It covers the suite only; it says nothing about any organisation's legal position, which is for counsel admitted in the jurisdiction.

The method was revised in November 2026, after the United States was added (development plan step 4 and website checklist W), and again on 16 November when a layer-by-layer comparison of the United States with Australia showed where a jurisdiction can meet every step and still fall short of the first jurisdiction. [What the United States taught](#what-the-united-states-taught) at the end records what changed and why.

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

## Jurisdiction codes

Settle this in J.1, before any record is written. Changing a code after records are published means an update submission for every record it touches.

- **The code follows the legislature that made the law.** National or federal law (statutes, prudential standards, federal agency rules) takes the country code (`AU`, `US`). A state's or territory's statute takes its ISO 3166-2 code (`US-NY`, `US-CO`, `AU-NSW`).
- **A model a state has to adopt stays at the country code.** A multistate model (such as an insurance regulators' association's model bulletin) is recorded once at the country code; a state's own adoption, if recorded, takes the state's code.
- **The regulator or body follows the same rule.** A state's department or legislature carries the state's code.
- **A state belongs to its country.** Asking the Atlas for a country lists its national records and every state's; asking for a state lists that state's and the national ones. The Atlas names each state in `SUBDIVISIONS` (`src/core/atlas.js`); add the jurisdiction's states there in J.3.

## Steps

Each step is one pull request per repository unless the step says otherwise. Check that no pull request is open in a repository before starting a step in it. Merge in the order of the steps: later steps read what earlier steps publish.

| # | Step | Where | Done when |
| --- | --- | --- | --- |
| J.1 | **Scope.** The jurisdiction's regulators and instruments by tier; the candidate sectors scored; the five chosen; the code rule applied to the jurisdiction's federal or state structure; the official source for each instrument; the open leads for the jurisdiction already in the review queue | A research note, dated; the review queue | The five are recorded with their scores; every instrument has a code and an official source; the open leads are listed |
| J.2 | **Reference data.** Every selectable sector in `reference-data/regulated-sectors.json`, with its entity types, its regulators, `mainSector: true` on the five, and `baselineProfiles` naming the baselines it builds on | This repository; then each app's copy (`node tools/sync-sectors.mjs` in each engagement app) | `python3 scripts/validate.py` passes; every app lists the sectors |
| J.3 | **Atlas round.** Obligations for each main sector, each with its source, tier and code, at the depth of the first jurisdiction: a research brief per main sector that breaks each instrument into the obligations it imposes (an inventory, a validation, a contract term, a board report, a notification), not one record per instrument; the jurisdiction (and its states) in the Atlas's tables; records submitted through the review queue, approved, and published by a snapshot refresh | obligations-atlas `data/research` (one brief per sector), `data/seed`, `src/core/atlas.js`; the review queue (Reasoning Fabric) | Records published in the snapshot; open leads for the same instruments closed; a matter brief for each main sector lists at least six records of its own, and the jurisdiction's record count is within reach of the first jurisdiction's (Australia: about 40) |
| J.4 | **Sector packs.** Each main sector's pack is its baseline plus the jurisdiction's overlay, written once in `content/overlays/<code>.json` in each app and built by the app's overlay tool. Board Direction: areas (the baseline's), failure cases for the director briefing, uses boards commonly consider ruling out. Risk Appetite: the documents an entity in the sector usually holds; a consequence prompt where the sector needs one. Use Assessment: arrangement types, document list. Same pack ids in every app | Each app's `content/overlays/`; Board Direction `tools/sync-overlays.mjs`, Risk Appetite and Use Assessment `tools/build-overlay-packs.mjs`, then `tools/build-content.mjs` | Each main sector opens with its pack, and only in its jurisdiction; golden copies change by additions only |
| J.5 | **Worked examples.** One fictional organisation per main sector, labelled fictional on every screen, the same organisation carried from one app to the next, in every engagement app (AI Confidentiality Exposure Assessment included: one matter in the jurisdiction's own terms); Triodian Start accepts each example id and opens it in every app; the jurisdiction's regulated example added to the suite's chain test | Each app's example files; Triodian Start (`EXAMPLE_SECTORS` in `lib/identity/try-first.js`, the picker and the guide); triodian-install `suite/chain` | Each example runs end to end with every app check passing; Start opens the jurisdiction's example in every app, not a default; the chain test runs the jurisdiction's regulated example through Board Direction, Risk Appetite and Use Assessment in both legs of the suite workflow |
| J.6 | **Installer and defaults.** The jurisdiction code, its default sector; every app reads the defaults at first sign-in and starts a new engagement on `TriodianPacks.startPack` | triodian-install (README, an answers file, tests); each app's `wrangler.jsonc` defaults and `/api/me` | A test deployment installs with the new jurisdiction; every sector the installer offers lands on a pack of its jurisdiction or a baseline, in every app |
| J.7 | **Home-jurisdiction sweep.** Search every repository for the terms of the jurisdictions already in the suite (supervisor names, instrument numbers, currency symbols, fee amounts, place names in labels) and make each one depend on the engagement's jurisdiction or remove it; name the new jurisdiction in the suite description and coverage lines | All suite repositories: app shared code, method texts, user guides, Atlas MCP and API pages, Start's *What the apps cover*, practice-hub | No output, tag, label or method text names another jurisdiction's supervisor or fee unless the engagement is in that jurisdiction |
| J.8 | **Website.** A jurisdiction page in the site's pattern, linked from the menu, the footer and the regulated-entities pages; fees in the jurisdiction's currency; the cost estimator's jurisdiction with its own rate table; the site's work log | triodian_website (its `CLAUDE.md` sets the page rules) | `python3 tests/seo_check.py` passes; the page carries *Regulatory position as at* its date |
| J.9 | **Counsel and re-check.** Counsel admitted in the jurisdiction reviews the research note, the jurisdiction page, the overlay wording and the evidence mapping (J.10); the dates are re-checked each quarter | The research note; the jurisdiction page; the evidence module | Counsel's review recorded; the next re-check dated |
| J.10 | **Evidence regimes and jurisdiction-bound wording.** The evidence index maps every output to the jurisdiction's own regime per main sector (the supervisor's instrument and paragraph) beside the shared ISO/IEC 42001 and NIST AI RMF columns, so the index for the jurisdiction reads as the first jurisdiction's does; the automated-decisions question, the privilege marking, the notification-hours default and the output footers take their text from the jurisdiction's overlay; the Atlas jurisdiction matrix carries the jurisdiction's incident clocks; the security answer pack gains the section a reviewer in that jurisdiction asks for; the running-an-engagement guides gain the jurisdiction's variant of each section that names an instrument | `public/shared/evidence.js` (identical in the three apps); each app's overlay and content; obligations-atlas (jurisdiction matrix); triodian-install `docs/security-answers.md`; Triodian/docs guides and mapping pages | The evidence index for the jurisdiction's regulated example lists its regime by instrument, with none yet where there is nothing; no screen or output of an engagement in the jurisdiction names another jurisdiction's instrument, regulator or date (a test per app asserts it); the clocks and the answer-pack section exist; the mapping is marked as the suite's reading for counsel to confirm |

### J.1 Scope: what to settle before writing anything

- **The code rule** (above), applied to the jurisdiction's structure: which instruments are national, which are state, which are multistate models.
- **Official sources.** The Atlas's dataset policy ranks sources: a *binding* record cites a rank 1 source (the instrument itself, on the legislature's or regulator's own site); *expected* and *anticipated* records cite rank 2 or better. Find the official text in J.1, not at submission.
- **Open leads.** Earlier rounds and agents leave leads in the review queue. A proposal for an instrument that already has a lead is refused as a duplicate. List the jurisdiction's open leads in J.1 so J.3 promotes them rather than colliding with them.
- **Instruments that have moved.** Check each instrument's current status on its source, not from memory: supervisory guidance is replaced and rescoped without a change of name (the US model-risk letter of 2011 was replaced in April 2026, with generative and agentic AI outside the new letter's scope).

### J.3 Atlas round: how a submission goes through

1. Research file in `data/research`; build the submission with `data/seed/build-submission.mjs`. Proposal ids carry the change file's name.
2. Submit through the connector to the review queue. A proposal that matches an open lead promotes the lead; a lead approved before promotion existed is closed with `data/seed/build-close-leads.mjs`.
3. A refused proposal is rebuilt with `data/seed/build-resubmission.mjs`, not edited by hand.
4. A code changed after publication goes as an update with `data/seed/build-jurisdiction-update.mjs`: one update per published record, changing only the jurisdiction.
5. Approve, then run the snapshot refresh. The tests the refresh runs check properties (a record’s code belongs to its country), not record versions or a fixed count; otherwise the refresh fails when the records it brings in change them.
6. Rebuild what reads the published snapshot: matter briefs in the worked examples (Board Direction `tools/build-us-example-briefs.mjs` for the United States; a new jurisdiction gets the same tool), and Start's coverage line.

### J.3 Atlas round: depth

A jurisdiction's first round tends to produce one record per instrument, which is enough for a matter brief to name the instrument and not enough for an engagement to work from. The first jurisdiction's records are the measure: each instrument is broken into the obligations it imposes, each with its own paragraph reference, tier and key dates, so that a Use Assessment finding or a Board Direction question can cite the obligation, not the instrument. Write one research brief per main sector before the round, listing the instruments and the obligations each yields, and submit sector by sector.

### J.5 Worked examples: what to check

- Every check in the app passes on the example (Risk Appetite: every decision has its reason and every measure an owner).
- An example that loads a matter brief waits for the records to be published. A trial on the preview snapshot is marked as preview in every brief.
- Examples are built from a factory, so opening one does not change the state of the next.
- The organisations, people and counsel firms are invented, and say so.

## Rules

- **Overlay, not replacement.** A main sector's pack is its baseline plus the jurisdiction's obligations. A sector with no baseline (such as Australian superannuation) carries its pack as an overlay alone.
- **A pack belongs to its jurisdiction.** An overlay pack is offered only in its jurisdiction; another jurisdiction's pack is never suggested by entity type alone.
- **Tiers stay honest.** Guidance stays *expected*, proposals stay *anticipated*, standards an organisation chooses stay *adopted*. Only law and binding instruments are *binding*.
- **No legal conclusions.** Packs and examples describe what an organisation might set and record. Whether an obligation applies is counsel's question.
- **Each supervisor's terms in its own jurisdiction.** An output, evidence tag or label names a supervisor or instrument only when the engagement is in that jurisdiction. Until J.10 has mapped the jurisdiction's regimes, the evidence index outside the first jurisdiction carries the international standard alone; once mapped, it carries the jurisdiction's own regime beside it.
- **No currency or fees in the apps.** The apps have no currency setting and amounts are free text. Method texts and guides carry no fee and no firm name; fees are published per jurisdiction on the website, in its currency, as conversions of the reference schedule.
- **Golden copies change by additions only.** A change that alters an existing golden copy is a regression until shown otherwise.
- **Re-check each quarter.** Instruments change; the research note and the jurisdiction page carry the date they were checked.

## What the United States taught

The United States was added on 14 and 15 November 2026. These are the points where the earlier method fell short, and what now covers each one.

| What happened | Now covered by |
| --- | --- |
| State laws were first recorded at `US` with the state in the title. Moving them to state codes after publication took an update for seven published records, two held records, Atlas filter and naming changes, and a matching move for one Australian state statute | [Jurisdiction codes](#jurisdiction-codes), settled in J.1 |
| Three proposals were refused as duplicates of leads already in the queue; promotion had to be added to the review queue, and two leads approved before it stayed open until closed by hand | J.1 *Open leads*; J.3 steps 2 and 3 |
| A snapshot refresh failed on tests that assumed the old versions, and again on tests that assumed every Australian record is `AU` | J.3 step 5 |
| The guidance one sector's pack drew on had been replaced months before; the research note was corrected during the Atlas round | J.1 *Instruments that have moved* |
| Every output in three apps carried the Australian supervisor's letter and standard as evidence tags whatever the pack; labels in two apps said Singapore; a US financial institution was offered the Singapore pack | J.7; rules *A pack belongs to its jurisdiction* and *Each supervisor's terms in its own jurisdiction* |
| Triodian Start dropped example ids it did not know, so a US choice opened the Australian example | J.5 done-when; `EXAMPLE_SECTORS` named |
| The Board Direction US examples could not be built until the US records were published | J.3 step 6; J.5 *waits for the records to be published* |
| Only one app read the installer's default jurisdiction and sector; a US install of the other two started on an Australian pack | J.6 done-when: every app, every offered sector |
| Two apps' method texts quoted Australian fees, and one named a law firm | J.7; rule *No currency or fees in the apps* |
| The suite description, the Atlas's MCP and API coverage lines, Start's coverage and the website's Atlas page each named the earlier jurisdictions only | J.7 *name the new jurisdiction in the suite description and coverage lines* |
| The website, its fees and the cost estimator were a separate checklist after the apps | J.8 |
| On 16 November a layer-by-layer comparison with Australia found the United States had met every step and still had 17 Atlas records to Australia's 41, no example in the chain test, no US matter in the confidentiality app, an evidence index that listed ISO/IEC 42001 alone, an automated-decisions question and privilege wording written for Australian law, no incident clocks, Australian engagement guides and an answer pack shaped for an Australian prudential reviewer | J.3 depth; J.5 chain and every app; J.10 |
