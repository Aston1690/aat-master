# Validation — 2026-10-05

This is a shareable local-test package, not an approved production standard. Tests below verify mechanics, not design quality.

Executed for this package:
- Installer completed in isolated Codex/config directories on macOS, using an existing Chromium rather than downloading a browser.
- All 23 runtime regression tests passed, including all-seven routing with explicitly stubbed model responses.
- The master resolves its bundled runtime and status reports seven routes with no problems.
- Portable integrity checks accepted intact files and rejected both modified sources and modified installed profiles.
- All eight skills passed structural validation; all relative Markdown references resolve. Seven specialist SKILL.md/REVIEW.md pairs match the local baseline byte-for-byte.
- Shared source passed personal-path/client-name/credential-pattern checks. Font licence attributions remain intact.
- A headless Chromium renderer launched and read a neutral HTML fixture. This is renderer availability, not a visual client-job test.

The initial Python environment test exposed copied-interpreter library resolution on this Mac; the installer now uses symlinked interpreters and setup succeeds. No existing user installation was overwritten. See GitHub history for subsequent changes.

The original local runtime also passed real Astra/Sol connection probes and a deliberately failing Astra visual-review fixture. These were previous local checks, not fresh end-to-end client jobs performed for this repository. No claim of model availability on another account follows from them.

Limitations: no new client design, image-generation call, human design approval, deployment or external form submission was performed for this release. macOS is the tested platform; Linux is not yet validated and native Windows is unsupported. T3 may need a full restart to refresh the skill picker. Model account access and host image/browser capabilities need checking at job time. Human owners and adoption remain pending.
