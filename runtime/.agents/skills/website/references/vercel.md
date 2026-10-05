# Vercel: local preparation and human release

This is a checklist for the human release operator. It does not permit an agent to deploy, upload, push a deployment-triggering branch, change DNS, promote an alias, replace a live site or roll back production. Preview deployments are releases too.

## Agent’s local preparation

Read existing configuration without changing the remote project. Record the intended team/project, root, build/output settings, source revision, local QA evidence and required environment variable names; never record secret values. Ask for missing destinations, access requirements and the person who will release. Package only the intended public build/source and necessary assets, keeping private notes and client records outside it. Prepare a human test checklist for links, forms, receipt and promised downloads/emails. Do not run deployment commands.

## Human operator’s steps

1. Confirm the designer inspected every option at full and phone sizes and identify the approved source revision.
2. Confirm the Vercel project and preview/production target, current official tooling instructions, environment and access. The human obtains secrets through secure configuration.
3. The human performs the authorised deployment. DNS changes, production promotion, replacement and rollback are separate human decisions; never use them as an automated workaround.
4. Record the returned URL and deployment identifier. Verify routes, assets, desktop/mobile layout, navigation and console errors. The human performs external form test submissions and verifies actual receipt and fulfilment with approved test data.
5. Record release results and unresolved issues. A command exit code or local mock does not establish a working live journey.

The agent may inspect a human-supplied public URL read-only, without sending forms or triggering external effects. Report local QA, human design approval, human release and live verification separately. Unresolved items block the corresponding readiness claim, not truthful delivery of local draft work.
