---
name: aat-master
description: Route creative briefs through the AAT Astra/Sol design workflow for banners, social posts, carousels, BIPs, newsletters, landing pages and websites. Use when asked for AAT Master or the team's orchestrated design process.
metadata:
  version: "0.1.0-local-test"
  status: "Installed for local testing; human team adoption pending"
---

# AAT Master

One entry point for the existing seven-skill Team Design Runtime. Use the canonical specialist files resolved by the local runtime; do not copy them into this skill or substitute another installed skill with the same name. The repository bundles the runtime and seven specialist workflows. Run its installer once before production.

Read [REVIEW.md](REVIEW.md) before execution and handover. The user supplies a brief; they do not need to repeat model-routing or workflow instructions.

## Connect before production

Run `python3 scripts/runtime.py locate` and `python3 scripts/runtime.py status`, resolving the script relative to this SKILL.md, not the current project directory. `locate` returns the runtime root and canonical instruction paths. `status` checks pinned files, dependencies and model-role configuration. A passing status does not prove image generation, browser access, current account/model access or design quality.

Read the resolved runtime `AGENTS.md` and `RUN-A-JOB.md`. The wrapper resolves the bundled runtime first; a machine-local registry is the fallback. Machine-specific configuration stays outside shared instructions. If it is absent or invalid, report the concrete setup gap. Never silently construct a replacement runner, use a Claude adapter, edit pins or weaken checks.

The main conversation must be Astra for the requested architecture. Use known session metadata to confirm this; do not infer the model from a persona or claim a skill changed it. If it is another model or unknown, explain that the main session needs Astra. Do not silently proceed under a different architecture. The runner selects Sol builders and fresh Astra reviewers itself.

Check the actual session's built-in image-generation capability and available browser before stages requiring them. Use the host's preferred browser integration. If a required tool is missing, report the gap and complete independent preparation only; do not claim the missing stage ran.

## Route the brief

Choose by requested output, using the brief and supplied references rather than a single keyword:

| Requested output | Runtime deliverable |
|---|---|
| LinkedIn profile/company cover or banner | `linkedin-banner` |
| Individual static LinkedIn/social graphic | `linkedin-static` |
| LinkedIn swipeable slide series/carousel | `linkedin-carousel` |
| Business Information Pack (BIP), company information document | `bip` |
| Email newsletter, email concept or newsletter HTML | `email-newsletter` |
| One marketing/campaign landing page | `landing-page-director` |
| Multi-page marketing website | `website` |

An unfamiliar acronym such as “DIT” is not automatically a BIP. Infer it only when the attached brief establishes the meaning; otherwise ask one concise scope question. Unsupported deliverables need clarification rather than a forced match.

For banners, resolve personal versus business from the brief and use only that destination's prototype; ask if the destination remains ambiguous. Distinguish a website containing a landing page from two separately requested deliverables. For mixed briefs, inventory every task and requested option, then process one task at a time. Stop after its reviewed output for the user's assessment before beginning the next, unless the user explicitly requests a different sequence.

Read the selected `<runtime>/.agents/skills/<deliverable>/SKILL.md` and `REVIEW.md` fully, plus their required references. Record the canonical path and version in the job. Read only the relevant specialist workflow; do not run all seven.

## Execute the actual runner

Use `python3 scripts/runtime.py <command> ...` to invoke the existing runtime with its configured Python environment. The wrapper forwards `new`, `preflight`, `build`, `review`, `repair` and `handover` to the real runner. Follow the exact plan schema and procedure in `RUN-A-JOB.md`.

1. Read the real brief, approved copy, brand assets and requested variants. Gather missing consequential inputs together. Do not invent facts, claims, logos, consent or approval. Create the case inside the correct client project, not the shared runtime or installed skill. Preserve brief provenance and approved copy. For an audit or specification-only request, honour that scope without forcing production.
2. Astra establishes the direction and prepares required images/references with built-in image generation. Inspect them before builder dispatch. Keep assets in the case. Agent direction selection is not human approval. Follow the selected specialist's imagery and reference requirements.
3. Initialise the selected deliverable with explicit option count, complete its case notes and `production.json`, and run `preflight`. Honour the brief's variant count; use the runtime's documented fallback only when it is genuinely unspecified. Never bypass incomplete inputs to start production.
4. Run `build`. The runner starts separate Sol builders for the selected task's options. Do not substitute an ordinary same-model response or self-build and call it a Sol run. Stage-specific builders must not launch a competing harness.
5. Inspect the actual outputs and complete the required exports, browser/mechanical checks and evidence. For web work, retain image-first direction and required responsive/interaction testing; this runtime owns dispatch and review instead of launching a second legacy orchestration loop.
6. Run `review`. The runner uses fresh Astra visual-review sessions and final rubric review, tied to preserved source/evidence. The orchestrator's own opinion is not independent review. “Fresh” refers to a separate session, not a model named Flash.
7. For repairable failures, run `repair`, repeat affected checks and `review`, within the existing runner's repair limit. Resolve blockers honestly. Do not reset the allowance, overwrite active review evidence or change rules to obtain a pass.
8. Deliver the actual artifact links, previews, check results and remaining gaps. Preserve the distinction between agent QA, independent review and human approval. Stop for the user's final visual review. Agents do not deploy, upload, send or submit external forms; a person releases the work.

## Maintain the boundary

This invocation authorises production using the installed workflow, not edits to specialist skills, review checks, runtime tools or model settings. Record proposed general lessons in job notes for human owner review. Local test installation is not team adoption. Never report missing work, an unrun tool, a model probe or a passing structural check as a completed client design.
