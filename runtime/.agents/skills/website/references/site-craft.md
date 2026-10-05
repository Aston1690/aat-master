# Site craft

Use only the sections relevant to the task. These rules preserve a shared design system without imposing a particular client's appearance.

## Typography and layout

- Check loaded font files, computed font family and weight, and child spans. A declaration alone does not prove the font rendered.
- Size headings for their actual copy, line length and viewport. For ordinary commercial pages, 56–78 px desktop hero type, 40–48 px mobile hero type and 16–20 px body text are starting ranges, not universal limits or permission to change copy.
- Inspect every display heading, not just the hero. Correct wrapping, column widths and spacing together. Do not remove punctuation or words to make a line fit.
- Align repeated cards through shared grid rows and content structure. Keep badges from displacing unrelated content. Reserve clear space around numbers, icons, dividers and labels.
- Diagnose overflow at the offending component. Preserve ordinary page scrolling; a modal's temporary scroll lock must restore on close, route change and error.

## Assets

Use verified supplied assets or permitted official sources, recording provenance in the project. An official logo source establishes the asset identity, not a client relationship or endorsement. A downloadable image or font is not evidence of production usage rights. Keep trial-only assets out of release output. Use approved logo variants proportionally; do not redraw, recolour or approximate marks to fit a layout.

Inspect source pixels and the final crop. Keep image proportions, useful resolution and meaningful alt text. Confirm the browser loads the intended local asset and that removed assets are no longer active in fallback declarations. Generated art is illustrative; it cannot stand in for actual product functionality, real customers or proof. Use one consistent icon family with accessible labels where needed.

## Navigation and components

Map destinations before building. Desktop and mobile navigation expose the same required pages. Test dropdown visibility, pointer movement into the submenu, keyboard focus, Escape, touch behaviour, route changes and focus return. Closed menus must not retain focusable hidden links; exposed state and aria-expanded must agree. Do not retain links to an old client's domain.

Preserve approved form fields and consent copy. Use labels and real validation/error states. Keep conditional fields’ visibility, disabled and required states consistent; hidden required fields must not block submission, and toggling a choice must not silently discard entered data. A prototype with no endpoint must say it is a prototype and must not claim a submission succeeded. Do not introduce a form service, chat widget or analytics provider by default. Agent tests use isolated local mocks with external side effects disabled. A person conducts external submissions and records actual receipt and fulfilment.

Only build a calculator from a supplied or verified formula. Show its assumptions and units; confirm displayed explanations agree with the actual computation. Flag discrepancies between supplied formulas and examples; do not change arithmetic to manufacture the expected answer. Test zero, boundary and invalid inputs. Accordions, tabs and selectors must retain semantic controls and keyboard operation.

## Motion and failure states

Give each effect a purpose, trigger, final state, mobile behaviour and reduced-motion alternative. Preserve the existing suitable motion system; do not add a library simply to satisfy a style label. Critical content is visible by default. Initialise enhancements only after required scripts are ready, and restore a readable state if initialisation fails. A JavaScript class alone is insufficient if an exception can leave content hidden indefinitely.

Clean up event listeners and animation instances on teardown or route changes. Keep layout transforms separate from animated transforms. Removing an effect includes its obsolete triggers and asset requests, not merely hiding the element.

Respect reduced-motion preferences. Never force animation back on with a global override. Keep focus indicators and skip links visible when used; do not remove them for cleaner captures. Avoid scroll hijacking and persistent decorative movement that obstructs reading.

For reveals, inspect a structural full-page view with reduced motion and separately watch normal-motion scrolling. Verify anchor entry, deep links, returning to a page and resizing. A reduced-motion screenshot proves neither normal timing nor trigger behaviour.

## Performance, metadata and capture

Optimise images, fonts and media for their actual use; reserve image dimensions to limit layout shifts. Verify video playback, poster and failure/reduced-motion fallbacks rather than relying on a ready-state value. Wait for fonts and images, and scroll through lazy-loaded sections before final captures.

Check page titles, descriptions and favicon against the approved site identity. Use a canonical URL only when the actual destination is verified; do not invent a production address. Check nested routes for asset-path failures.
