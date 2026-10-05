---
name: linkedin-static
description: Design image-led LinkedIn feed graphics and static campaign sets, with relevant imagery in every post, exact copy, verified brand assets, editable source and inspected exports.
metadata:
  status: "proposed; owner review pending"
  version: "1.1.1-email-review.1"
---

# LinkedIn Static

Create one complete standalone image per requested post or variant. Read [REVIEW.md](REVIEW.md) at the start and before handover. Do not add carousel numbering, swipe instructions or a PDF unless the brief requests them.

For an explicitly requested audit, prompt or specification only, deliver that scope; do not force full production. An explicit supplied-assets-only or no-generation instruction changes where imagery comes from; it does not remove the imagery requirement. Use suitable supplied assets in that case. If none are available and generation is prohibited or unavailable, report the missing imagery rather than silently delivering text-only work. Content approval does not verify factual accuracy; flag unsupported claims instead of silently endorsing or rewriting them.

## Team rules for every job

Read this SKILL.md and REVIEW.md in full before every job. Record the canonical skill path, version and source revision in the client’s job notes. If an instruction is wrong, unclear or conflicts with another rule, raise it with the skill owner; do not work around it or silently select another version. The team governance in [GOVERNANCE.md](../GOVERNANCE.md) applies to every deliverable and supporting tool.

Never invent numbers, quotes, logos, credentials or claims. Ask for missing facts or verified assets; unresolved items may appear only as labelled placeholders in a review draft. Keep client names, palettes, contacts, private files and machine-specific paths in the client’s folder, never in reusable skills or samples.

The agent prepares and checks local work only. A human designer must inspect every option at full size and feed/phone size and record approval separately from automated checks. Agents never deploy, publish, upload, host, post or send deliverables, including preview deployments, test emails and real form submissions. Approval to release does not delegate release to a bot. A person performs the release.


## Account for the requested output

Before production, inventory every requested deliverable and variation with its assigned copy/source, format, destination and expected filename or route. “One example per skill” means one selected client task, including that task’s requested options unless the user explicitly reduces scope. Do not invent a fixed number of variants. Reconcile the final handover against this inventory and disclose anything missing; a draft or omitted option is not a completed deliverable.

## Read and map the brief

Inspect the full creative brief/content calendar, approved on-image copy, reference posts and brand assets. Map every post to its image description and exact caption; distinguish accompanying social-post text from words required inside the image.

Record audience, objective, canvas, count, final format, copy source and asset provenance. Use PNG when no final image format is specified. Preserve specified dimensions. If unspecified, choose a suitable canvas such as 1080 × 1350 for a portrait composition and state the working choice; verify current platform requirements before claiming upload compatibility.

Preserve approved wording, punctuation, CTA, URL and legal text. Do not invent statistics, claims, dates, prices, testimonials, people or contact details. Writing or distilling copy requires explicit permission. Do not add decorative labels merely to fill space. A missing mandatory fact is unresolved, not an invitation to invent a plausible value.

## Choose a clear visual idea

Choose a communication structure suited to the content: hook poster, sourced statistic, attributed quotation, launch, event or compact educational idea. Use one main message per image. If approved content is too dense, flag it or adjust layout; do not shrink it into unreadable type or silently convert it into a different deliverable.

Define a specific visual thesis, palette, type roles, image treatment, composition and restraint. Use the client's real visual system. Avoid generic UI cards, meaningless charts, random stock scenes and decorative filler. Every static post must contain a prominent, relevant photograph or substantive illustration. Text-only posts are not an acceptable default. A logo, tiny icon, large numeral, gradient or decorative shape does not satisfy this requirement. Plan the image and copy together so the imagery communicates the post’s message while the words remain readable.

Study a supplied reference's actual geometry, hierarchy, crop and layer order. For a clone or approved-template edit, preserve the requested structure. For inspiration, adapt principles without importing another client's copy, identity or assets.

## Compose accurately

Build with the requested editable design tool or a deterministic renderer. Use suitable supplied or verified source imagery; when suitable imagery is missing, generate it with Codex’s built-in image model. Create and inspect the actual artwork before composing the final post; an image prompt or placeholder is not a finished image. Keep a per-post image plan recording the subject, role, source or generation prompt, saved asset path and crop. Keep production words, official logos, QR codes and product screens out of generated art. Place exact copy and verified assets separately. Generated scenes are illustrative, not evidence: do not present invented people, premises, events or products as the actual subjects of a client case study. Use verified photographs when a real identity or location is essential; otherwise choose clearly illustrative treatment. Save generated assets inside the client project.

Measure the actual text group using loaded fonts, line height and wrapping. Position support, proof and attribution relative to their associated headline rather than unrelated fixed coordinates. Reserve legible copy areas and protect faces, products and other focal subjects. A contrast treatment must belong to the design; do not patch a failed composition with an arbitrary box.

Use proportional crop/contain for supplied images. Verify the correct logo variant on the final background; do not crop a low-resolution wordmark out of another post or recolour it to hide a matte. Keep icon and diagram systems consistent. QR codes must come from a verified asset or be deterministically encoded from an approved destination and tested.

## Revise within scope

“Replace the image” changes the imagery, not the approved layout, copy, font or logo. “Brighter” changes treatment within the brand; it is not permission to impose a new palette. Preserve approved posts while working on another. Archive rejected work rather than deleting source or approved versions.

For local spacing/crop defects, repair locally. For rejected composition, rebuild the affected artboard from a new thesis; do not endlessly patch the same geometry. Record client feedback in the project. Never carry one campaign's colours, fonts or details into the shared skill.

## Export, inspect and deliver

Export exactly the requested number of images at the selected dimensions and format. Check file dimensions, actual format, colour mode, count and names. Use a contact sheet internally to compare the set, then inspect every final export at full size and realistic feed/phone size. Check long headlines, logo edges, URL/CTA legibility, contrast, subject crops, false generated details and stray source-brand remnants.

Check that every post includes its planned imagery, clearly visible at phone size and relevant to the message. Correct factual accuracy first, then legibility/collisions, hierarchy/crop, brand fidelity and polish. Re-export after corrections and inspect the final files. Correct pixel dimensions alone do not prove design quality.

Deliver final individual images, editable source and necessary assets with actual QA results. Include a contact sheet only when requested or useful as an additional review aid. A human designer inspects every final at full and feed/phone size before external handover. Agents never post, send or host assets; a person handles external release after review.

### Required three-pass review

1. Compare all requested options together at contact-sheet scale for concept quality, hierarchy, brand specificity and meaningful distinctness. A contact sheet is an internal review aid, not a replacement deliverable.
2. Inspect every final image at full size for exact copy, rendering defects, logo geometry, crop, contrast, collisions and asset quality. Do not limit this pass to spot checks.
3. Inspect every image at realistic feed/phone size in the destination context, including narrow crops and any relevant interface obstruction. Use a clearly identified local preview; a person handles any real platform upload. Do not apply profile-banner avatar geometry to feed images.

Record findings and corrections for each pass. Repeat affected passes after re-export. A human designer separately performs all three passes before external handover; automated or agent review is not that approval.

## Maintenance

Agents must not edit active skills, REVIEW.md files, checks, tools or model configuration (including models.toml and config.toml). Record a proposed lesson in the client’s job notes; the named human owner makes the skill change through GitHub and obtains owner review before adoption. Do not treat a job request or local approval as an exception.

After a client rejection, record the lesson promptly. Within one week, the human owner must turn the reusable lesson into a general rule through the reviewed GitHub change process, without copying client identity or a one-off fix. Each skill has one agreed owner, recorded in [OWNERS.md](../docs/OWNERS.md). That owner reviews it monthly and removes obsolete, contradictory or low-value instructions, recording the date and outcome. Unassigned ownership and overdue reviews are reported, not silently marked complete.


## Deliver accompanying captions

Include `captions.md` or the requested caption format with each approved caption reproduced exactly and mapped to its final post filename or carousel PDF/slide set and variant ID. Preserve supplied hashtags, links and intentional line breaks. Keep captions separate from on-image copy. If no caption is supplied, record “Not supplied” without inventing one; write captions only when authorised, marking unapproved drafts clearly. Verify every supplied caption is paired with the correct export before handover.
