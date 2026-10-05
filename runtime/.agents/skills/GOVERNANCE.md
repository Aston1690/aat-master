# Team design governance

## Status and precedence

This is a proposed revision for human skill-owner review through GitHub. It is distributed for local testing and has not been approved as the team standard. These governance rules implement the manager’s supplied email. Within an adopted package they govern every deliverable, checklist and helper; setup notes must not create weaker exceptions. If any instruction conflicts, stop the affected action and raise the exact conflict with the owner. Do not change instructions, checks or models to make a job pass.

## One canonical version

Use one reviewed GitHub revision for the team. Each deliverable has exactly one canonical SKILL.md and REVIEW.md in this package: `linkedin-banner`, `linkedin-static`, `linkedin-carousel`, `bip`, `email-newsletter`, `landing-page-director`, `website`. Alternate drafts, ZIPs, archives and other installed skills with the same name are not additional sources of authority. The human owner designates the accepted repository/path/revision and retires obsolete active copies. Record that selection in [OWNERS.md](docs/OWNERS.md). Read the selected SKILL.md and REVIEW.md fully before every job and record their version/source revision in the client job.

## Human approval and release

The agent prepares local artifacts and inspects every option at full size and realistic feed/phone size. A human designer independently inspects every option at those sizes and records reviewer, date, artifact revision and outcome before anything goes out. A contact sheet, numerical score, automated PASS or agent opinion does not supply human approval.

Agents never deploy, upload, publish, host, post or send deliverables. This includes preview deployments, test emails, external testing-service uploads, external form submissions and pushes that trigger release. No DNS change, production alias switch or live-site replacement belongs in an agent’s design workflow. A human performs all release actions. Job-level approval is not an exception to this policy. Read-only inspection of a human-supplied live result is allowed when it has no external side effects. Image generation through the approved capability is a production tool, not approval to publish its output or expose client files through an unapproved service.

Record states separately: local agent QA; independent review if actually performed; human design approval; human release; live verification. Failed requirements fail the relevant QA. Unperformed mandatory checks are incomplete. Missing client inputs are blocked. Neither incomplete nor blocked work is client-ready. Human approval is never inferred from an automated pass or silence.

## Facts, assets and client separation

Never invent numbers, quotes, logos, customers, credentials or claims. Ask for absent facts, approved copy and verified logo/portrait assets. Use clearly labelled placeholders only in a review draft. Keep supplied brand identity and claims exact; factual verification and copy approval are separate. Illustrative artwork is not documentary proof of real people, premises, events or product functionality.

Client names, palettes, contacts, private files, personal machine paths and client-specific lessons live only in that client’s project folder. Shared samples must be neutral placeholders. Licensed stock or approved supplied imagery may be used when relevant and allowed by the brief; preserve source/licence evidence in the client folder. A no-stock or supplied-only brief takes precedence over this choice. Avoid stock filler; never treat licensed imagery as proof of a client relationship. Static posts and every carousel slide still require prominent relevant imagery.

## Changes and maintenance

Agents must not edit active skills, review checklists, checks, shared tools or model settings, including models.toml and config.toml. They record proposed lessons in client job notes. The named human skill owner makes changes through GitHub, reviews the complete diff and approves adoption. An explicitly requested draft proposal outside the active package is not adoption and must not be installed or treated as the active skill by the agent.

After a client rejection, record the issue and proposed general lesson promptly. The human owner must convert the reusable lesson into a reviewed general rule within one week. Keep client details out of the GitHub proposal. If it duplicates an existing rule or conflicts with another rule, the owner resolves that explicitly rather than accumulating contradictory notes. Track the due date and reviewed change link in [LESSONS.md](docs/LESSONS.md).

Each skill has one agreed named owner, who reviews it monthly, prunes obsolete/contradictory rules and records the outcome. Agree the owner split and tell the manager; agents do not assign people or send that message. Missing assignments and approvals remain pending in [OWNERS.md](docs/OWNERS.md).

## Review evidence

When independent review is used, preserve the exact source and evidence per revision; hashes alone do not replace the files. Do not edit evidence beneath an active review. New evidence belongs to a new supported review submission. Record which required artifacts were actually inspected; an image/context limit must produce split review with complete coverage or an explicit incomplete result. Do not label omitted artifacts passed. Do not bypass blocked checks or reset repair allowances.

These are requirements for the adopted workflow, not a claim that a helper tool enforces them. This package includes no replacement review engine and does not fix the separate repository’s parser or evidence-storage bugs.
