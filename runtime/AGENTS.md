# Universal local design workflow

This is the user-requested Astra/Sol replacement workflow for all seven skills. This project-specific orchestration replaces the separate landing-only harness for jobs run here. It preserves image-first web direction and browser inspection. Do not run competing orchestration loops.

Astra orchestrates. Sol builds each isolated option (up to two concurrently). Built-in image_gen supplies images through the main Codex thread before building. Astra reviews in fresh read-only CLI sessions, first every image in bounded batches and then every rubric item. Human review and release remain separate. All roles use the selected skill and REVIEW.md under .agents/skills; those local versions take precedence over older installed same-name skills for this project.

Read RUN-A-JOB.md. Use the runtime/.venv Python. Client inputs and jobs belong in the appropriate client project; QA fixtures are explicitly synthetic. No shared client names, claims or assets belong in this runtime. No GitHub changes, publication or external sending during client production. No rules/checks/models edits during a job. Root policy concerns about new defect rules mean propose a lesson for a human owner, not edit checks.

Record every requested option; default two for new designs, one for a clone/template/scoped edit unless the brief or user specifies otherwise. Do not start production without the real brief and approved copy. Preserve source snapshots and results. Malformed review output is incomplete. A missing image, slide, page, route or test cannot silently pass. Do not claim that configuration tests are client-production tests.
