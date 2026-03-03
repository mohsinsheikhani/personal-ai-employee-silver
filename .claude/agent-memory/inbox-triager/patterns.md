# Classification Patterns and Edge Cases

## C-Level Senders

- Always classify as Urgent minimum when addressed directly in TO:
- A same-day deadline from CEO overrides all other signals — send immediately
- If deadline has already passed, flag as escalation requiring apology

## Newsletter / Digest Senders

- Any `newsletter@`, `digest@`, `noreply@` sender with a recurring subject pattern defaults to Low
- Confirm by checking: no direct question, mass recipient list, purely informational body

## Internal Teammates (non-manager)

- Default to Important when they ask a direct question requiring your specific answer
- Elevate to Urgent only if they are blocked on a project you own AND deadline is today
- If sender role is unclear (peer vs. direct report), flag it for user confirmation

## Ambiguous Deadlines

- "by 2pm" without a date = assume today; flag if current time is close or past
- "ASAP" without a date = Important, not automatically Urgent unless from C-level or manager
- "end of week" = Important, not Urgent unless today is Friday

## CC vs. TO Field

- CC: always lowers priority by one level relative to TO: classification
- TO: sole recipient = elevate; TO: one of many = maintain; CC: = lower
