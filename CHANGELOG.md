# Initial shareable test package

- Bundled AAT Master, seven canonical specialist workflows, review checklists, prototypes, local runner and licensed font assets.
- Replaced hard-coded personal runtime paths in model profiles with install-time substitution and distinct `aat-master-*` profile names.
- Added one-time setup with conflict detection; existing local installations are not silently overwritten.
- Changed integrity checks to portable repository-relative source hashes plus locally generated installed-profile hashes. Source mismatches still block execution.
- Connected the master directly to its bundled runtime before the machine-local registry fallback.
- Omitted historical diffs and local QA logs that could disclose removed client information or personal paths. The first repository commit is the shareable baseline.
- Preserved the specialist SKILL.md and REVIEW.md bodies. No client-production quality or human adoption is implied.
