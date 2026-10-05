---
name: landing-page-director
description: Design, build, redesign and visually review single marketing landing pages and campaign pages using image-first direction, approved copy and responsive browser checks.
metadata:
  status: "proposed; owner review pending"
  version: "1.0.3-email-review.1"
---

# Landing Page Director

Own art direction and completion for one marketing page. Read [REVIEW.md](REVIEW.md) at the start and before handover. Use the website workflow for multi-page architecture; avoid running two competing direction processes. Keep mechanical fixes proportional to their scope.

For an explicitly requested audit, prompt or specification only, deliver that scope; do not force full production. An explicit supplied-assets-only or no-generation instruction overrides generation defaults. Content approval does not verify factual accuracy; flag unsupported claims instead of silently endorsing or rewriting them.

## Team rules for every job

Read this SKILL.md and REVIEW.md in full before every job. Record the canonical skill path, version and source revision in the client’s job notes. If an instruction is wrong, unclear or conflicts with another rule, raise it with the skill owner; do not work around it or silently select another version. The team governance in [GOVERNANCE.md](../GOVERNANCE.md) applies to every deliverable and supporting tool.

Never invent numbers, quotes, logos, credentials or claims. Ask for missing facts or verified assets; unresolved items may appear only as labelled placeholders in a review draft. Keep client names, palettes, contacts, private files and machine-specific paths in the client’s folder, never in reusable skills or samples.

The agent prepares and checks local work only. A human designer must inspect every option at full size and feed/phone size and record approval separately from automated checks. Agents never deploy, publish, upload, host, post or send deliverables, including preview deployments, test emails and real form submissions. Approval to release does not delegate release to a bot. A person performs the release.


## Account for the requested output

Before production, inventory every requested deliverable and variation with its assigned copy/source, format, destination and expected filename or route. “One example per skill” means one selected client task, including that task’s requested options unless the user explicitly reduces scope. Do not invent a fixed number of variants. Reconcile the final handover against this inventory and disclose anything missing; a draft or omitted option is not a completed deliverable.

## Read and lock the brief

Inspect supplied copy, current page, references, brand kit, logos, fonts, imagery and repository instructions. Identify audience, offer, primary action, content status, required section order, source assets and existing stack. Record locked facts separately from design decisions and unresolved information in the project brief.

Preserve approved words, punctuation, assets, framework and templates. Do not invent proof, clients, metrics, credentials, contacts, product screens or service promises. Writing or summarising copy requires explicit authorisation; drafts remain unapproved. Missing factual content stays in project notes or clearly marked draft placeholders. A concept uses clearly labelled placeholders for absent facts; it must not invent business claims or proof.

Use information already available. Resolve routine art direction autonomously. Ask only for a consequential missing fact or requested checkpoint; a lack of visual preferences is not a reason to run a compulsory interview.

## Resolve CTA, form and human-release requirements

For a complete build, read existing answers first, then ask together for missing CTA destinations, booking URLs, actual download files and delivery method; each form’s intended backend/CRM or recipient service, fields, consent copy and confirmation/fulfilment behaviour; and the intended Vercel team/project, preview or production target and human release operator. Do not request secrets in chat. Keep secret configuration out of source and handover screenshots.

Map every requested page and shared navigation/footer link to its supplied destination. Continue independent local design/build while missing answers are pending. Never invent links, choose a paid service or treat an email address alone as a submission backend. Implement integration code locally using supplied configuration, with external side effects disabled during agent checks. Exercise validation, loading, error and success handling through an isolated local mock; label mock results as local tests, never proof of real receipt. A CTA scrolling to a form does not prove submission works.

Prepare a concrete local handover with the reviewed source revision, integration instructions, environment variable names, unresolved details and a human test checklist. A person conducts external test submissions, verifies receipt and any promised email/file fulfilment, and performs Vercel deployment after human design review. The agent must not run these actions, even when a job requests a live page. Do not alter DNS, production aliases or a live site.

After the person supplies the deployed URL and test evidence, the agent may assist with read-only inspection of the public page. Do not trigger forms, messages, transactions or other side effects while checking links. Record precisely what was observed and what remains unverified. Until human release and delivery checks are recorded, label the result “local build; not deployed” or “human-deployed; live verification incomplete”, as applicable. Never claim a working live lead journey from local tests. Honour explicitly local-only or scoped-edit briefs without forcing a release project.

## Workflow dependencies

Read [package dependencies and fallback](../DEPENDENCIES.md) before choosing tools. Optional specialist skills are not bundled here; do not claim they are installed. The fallback supplies the local workflow when orchestration helpers are absent, but never bypasses a workflow required by project instructions.

## Direct before implementing

Use design-harness for saved context and the bounded implementation/review loop when available. This skill owns art direction; the harness owns execution records. A stage-specific invocation performs its assigned stage without starting another harness. Confirm tool and skill availability; report a missing capability honestly.

For new designs and substantial visual redesigns:

1. Choose one relevant taste/style skill when available; otherwise define the visual direction from the supplied brand and references as described in the dependency fallback. Define a concrete visual thesis: what the visitor should understand, the main image or compositional idea, palette, type hierarchy, density, CTA emphasis and treatments to avoid.
2. Load imagegen-frontend-web when available. Use built-in image generation to create one large horizontal reference per planned section. Inspect and correct the hero before extending the direction. Save the images in the project.
3. Keep palette, typography character, imagery and component language coherent while varying section composition. Generate fresh detail references when needed, not tiny crops from a compressed whole-page board.
4. Select the direction after critical review. Record agent selection distinctly from user approval. Pause for visual approval only when the user requested that checkpoint.
5. Load image-to-code when available. Analyse each selected reference for type, spacing, colour, imagery, components, reading order and responsive intent. Generated words and logos are not production assets: implement exact approved copy and verified logo files.

A clone, approved-template adaptation or narrow edit uses the supplied visual target. Preserve its requested layout and order; do not use the new-design process to replace it. If required image generation or inspection is unavailable, report the gap and complete independent preparation without claiming the image-first sequence ran.

## Build with deliberate hierarchy

Inspect existing components, package scripts and repository changes before editing. Preserve the existing stack. Implement the header and hero first and inspect at 1440 and 390 pixels before completing the page.

Keep one dominant message and primary action in the first viewport. Size the logo optically; avoid accidental white boxes or distorted marks. Design the final conversion section with clear emphasis. Use only sections supported by content, not a compulsory sequence of hero, proof strip, three cards and testimonials.

Use readable type and varied rhythm. Typical commercial starting points are 56–78 px desktop hero type, 40–48 px mobile hero type and 16–20 px body text; adapt to the brand and verify actual rendered size. Do not turn these ranges into fixed limits. Fix awkward wraps through layout, never silent copy edits. Keep numbers, rules, icons and labels clear of text.

Use meaningful imagery and a consistent icon family. Keep assets in the project and record provenance. Do not introduce fake dashboards, stock proof or generic gradient decorations. Add dependencies only for requirements the current stack cannot meet cleanly.

Navigation, CTA destinations, forms and controls must behave as represented. Unconfigured forms are clearly identified prototypes with no false success. Use isolated local mocks for agent form tests; a person performs external submissions and verifies receipt.

## Motion and responsive behaviour

Choose purposeful motion that suits the brand and existing implementation. Record trigger, sequence, final state, mobile adaptation and reduced-motion result. Do not mandate a particular animation library or add ceremonial effects. Preserve a requested static design or existing motion system.

Keep critical content readable if JavaScript fails, loads slowly or throws during setup. Honour reduced motion, retain keyboard focus indicators and avoid scroll hijacking. Watch normal animation and test reduced motion separately; still images do not prove movement works.

Define reading order, column collapse, type wrapping, image crops, navigation and CTA treatment per breakpoint. Do not shrink a desktop composition uniformly or hide overflow to conceal broken components.

## Review, revise and deliver

Run the project's available build, type, lint and tests. Fix the cause of failures; do not suppress errors or weaken checks to get a pass. Open the real page at 1440, 1024, 768, 390 and 320 pixels where supported. For reported defects, also inspect the reported viewport and relevant breakpoint transitions. Inspect the full page, not just the hero; compare with selected references and supplied quality benchmarks and complete REVIEW.md.

Check exact copy in shared components and structured data as well as visible content. Verify loaded fonts and assets before capture; optimise media, reserve image dimensions, and test playback and failure fallbacks. Confirm metadata and destination URLs against the real brief. Closed menus must not retain focusable hidden links; conditional form fields must keep visibility and validation consistent.

Correct local defects locally. Recompose a rejected section; return to new references when the overall direction is rejected. Preserve prior versions and record rejected treatments in project notes. After two unsuccessful correction rounds for the same issue, reassess the cause; disclose any remaining gap instead of claiming quality from a score.

Deliver working source, assets, references, run instructions and evidence of actual checks. State unresolved content or testing gaps. A human designer reviews full-page and phone views before client handover. Prepare the human-release handover described above. Use [the Website package’s human Vercel checklist](../website/references/vercel.md); the agent never executes deployment. Report local QA, human design approval, human release and live verification as separate states.

## Preserve independent review evidence

When independent review is used, freeze the reviewed source/build and its evidence together before submission, recording a revision identifier and file hashes. Do not overwrite submitted screenshots, check results or review notes while review is active. Save corrections or supplementary evidence as a new revision and request a new review through the review system’s supported process. Keep the earlier record intact; never bypass a blocked gate or reset a repair allowance to manufacture a pass. Tie each verdict to the exact reviewed revision and disclose pending or blocked review honestly.

## Maintenance

Agents must not edit active skills, REVIEW.md files, checks, tools or model configuration (including models.toml and config.toml). Record a proposed lesson in the client’s job notes; the named human owner makes the skill change through GitHub and obtains owner review before adoption. Do not treat a job request or local approval as an exception.

After a client rejection, record the lesson promptly. Within one week, the human owner must turn the reusable lesson into a general rule through the reviewed GitHub change process, without copying client identity or a one-off fix. Each skill has one agreed owner, recorded in [OWNERS.md](../docs/OWNERS.md). That owner reviews it monthly and removes obsolete, contradictory or low-value instructions, recording the date and outcome. Unassigned ownership and overdue reviews are reported, not silently marked complete.
