# All seven deliverables: one entry point

From the repository, use `runtime/.venv/bin/python runtime/team.py`, or the master skill's wrapper. `status` lists all seven routes and verifies pinned runtime files. `codex --profile aat-master-astra` opens an Astra CLI session after installation. In T3, keep the main model Astra and ask it to use this runtime; a CLI profile does not silently change an already-open T3 thread.

1. Read the selected SKILL.md and REVIEW.md fully. Read the brief, approved copy, brand assets and references. Select destination/track/routes and list missing consequential inputs in one request. Do not invent client facts.
2. `new <deliverable> --case <absolute new client case path> --brief <local brief file> --options N`. For banners add `--destination personal|business`. Use explicit N from the brief; otherwise two for new work, one for clones/scoped edits. Never use Group with this skill version.
3. Complete case-notes.md and production.json. Every option has an exact copy_file relative to the case, a distinct thesis, expected_artifacts (exact relative output filenames) and the configured mandatory required_checks. Set copy_approved only from actual user/source evidence and record it. Resolve build blockers. User visual approval is required only when requested; routine art direction belongs to Astra.
4. Astra uses built-in image_gen for the images/references needed by the chosen skill and saves them inside the option. Inspect the hero/cover first, then extend the direction. Static posts and every carousel slide need real relevant imagery. A logo is supplied, never generated. If unavailable, stop the affected production; no simulated image-generation pass.
5. `preflight <case>` validates inputs and the complete output plan. `build <case>` starts one fresh Sol CLI process per option, up to two at once. Each has only its own working directory. For scoped audit/prompt requests do that scope directly; don't force this production runner.
6. Mechanical tools: `runtime/.venv/bin/python runtime/tools/design.py --help`. PNG/PDF exports, banner prototype/preview, full-page capture, emailcheck, pagecheck and inspect are available. The bundled licensed fonts may be copied into the client project; shared font-library mutation and source-import helpers are not enabled. Do not use its legacy new/review/status paths. Preserve an existing web stack. Web source goes in option-N/site; other editable layouts in source. Put native outputs in exports, full/phone screenshots in previews, and actual checks/results.json plus detailed evidence in checks. Required check IDs come from config.toml. Never hide failed or missing checks.
7. Astra inspects every option at full and feed/phone size, all PDF pages and every web route. For websites, required_checks must include evidence for all routes, not just a homepage screenshot. Newsletter production needs HTML, plain text and an honest inbox-test status; conceptual preview alone is not production readiness.
8. `review <case>` first checks expected outputs, counts and required evidence. It keeps a complete source snapshot under review/round-N. It renders every PDF page, includes native/context/feed images, batches all images (no truncation) into fresh Astra sessions, then starts a fresh final Astra rubric review per option. The final reviewer reads the source/copy/mechanical checks and all visual findings. Every rubric ID is required. Missing or malformed results stop without a pass. Code computes fail/incomplete/ready_for_human_review; human checks may keep a job incomplete until they happen. This is honest status, not approval.
9. `repair <case>` sends only failed options back to fresh Sol builders. Blockers need the designer/client, not fabricated repairs. Repeat checks/review; at most three repair rounds after the initial review. Reviews use a per-case lock and a shared review lock. Image generation in the main thread is completed before review; do not run image batches concurrently with review.
10. Read HANDOVER.md and the exact final review result. Human designer inspects every option and chooses; only a person publishes, deploys, uploads or sends. Agents do local form mocks only. Keep owner/team adoption pending until actually reviewed.

## Output map

- Banner: native banner, editable source, destination-specific desktop/mobile/phone prototype previews.
- Static: every post image, editable source, imagery provenance, captions map, full/feed review.
- Carousel: N ordered PNGs, one N-page PDF, editable source, creative bible, imagery and caption map.
- BIP: editable document/deck, one ordered PDF, every page inspected, disclosed print status.
- Newsletter: whole-issue desktop/phone previews; production HTML and plain text when asked; disclosed inbox-test status.
- Landing page: working single page, section references, source/assets, five-width and interaction/motion evidence.
- Website: same across every route, navigation/footer and shared components.

## Honest limits

This is a local Codex adaptation, not the Claude runtime with renamed models. Production quality is untested until real jobs are run. Structural/routing tests use neutral fixtures. The reviewer cannot prove a human approved the work. Linked external tools and optional specialist skills may need capabilities at job time; absence must be reported. No new API billing or provider is configured.
