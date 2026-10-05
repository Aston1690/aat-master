# AAT Master

One skill entry point for seven creative workflows: **Astra orchestrates → Sol builds → a fresh Astra session reviews → a human approves and releases.**

**Status: team testing; owner review/adoption pending.** Configuration and protocol tests do not establish design quality. Validate real client tasks one at a time. No automatic deployment, upload, email send or external form submission is part of client production.

## Included workflows

| Input | Specialist |
|---|---|
| LinkedIn personal/business banner | `linkedin-banner`, with separate destination prototypes |
| Static post | `linkedin-static` |
| Carousel | `linkedin-carousel` |
| Business Information Pack | `bip` |
| Email newsletter | `email-newsletter` |
| One campaign/marketing page | `landing-page-director` |
| Multi-page marketing website | `website` |

The master detects scope from the brief, asks about ambiguous inputs, reads the matching SKILL.md and REVIEW.md, and uses the real runner. Mixed briefs are inventoried and processed one task at a time. Requested variations belong to that task; there is no fixed three-option rule.

## Install once

Requirements: Windows or macOS, Python 3.11+, Node.js/npm, and an authenticated Codex CLI with access to `gpt-6-astra` and `gpt-6-sol`. The main T3/Codex session needs built-in image generation and browser access for stages that require them. Claude is not required. WSL and administrator access are not required by this installer. Linux is not yet validated; compatibility with every IDE is not guaranteed.

Windows PowerShell (after installing Python 3.11+, Node.js and Codex):

```powershell
git clone https://github.com/Aston1690/aat-master.git
cd aat-master
py -3 install.py
```

If already cloned, run `git pull --ff-only` in that folder, then `py -3 install.py`. A previous attempt that stopped with the Windows restriction did not install the skill; no WSL setup is needed.

macOS:

```sh
git clone https://github.com/Aston1690/aat-master.git
cd aat-master
python3.11 install.py
```

The installer creates a local Python environment, installs pinned Python/Node dependencies and Chromium, installs three named `aat-master-*` Codex profiles, installs the master skill into the selected Codex home (a managed copy on Windows; a symlink on macOS), and creates a local connection registry. It does not change the global default model, authenticate services, start a client job or run paid model probes. Existing conflicting installations are refused. `--skip-browser-download` is available if a compatible browser is already configured.

Keep this checkout in place: the installed skill resolves this runtime. After pulling reviewed updates, rerun the installer to refresh the Windows skill copy and profiles. Unmodified files from this same installation can be updated; manually changed or unrelated installations are refused. Do not copy just SKILL.md or install this repository with a skill-only installer; that leaves out the runtime setup. Use `--codex-home` for a custom Codex home. The `--config-home` option changes the connection-registry location.

## Use in T3

1. Start a fresh chat with **GPT-6-Astra** selected.
2. Invoke **`$aat-master`** and attach the real brief, approved copy, brand kit and assets.
3. Review the result before proceeding to the next task. A person handles external delivery.

If the T3 picker misses a newly installed skill, fully quit and reopen T3. Provider refresh/window reload did not clear the workspace skill cache in the version used for initial testing.

Invoking a skill cannot change the main chat's model. Once Astra is selected, the runner explicitly starts Sol builders and fresh Astra review sessions. Missing model/tool access is a reported blocker, not permission to silently substitute another workflow.

## Check the installation

Windows PowerShell:

```powershell
.\runtime\.venv\Scripts\python.exe runtime/team.py status
.\runtime\.venv\Scripts\python.exe -m unittest discover -s runtime -p test_runtime.py -v
.\runtime\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS:

```sh
runtime/.venv/bin/python runtime/team.py status
cd runtime
.venv/bin/python -m unittest test_runtime -v
```

`status` checks source/profile hashes and local dependencies. It does not prove account access, successful image generation or visual quality. Optional `probe` commands in `team.py --help` start real model sessions and consume account usage.

## What is maintained where

- [.agents/skills/aat-master](.agents/skills/aat-master/SKILL.md): master routing and runner connection.
- [runtime/.agents/skills](runtime/.agents/skills): one canonical copy of each specialist and checklist.
- [runtime/RUN-A-JOB.md](runtime/RUN-A-JOB.md): actual execution procedure.
- [runtime/config.toml](runtime/config.toml): seven routes and model roles.
- [profiles](profiles): install-time templates; machine paths are generated locally.
- [VALIDATION.md](VALIDATION.md): checks performed and untested areas.
- [NOTICE.md](NOTICE.md): source attribution and asset licences.

Client briefs, identities, contact details, credentials, outputs and QA snapshots belong in separate client folders, never this repository. Agents must not edit production rules or pins to make a job pass. Human owners review changes and agree ownership before team adoption.
