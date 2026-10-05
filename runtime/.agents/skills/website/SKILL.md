---
name: website
description: Design, build, revise and review multi-page marketing websites while preserving approved content, brand identity and the existing implementation stack.
metadata:
  status: "proposed; owner review pending"
  version: "1.0.3-email-review.1"
---

# Website

Produce a working, inspected website with a coherent system across its pages. Read [REVIEW.md](REVIEW.md) before starting and again before handover. Single campaign pages belong to the landing-page workflow; narrow website fixes stay proportional to the requested change.

For an explicitly requested audit, prompt or specification only, deliver that scope; do not force full production. An explicit supplied-assets-only or no-generation instruction overrides generation defaults. Content approval does not verify factual accuracy; flag unsupported claims instead of silently endorsing or rewriting them.

## Team rules for every job

Read this SKILL.md and REVIEW.md in full before every job. Record the canonical skill path, version and source revision in the client’s job notes. If an instruction is wrong, unclear or conflicts with another rule, raise it with the skill owner; do not work around it or silently select another version. The team governance in [GOVERNANCE.md](../GOVERNANCE.md) applies to every deliverable and supporting tool.

Never invent numbers, quotes, logos, credentials or claims. Ask for missing facts or verified assets; unresolved items may appear only as labelled placeholders in a review draft. Keep client names, palettes, contacts, private files and machine-specific paths in the client’s folder, never in reusable skills or samples.

The agent prepares and checks local work only. A human designer must inspect every option at full size and feed/phone size and record approval separately from automated checks. Agents never deploy, publish, upload, host, post or send deliverables, including preview deployments, test emails and real form submissions. Approval to release does not delegate release to a bot. A person performs the release.


## Account for the requested output

Before production, inventory every requested deliverable and variation with its assigned copy/source, format, destination and expected filename or route. “One example per skill” means one selected client task, including that task’s requested options unless the user explicitly reduces scope. Do not invent a fixed number of variants. Reconcile the final handover against this inventory and disclose anything missing; a draft or omitted option is not a completed deliverable.

## Establish the project

Read the current brief, approved copy, brand assets, reference pages, project instructions and repository status. Identify the actual source components, package manager, build commands, routes and shared styles before editing. Verify source identity using known content/version markers, not folder timestamps or deployment linkage alone. Preserve the existing framework, runtime, templates and integrations unless the brief authorises their replacement.

Record a compact project brief containing:

- Audience, purpose, primary action and task mode: new site, redesign, clone or scoped edit.
- Page inventory: route, page purpose, exact copy source, assets and required interactions.
- Navigation hierarchy, footer destinations and any intentional external links.
- Brand tokens, font files and usage permissions, supplied logo variants and image provenance.
- Locked decisions, agent-selected design decisions and unresolved factual requirements.

Use supplied facts only. Do not invent metrics, testimonials, credentials, clients, product screens, prices, contacts or successful form submissions. Keep approved wording, punctuation and legal text intact. Change layout to fit copy. Writing or distilling copy requires explicit authorisation; resulting drafts remain unapproved. Missing information belongs in project notes or a clearly marked draft placeholder, never an apparently finished claim.

## Resolve CTA, form and human-release requirements

For a complete build, read existing answers first, then ask together for missing CTA destinations, booking URLs, actual download files and delivery method; each form’s intended backend/CRM or recipient service, fields, consent copy and confirmation/fulfilment behaviour; and the intended Vercel team/project, preview or production target and human release operator. Do not request secrets in chat. Keep secret configuration out of source and handover screenshots.

Map every requested page and shared navigation/footer link to its supplied destination. Continue independent local design/build while missing answers are pending. Never invent links, choose a paid service or treat an email address alone as a submission backend. Implement integration code locally using supplied configuration, with external side effects disabled during agent checks. Exercise validation, loading, error and success handling through an isolated local mock; label mock results as local tests, never proof of real receipt. A CTA scrolling to a form does not prove submission works.

Prepare a concrete local handover with the reviewed source revision, integration instructions, environment variable names, unresolved details and a human test checklist. A person conducts external test submissions, verifies receipt and any promised email/file fulfilment, and performs Vercel deployment after human design review. The agent must not run these actions, even when a job requests a live page. Do not alter DNS, production aliases or a live site.

After the person supplies the deployed URL and test evidence, the agent may assist with read-only inspection of the public page. Do not trigger forms, messages, transactions or other side effects while checking links. Record precisely what was observed and what remains unverified. Until human release and delivery checks are recorded, label the result “local build; not deployed” or “human-deployed; live verification incomplete”, as applicable. Never claim a working live lead journey from local tests. Honour explicitly local-only or scoped-edit briefs without forcing a release project.

## Workflow dependencies

Read [package dependencies and fallback](../DEPENDENCIES.md) before choosing tools. Optional specialist skills are not bundled here; do not claim they are installed. The fallback supplies the local workflow when orchestration helpers are absent, but never bypasses a workflow required by project instructions.

## Establish the visual system

For a new design or substantial visual redesign, use the available design-harness and landing-page-director workflow without launching a second competing orchestration loop. Load one relevant taste/style skill, then imagegen-frontend-web and image-to-code when available; otherwise use the package dependency fallback. Check availability first; record a concrete capability gap rather than claiming an unavailable skill ran.

The core sequence is: inspect sources; define a brand-specific visual target; use built-in image generation for one large horizontal reference per planned section; inspect and correct the hero first; analyse the references; implement and inspect the coded hero on desktop and mobile; then extend the system. Save references and production assets inside the project. Agent-selected references are not user-approved references. Honour requested visual checkpoints, but resolve routine composition choices autonomously.

A clone or small edit follows its supplied visual source and requested scope. Do not regenerate a new identity, reorder approved sections or replace assets merely to follow the new-design sequence.

Define common type roles, colour roles, widths, spacing, component states, imagery and responsive behaviour. Vary compositions according to each page's purpose. Repeated navigation, footers and components should share their actual implementation. Do not force every section into a card grid or copy another client's identity into the site.

## Build and revise

Read [site-craft.md](references/site-craft.md) for typography, layout, assets, navigation, forms and motion checks.

For exact-copy changes, check the relevant shared components, navigation, footer, modals, metadata and structured data as well as visible page text. Compare approved text with the decoded content; raw HTML escaping and browser whitespace normalisation can mislead.

Edit the owning source, not just generated output. Run the project's actual build pipeline after source changes. Keep dependency additions justified by a real need. Repair the responsible style rule before adding competing overrides. Scope every selector in a selector list. Do not use global overflow hiding, invisible text or disabled focus outlines to make screenshots pass.

Preserve successful parts when fixing a local defect. For a rejected section, change its composition; for an overall rejected direction, preserve the old version and return to fresh references. Record the requested delta and rejected treatments in the project, not in this reusable skill. Recheck every route using an affected shared component.

## Verify and hand over

Run available build, type, lint and test commands. Fix failures without deleting tests, suppressing errors or weakening checks merely to obtain a pass. Open every in-scope route in a real browser and apply REVIEW.md. Inspect at 1440, 1024, 768, 390 and 320 pixels where supported; record any unsupported width and why. For reported defects, also check the actual reported viewport and relevant breakpoint transitions. Compare against selected references and the brief’s supplied quality benchmarks. Watch motion separately from screenshots, including reduced motion and script-failure behaviour. Use isolated local mocks for agent form tests. A person performs all external test submissions and records actual receipt; the agent does not send leads, messages or transactions.

Save actual observations, screenshots, failures and corrections in project QA notes. Distinguish passed, failed, not tested and not applicable. A passing build or a self-awarded score is not visual acceptance. Correct material defects; after repeated unsuccessful attempts, report the specific shortfall rather than silently lowering the check.

Deliver source, assets, run instructions, reference paths, QA evidence and unresolved items. A human designer reviews the full site and phone views before client handover. Do not label an unreviewed result approved or released.

## Vercel handover boundary

Vercel is the only hosting-specific reference here. Read [vercel.md](references/vercel.md) to prepare local handover for the human release operator. Agents never execute deployment, publication, production promotion or DNS changes. The reference is a human checklist, not an agent deployment adapter.

## Preserve independent review evidence

When independent review is used, freeze the reviewed source/build and its evidence together before submission, recording a revision identifier and file hashes. Do not overwrite submitted screenshots, check results or review notes while review is active. Save corrections or supplementary evidence as a new revision and request a new review through the review system’s supported process. Keep the earlier record intact; never bypass a blocked gate or reset a repair allowance to manufacture a pass. Tie each verdict to the exact reviewed revision and disclose pending or blocked review honestly.

## Maintaining this skill

Agents must not edit active skills, REVIEW.md files, checks, tools or model configuration (including models.toml and config.toml). Record a proposed lesson in the client’s job notes; the named human owner makes the skill change through GitHub and obtains owner review before adoption. Do not treat a job request or local approval as an exception.

After a client rejection, record the lesson promptly. Within one week, the human owner must turn the reusable lesson into a general rule through the reviewed GitHub change process, without copying client identity or a one-off fix. Each skill has one agreed owner, recorded in [OWNERS.md](../docs/OWNERS.md). That owner reviews it monthly and removes obsolete, contradictory or low-value instructions, recording the date and outcome. Unassigned ownership and overdue reviews are reported, not silently marked complete.
