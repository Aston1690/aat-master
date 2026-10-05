---
name: linkedin-carousel
description: Design image-led LinkedIn document carousels with relevant imagery on every slide, exact approved copy, ordered PNGs, one combined PDF and editable source.
metadata:
  status: "proposed; owner review pending"
  version: "1.1.1-email-review.1"
---

# LinkedIn Carousel

Build one story across a sequence of slides. Read [REVIEW.md](REVIEW.md) before starting and before handover. A standalone post or animated video card is a different deliverable.

For an explicitly requested audit, prompt or specification only, deliver that scope; do not force full production. An explicit supplied-assets-only or no-generation instruction changes where imagery comes from; it does not remove the imagery requirement. Use suitable supplied assets in that case. If none are available and generation is prohibited or unavailable, report the missing imagery rather than silently delivering text-only work. Content approval does not verify factual accuracy; flag unsupported claims instead of silently endorsing or rewriting them.

## Team rules for every job

Read this SKILL.md and REVIEW.md in full before every job. Record the canonical skill path, version and source revision in the client’s job notes. If an instruction is wrong, unclear or conflicts with another rule, raise it with the skill owner; do not work around it or silently select another version. The team governance in [GOVERNANCE.md](../GOVERNANCE.md) applies to every deliverable and supporting tool.

Never invent numbers, quotes, logos, credentials or claims. Ask for missing facts or verified assets; unresolved items may appear only as labelled placeholders in a review draft. Keep client names, palettes, contacts, private files and machine-specific paths in the client’s folder, never in reusable skills or samples.

The agent prepares and checks local work only. A human designer must inspect every option at full size and feed/phone size and record approval separately from automated checks. Agents never deploy, publish, upload, host, post or send deliverables, including preview deployments, test emails and real form submissions. Approval to release does not delegate release to a bot. A person performs the release.


## Account for the requested output

Before production, inventory every requested deliverable and variation with its assigned copy/source, format, destination and expected filename or route. “One example per skill” means one selected client task, including that task’s requested options unless the user explicitly reduces scope. Do not invent a fixed number of variants. Reconcile the final handover against this inventory and disclose anything missing; a draft or omitted option is not a completed deliverable.

## Lock content and delivery

Inspect the brief, source material, brand kit, approved slide copy, assets and reference work. Record objective, audience, canvas, slide count, order and primary action. Preserve the requested count. When no count is given, propose a content-led count in the plan; neither seven nor eight is compulsory. Do not add filler or cut approved copy to reach a preset count.

Use the brief's canvas. A 1080 × 1350 or 1080 × 1080 canvas is a useful working choice when unspecified, not a claim about current platform requirements. Verify official destination limits before describing a PDF as upload-ready.

Approved copy is locked. A long caption is not automatically permission to summarise: distillation requires authorisation and resulting slide copy must be accepted before being treated as final. Do not add hook words, CTA labels, proof, quotations, testimonials or “SWIPE” text that the brief did not supply or authorise. Pagination is a layout choice; keep it consistent and accurate. Use visibly labelled placeholders for missing content in a review draft; do not fabricate client facts even to make a concept look convincing.

Map every slide to exact copy, evidence, role, image subject, source or generation prompt, saved asset path, crop and layout. Every slide must have a prominent, relevant photograph or substantive illustration, including cover, statistic, quotation and closing slides. Text-only slides are not an acceptable default. Logos, tiny icons, large numerals, gradients and decorative shapes do not count as the required imagery. Missing facts remain clearly unresolved. Use verified logo files. Source imagery from suitable supplied or verified assets, or generate illustrative artwork with the built-in image model. Generated art is not factual evidence: do not depict invented people, premises or events as the actual subjects of a client case study, or present generated product screens as real. Use verified photography when a specific identity or location is essential; otherwise choose clearly illustrative treatment.

## Plan story and visual rhythm

Adapt the narrative to the supplied material: hook, context, useful explanation, evidence or example, synthesis and final action. Each slide should advance the same argument. Do not invent a proof slide when evidence is absent.

Lock one palette, type hierarchy, grid, margins, image treatment and pagination/branding system. Keep one visual identity while varying scale, density and arrangement. Inspect adjacent slides for repetitive geometry or abrupt drift; do not impose arbitrary layout quotas on a short or template-preserving deck.

Reserve copy, logo and pagination areas before generating or positioning artwork. The quiet field must fit the actual words. Plan subject crops and contrast; do not cover a failed image with an improvised rescue panel. An intentional panel system remains valid when it is part of the chosen direction.

### Lock the creative bible

Before generating, save one creative bible in the client’s project: palette roles; typography and hierarchy; grid, margins and line/border language; photography/illustration treatment; texture/material vocabulary; recurring motifs where useful; branding and pagination zones; verified asset sources; direct-on-background or deliberately planned panel treatment; composition rhythm; and any seamless-transition logic. Apply it across every slide, including the cover and closing slide. Variation belongs in layout, crop and pacing, not random changes of fonts, palette or rendering style. A planned panel system is valid; a rescue box covering a failed image is not a substitute for composition.

## Produce slide by slide

Use the requested editable tool or deterministic renderer. Every slide is image-led. Use suitable supplied imagery or generate separate slide artwork with Codex’s built-in image model, inspecting the cover/master artwork first and using references to maintain consistency. Plan each image around that slide’s message; do not repeat one unrelated image across the deck just to satisfy the requirement. Do not generate the entire deck as one contact sheet. Inspect and save actual artwork before final composition; prompts and placeholders do not fulfil the imagery requirement.

Keep production text, logos and numbers separate from generated art. Typeset exact copy and place official assets deterministically. Measure actual text bounds with the chosen fonts and line breaks. Recompose or change authorised pagination when content will not fit; do not silently shorten it.

For a seamless treatment, match the exit and entry of a deliberate visual element precisely across adjacent slides. Keep critical words, faces and logos away from the split. Save all editable source, artwork and references inside the project.

## Export and verify

Deliver N individual ordered PNGs and exactly one combined N-page PDF for N slides. Use zero-padded filenames and numeric order. No separate per-slide PDFs and no contact sheet in place of the actual slides. Keep all pages at the selected canvas proportions and check for duplicates or omissions.

Prefer live text in the PDF when the composition tool supports it; verify visual agreement with the PNGs. If an image-only PDF is required, disclose flattened text and keep editable source. Set metadata from the supplied document title and author; do not leak internal calendar names or another client's identity.

Inspect every PNG at full size and roughly 360 px display width. Reopen the PDF, verify page count, dimensions and order, render every page, and compare with the final slide exports. Verify that all N slides contain their planned imagery, clearly visible at phone size and meaningfully related to their message. Review story continuity, readability, exact words, factual sources, logo geometry, safe areas and consistent identity. Contact-sheet review alone is insufficient.

## Handover and maintenance

Deliver all slides, the combined PDF, source and necessary assets with actual QA results and unresolved issues. A human designer reads every slide at full and phone/feed size before external handover. Agents never publish or host assets; a person handles external release after review.

Agents must not edit active skills, REVIEW.md files, checks, tools or model configuration (including models.toml and config.toml). Record a proposed lesson in the client’s job notes; the named human owner makes the skill change through GitHub and obtains owner review before adoption. Do not treat a job request or local approval as an exception.

After a client rejection, record the lesson promptly. Within one week, the human owner must turn the reusable lesson into a general rule through the reviewed GitHub change process, without copying client identity or a one-off fix. Each skill has one agreed owner, recorded in [OWNERS.md](../docs/OWNERS.md). That owner reviews it monthly and removes obsolete, contradictory or low-value instructions, recording the date and outcome. Unassigned ownership and overdue reviews are reported, not silently marked complete.


## Deliver accompanying captions

Include `captions.md` or the requested caption format with each approved caption reproduced exactly and mapped to its final post filename or carousel PDF/slide set and variant ID. Preserve supplied hashtags, links and intentional line breaks. Keep captions separate from on-image copy. If no caption is supplied, record “Not supplied” without inventing one; write captions only when authorised, marking unapproved drafts clearly. Verify every supplied caption is paired with the correct export before handover.
