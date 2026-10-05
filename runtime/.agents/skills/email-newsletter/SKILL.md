---
name: email-newsletter
description: Design branded newsletter concepts or build production HTML email from approved content, with complete exports, responsive inspection and explicit email-client testing status.
metadata:
  status: "proposed; owner review pending"
  version: "1.0.2-email-review.1"
---

# Email Newsletter

Produce the designed artifact. Read [REVIEW.md](REVIEW.md) before starting and before handover. Separate a visual concept from production email; an attractive browser page is not evidence of inbox compatibility.

For an explicitly requested audit, prompt or specification only, deliver that scope; do not force full production. An explicit supplied-assets-only or no-generation instruction overrides generation defaults. Content approval does not verify factual accuracy; flag unsupported claims instead of silently endorsing or rewriting them.

## Team rules for every job

Read this SKILL.md and REVIEW.md in full before every job. Record the canonical skill path, version and source revision in the client’s job notes. If an instruction is wrong, unclear or conflicts with another rule, raise it with the skill owner; do not work around it or silently select another version. The team governance in [GOVERNANCE.md](../GOVERNANCE.md) applies to every deliverable and supporting tool.

Never invent numbers, quotes, logos, credentials or claims. Ask for missing facts or verified assets; unresolved items may appear only as labelled placeholders in a review draft. Keep client names, palettes, contacts, private files and machine-specific paths in the client’s folder, never in reusable skills or samples.

The agent prepares and checks local work only. A human designer must inspect every option at full size and feed/phone size and record approval separately from automated checks. Agents never deploy, publish, upload, host, post or send deliverables, including preview deployments, test emails and real form submissions. Approval to release does not delegate release to a bot. A person performs the release.


## Account for the requested output

Before production, inventory every requested deliverable and variation with its assigned copy/source, format, destination and expected filename or route. “One example per skill” means one selected client task, including that task’s requested options unless the user explicitly reduces scope. Do not invent a fixed number of variants. Reconcile the final handover against this inventory and disclose anything missing; a draft or omitted option is not a completed deliverable.

## Resolve the delivery

Read the approved copy, brand assets, issue context, audience, links and requested output. Choose the requested track:

- **Visual concept:** editable design or browser composition plus full-length PNG; PDF if requested or useful for review.
- **Production email:** responsive email HTML, a matching plain-text version, assets and testing notes. Use the supplied sending-platform requirements.
- **Both:** retain distinct concept and production files, translating the chosen visual direction into email-compatible structure.

Preserve the exact subject, preheader, issue/date, body, link labels, CTA, sender and footer copy. Flag an overlong subject or dense paragraph; do not rewrite it without permission. Do not invent company news, releases, dates, people, achievements or proof. Missing facts use visibly labelled placeholders in a review concept; never invent sample news, metrics or endorsements. Keep missing facts clearly unresolved, not plausible-looking.

## Design the issue

Record a concise visual direction: masthead, hierarchy, type, palette, image treatment, section rhythm and main action. Follow the client's actual brand and supplied template. Choose sections based on supplied content, not a compulsory company-update structure.

Use editorial pacing: a clear lead, purposeful supporting modules and a connected closing action/footer. Vary density without changing identity. Avoid a long chain of equal cards, oversized empty heroes, fake dashboards and stock-photo filler. Preserve copy when adjusting layout.

A concept width around 640 px is a useful starting point, not a platform requirement. Check a roughly 390 px mobile view as well. Keep body and footer text readable at actual display size; avoid image-only text. Use approved images, verified logos and descriptive alt text. Generated artwork, when needed, uses the built-in image tool and receives exact text/branding separately.

## Build the requested format

For concepts, use the requested editable tool or a deterministic HTML/CSS composition. Wait for fonts and images before capture. Export the whole issue with backgrounds included and inspect the entire image. If producing a PDF, inspect every page break and page after export.

For production email, read [email-production.md](references/email-production.md). Confirm the actual merge tags, asset destinations, sender details and unsubscribe mechanism from the sending configuration or supplied brief. Do not guess these values or host assets; a person supplies or publishes the production URLs. Mark unresolved production requirements as blocking release.

Use current official sending-platform documentation and current client-support evidence when implementing a feature whose compatibility is uncertain. Keep findings in the project, not by updating the skill mid-job.

## Check and deliver

Inspect full-length desktop and mobile output, including CTA and footer. Check exact copy, consistent counts, clipping, long links, images, hierarchy, contrast and reading order. Verify production HTML and plain text agree. Use available local rendering tools; a person performs test sends or uploads to external inbox-testing services. Record only evidenced client, version or test-service results, date and observation. Browser preview is a separate check.

Deliver the requested files and assets with explicit status: concept, production HTML awaiting client tests, or production HTML tested in the listed environments. Do not claim universal compatibility or deliverability. A human designer reviews the complete issue and mobile view before external handover. Agents never send test emails or campaigns, upload assets or publish the issue; a person performs those actions after review.

## Maintenance

Agents must not edit active skills, REVIEW.md files, checks, tools or model configuration (including models.toml and config.toml). Record a proposed lesson in the client’s job notes; the named human owner makes the skill change through GitHub and obtains owner review before adoption. Do not treat a job request or local approval as an exception.

After a client rejection, record the lesson promptly. Within one week, the human owner must turn the reusable lesson into a general rule through the reviewed GitHub change process, without copying client identity or a one-off fix. Each skill has one agreed owner, recorded in [OWNERS.md](../docs/OWNERS.md). That owner reviews it monthly and removes obsolete, contradictory or low-value instructions, recording the date and outcome. Unassigned ownership and overdue reviews are reported, not silently marked complete.
