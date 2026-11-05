---
name: headless-gs-update
description: Configure a headless, subagent-driven workflow that documents customer meetings and follow-up emails in a user-selected GitHub repository, then publishes validated activities to Gainsight through the shared production pipeline.
---

# Headless Gainsight Update

Use this skill when a GitHub employee wants to set up or revise an unattended
customer-interaction and Gainsight publication automation.

The skill is a setup wizard. It must collect and validate the user's own
configuration before creating or changing any automation. Never reuse another
person's customer list, account identifiers, repositories, mailbox identity,
schedule, or production authorization.

## Intended outcome

Create two enabled automations:

1. A daily workflow that delegates customer-interaction documentation to one
   fresh subagent, waits for successful completion, and then delegates
   Gainsight publication to a second fresh subagent.
2. A validation workflow that checks the prior business day's work and reruns
   only missing or failed stages, in the same order.

The automation coordinator must remain compact. It should retain only status,
stable source identifiers, links, and source gaps from each subagent.

## Required services and tools

- GitHub Copilot app automation tools.
- GitHub CLI authenticated to repositories selected during setup.
- Microsoft 365 data through WorkIQ for Outlook calendar, meeting artifacts,
  and Sent Items.
- Revenue Copilot access to Salesforce and Gainsight account data.
- Read and write access to the user's customer-interaction issue repository.
- Read and write access to the production repository, which defaults to
  `github/project-alfred-automation`.
- Access to the current `aic-gs-timeline` skill and production Meeting issue
  template used by the shared Gainsight pipeline.

If a required service is unavailable, identify the exact missing connection or
permission. Do not create a partially enabled production workflow that could
silently omit data.

## Setup interview

Ask one focused question at a time with the interactive question tool. Reuse an
answer only within the current setup session.

Collect:

1. The source GitHub repository in `owner/repository` form where customer
   meeting issues and follow-up comments will be stored.
2. Confirmation that the repository already exists and that the signed-in
   GitHub identity may read and write issues and labels there.
3. The user's time zone.
4. The daily execution time. Recommend 5:00 PM in the user's time zone.
5. The validation time. Recommend 9:00 AM in the user's time zone.
6. Whether the daily workflow should run every day or weekdays only.
7. The user's internal email address used to identify their own calendar,
   messages, and meeting participation.
8. The Salesforce Account IDs for the user's book of business.
9. A short, unique GitHub label for each account.
10. Whether `github/project-alfred-automation` is the correct production
    publishing repository. Use it as the default, but allow an authorized
    alternative.

For the account list, instruct the user to use Revenue Copilot to find their
customers and obtain the canonical Salesforce Account IDs. Accept either:

- a prepared list of Salesforce Account IDs; or
- an interactive Revenue Copilot account search performed during setup.

For each supplied Salesforce Account ID:

1. Resolve the canonical Salesforce account record.
2. Resolve parent hierarchy only when requested or required for the intended
   customer scope.
3. Resolve the Gainsight company GSID from authenticated Revenue Copilot data.
4. Ask for or confirm a short GitHub customer label.
5. Reject ambiguous identities or duplicate labels.
6. Never guess an account name, hierarchy, Salesforce ID, or Gainsight GSID.

Keep the account map only in the user's generated automation configuration.
Do not add customer identifiers to this reusable skill.

## Preflight validation

Before creating automations:

1. Verify WorkIQ can read the user's calendar, meeting artifacts, and Sent
   Items.
2. Verify Revenue Copilot can resolve every configured Salesforce account and
   Gainsight company GSID.
3. Verify the authenticated GitHub identity and repository permissions with
   `gh auth status` and read-only `gh api` requests.
4. Verify Issues are enabled in the source and production repositories.
5. Verify the source repository has a `Meeting Notes` label. Offer to create
   missing customer labels only after showing the exact labels.
6. Read the current `aic-gs-timeline` skill and production Meeting issue
   template at runtime. Do not hardcode a stale production form schema.
7. Search existing automations for a matching setup. Offer to update an
   existing pair instead of creating duplicates.

Use authenticated `gh api` and `gh issue` commands for cross-repository issue,
comment, and label operations in the generated workflows. Do not treat a
higher-level GitHub tool permission denial as proof that repository access is
missing. If `gh` itself fails, report its exact error.

## Production approval gate

Show the user a complete setup summary containing:

- source and production repositories;
- time zone and schedules;
- account names, labels, Salesforce Account IDs, and resolved Gainsight GSIDs;
- data sources and repository effects;
- validation and retry behavior;
- the fact that labeling a production issue triggers a real Gainsight write.

Ask:

`Do you approve creating and enabling these automations with production Gainsight writes?`

Do not create or enable production automations until the user explicitly
approves that exact setup. If they decline, offer a validation-only
configuration that performs discovery and reports proposed records without
creating or labeling production issues.

## Daily automation

Create one coordinator automation for the configured schedule and time zone.
Its prompt must include the resolved account map and these rules.

### Stage 1: document customer interactions

Delegate to a fresh subagent. For the target local calendar date:

1. Enumerate the user's calendar events through WorkIQ.
2. Exclude canceled, declined, internal-only, social, and not-yet-ended events.
3. Confirm that external attendees and meeting context map unambiguously to one
   configured account.
4. Retrieve available transcripts, meeting notes, recap artifacts, or chat
   content.
5. If no transcript or meeting notes exist, use only the invitation or
   description for limited context and explicitly mark the call summary
   unavailable.
6. A missing transcript must not exclude an otherwise qualifying meeting,
   including a meeting organized by someone outside the user or GitHub.
   Organizer ownership is not attendee presence.
7. Create or update one source issue per meeting. Use a title beginning with
   the local date as `MM-DD-YYYY ` followed by the meeting title.
8. Preserve a stable calendar event ID in the issue so reruns and title changes
   deduplicate correctly.
9. Apply `Meeting Notes` and exactly one configured customer label.
10. Include matching evidence, local date and time, organizer, supported
    attendees, agenda, substantiated summary, decisions, commitments, action
    items, risks, next steps, source references, and explicit coverage gaps.
11. Do not invent discussion, decisions, attendance, or follow-up work.

Also inspect newly sent customer email since the last successful run. On the
first run, limit mail to the target date.

Match a sent email to a documented meeting only when at least one exact
external recipient attended that meeting and the customer identity agrees.
Add a deduplicated source issue comment containing a concise faithful account
of what the user newly wrote, supported commitments, and a stable mail ID.
Exclude quoted history, attachments, signatures, secrets, invitations,
responses, logistics-only messages, automated mail, and internal-only mail.
Never send or reply to email.

Return only compact completion status, created or updated links, stable event
and mail IDs, skips, and source gaps.

### Stage gate

Do not start Stage 2 unless Stage 1 completed successfully. If Stage 1 failed
or was blocked, report the exact failure and stop.

### Stage 2: publish validated activities

Delegate to a second fresh subagent for the same target date.

1. Read candidate source issues from the configured source repository.
2. Require `Meeting Notes` plus exactly one configured customer label.
3. Corroborate the labeled account against the source issue body.
4. Exclude canceled, declined, email-only, ambiguous, or invitation-only
   records that do not establish that the call occurred and the user joined.
5. Do not exclude a valid call merely because its transcript is missing.
6. Copy the complete raw source issue body byte-for-byte into the production
   Meeting form's Note field. Keep provenance outside Note.
7. Process substantive outbound customer emails for the target date. Copy the
   complete newly authored text into Note after safely removing signatures,
   quoted history, attachments, and restricted content.
8. Resolve the production Company ID from the configured Gainsight GSID.
9. Use the current production template, picklists, validation rules, and label
   mechanism from `aic-gs-timeline`.
10. Search all production issue states using stable source markers, account,
    subject, and time. Never recreate an existing pending, labeled, synced, or
    failed occurrence.
11. Validate form order, Note integrity, required fields, and size limits.
12. Create each validated production issue, then apply the existing production
    ready-to-sync label that triggers the Gainsight write.
13. Do not treat labeling as proof of successful synchronization. Report
    pending, synced, and failed statuses separately.

If source content contains credentials, restricted data, an incompatible form
heading, an ambiguous email boundary, or content that cannot be copied safely,
skip the record and report the reason rather than silently modifying it.

## Validation automation

Create a second coordinator automation.

Recommend 9:00 AM Monday through Saturday:

- Monday validates the preceding Friday.
- Tuesday through Saturday validate the immediately preceding calendar day.
- Sunday skips.

Use fresh subagents and the same stage gate:

1. Validate source meeting issues, labels, stable event IDs, and matching email
   comments for the target date.
2. Rerun Stage 1 only for missing or failed records.
3. After Stage 1 validates, verify production source markers, account, subject,
   time, Note integrity, labels, and pipeline status.
4. Rerun Stage 2 only for missing or failed records.
5. Never duplicate an existing pending, labeled, synced, or failed occurrence.

The validation automation is explicitly authorized to process its calculated
historical target date, while retaining every other privacy, validation,
deduplication, and production-write safeguard.

## Completion

After creation:

1. Read both saved automations back and verify their names, schedules, time
   zone assumptions, prompts, enabled state, repositories, and account map.
2. Report both automation IDs and next run times.
3. Recommend a one-off test for an explicit recent date.
4. During the test, require Stage 1 to finish before Stage 2 starts.
5. Report source issue links, production issue links, sync status, skips, and
   source gaps.

Never modify another user's existing automations, repositories, labels, or
account configuration unless they explicitly chose an update during setup.
