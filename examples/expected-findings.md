# Expected findings for `slop-draft.md`

What Detect mode should report on `examples/slop-draft.md`. Check the skill
against this after editing `SKILL.md` or `indicators.md`.

**Keep this file out of the run.** Point the skill at `slop-draft.md` alone. If
this file is in context, the model can copy the answers instead of finding them,
and the check proves nothing.

## Surface

- **Machine vocabulary** — "decided to leverage a more robust approach"
- **Empty phrases** — "It's worth noting that", "it's important to consider that", "At the end of the day"
- **Em dashes** — "productivity — and morale — and focus". Draft is under 300 words, so the allowance is zero

## Structure

- **Robotic transition** — "Furthermore, asynchronous communication improves..."
- **Colon reveal** — "The result: engagement improved significantly."
- **Weasel attribution** — "some argue that async-first is the future" and "Studies show that teams who adopt async practices see better outcomes". No source named, so this escalates to a Substance question
- **Binary contrast** — "Meetings are not a problem to be solved. They're a tool to be sharpened."
- **Fake-profound kicker** — the same closing line
- **Summary-recap ending** — "At the end of the day, the change was a success."

## Voice

- **Throat-clearing** — "Here's the thing about meetings:"
- **Seesaw equivocation** — "However, it's important to consider... On the other hand, some argue..."

## Judgment

Reported with the line quoted, never fixed, in all four modes. Edit and Rewrite
output should still contain both of these intact.

- **Tricolon** — "productivity — and morale — and focus". The em dashes go, all three nouns stay
- **Tricolon** — "we shortened the meeting, we added an agenda, and we cut attendee list"

## Substance

- **Summary voice** — "asynchronous communication improves team alignment and reduces context switching"
- **Unmeasured outcome** — "engagement improved significantly"
- **No timeline anchors** — nothing says when this happened
- **No named tools** — no tool the team actually used is named
- **Flat emotional range** — fires on the document, so no quoted line

## Not findings

- "we cut attendee list" is missing an article. **Preserve ruling** — leave it. Edit and Rewrite output should still contain this error.
