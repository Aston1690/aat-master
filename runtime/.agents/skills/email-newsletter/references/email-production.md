# Production email checks

Read for sendable HTML, not merely a browser-rendered concept. Confirm the supported clients and sending platform from the brief; implementation and verification must match that target.

- Use a fluid container with a conventional desktop content width around 600 px unless the supplied template specifies otherwise. Use presentation tables for critical structure and inline essential CSS. Preserve semantic reading order and label layout tables as presentation.
- Provide reliable fallbacks for fonts, colours and images. Do not rely on JavaScript, forms, video backgrounds, CSS Grid or advanced positioning for essential content. Verify any optional enhancement against current target-client support.
- Build CTA buttons with actual links and a tested fallback structure. Preserve approved labels and destination URLs. Test long labels, narrow screens and images-off display.
- Use absolute HTTPS image URLs for deployed production assets, with explicit sizing and useful alt text. Local assets may accompany a handover draft, but cannot be described as ready for sending until the sender has valid hosted paths. Agents never publish assets; a person supplies or publishes the production URLs.
- Supply the exact sender identification, footer copy, preference/unsubscribe mechanism and merge tags required by the approved brief and sending configuration. Do not invent addresses or legal wording. Validate tag syntax against the configured platform without changing the shared skill.
- Keep subject and preheader from approved copy. Ensure hidden preheader techniques do not expose filler or replace meaningful content. Produce plain text in the same logical reading order, including meaningful links and the applicable footer.
- Inspect mobile stacking, touch targets, long URLs, image scaling and readable footer text. Check dark mode and image blocking in actual test environments when available.
- Keep Gmail, Outlook variants and Apple Mail results distinct. Record exact environments tested; success in one does not prove another. No browser screenshot establishes delivery, spam placement, consent status or inbox rendering.

A person performs any test send or upload to an external testing service, after checking the exact test recipients and payload. Agents do not send or upload. Never use a production list to validate a design.
