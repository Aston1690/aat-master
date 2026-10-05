# Package dependencies and fallback

This package contains seven skills and their local supporting files. It does not install tools, authenticate services, or include `design-harness`, `imagegen-frontend-web`, `image-to-code` or a taste/style skill. Read this guide for website and landing-page production. When sharing a single skill separately, include this guide and any linked package references.

## Required capabilities

Use the existing project’s runtime/build tools, filesystem access, an actual browser for rendered inspection, and built-in image generation for a new image-first visual direction. A human operator needs Vercel tooling and access for release. Agent form tests use isolated local mocks; a person verifies a configured backend through external test submissions. Never claim any missing capability was used.

## Optional specialists

- `design-harness`: saved context, bounded implementation/review orchestration and review records.
- `imagegen-frontend-web`: direction for section-specific reference generation.
- `image-to-code`: detailed reference analysis and translation into code.
- One suitable taste/style skill: visual direction within the client’s brand.

Use installed specialists when appropriate. Do not download or install an unknown replacement automatically. If project instructions mandate a specialist, its absence is a concrete workflow blocker; finish independent preparation and report it rather than bypassing it.

## Local fallback when specialists are optional and unavailable

1. Save a project brief with exact copy sources, assets, requested deliverables, brand constraints, CTA/form destinations and delivery target. Select the visual thesis directly from the client’s brand and supplied references when no style skill is available.
2. Use built-in image generation to create one readable horizontal reference for each planned section in a new design. Inspect and correct the hero first; keep subsequent references consistent. For a clone or approved-template adaptation, retain its supplied visual target. If required image generation is unavailable, do not pretend the reference step happened; report the gap and complete independent preparation.
3. Record each selected reference’s typography, spacing, colours, imagery, hierarchy and responsive intent. Implement and inspect the hero at desktop/mobile sizes before extending the page/site.
4. Use the existing build tools and real browser to apply the skill’s REVIEW.md across its specified routes and widths. Keep source revisions, actual evidence and a defect list in the project. After two unsuccessful corrections for the same issue, reassess and disclose the remaining problem rather than weakening checks.
5. Record agent QA as agent QA. If an independent reviewer is unavailable, disclose that independent review did not occur; never imply the fallback reproduced it. Follow any mandatory project review gate.
6. Prepare integration code locally, test through isolated mocks and hand over the human Vercel release checklist. A person performs deployment and external form tests; an agent may inspect the supplied live URL read-only. Record missing inputs and pending human actions explicitly.

The website deployment reference is [website/references/vercel.md](website/references/vercel.md); the landing-page skill links to it. These fallbacks do not waive owner instructions, release approval or actual inspection.

All tools and optional skills must respect [GOVERNANCE.md](GOVERNANCE.md). If an adapter contradicts these boundaries, raise the conflict; do not silently override either instruction or install an unreviewed workaround.
