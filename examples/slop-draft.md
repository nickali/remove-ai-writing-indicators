# Fixture

A deliberately bad draft and the findings Detect mode should produce on it. Run
Detect against the draft after changing `SKILL.md` or `indicators.md` and check
the output against the expected list.

## Draft

Here's the thing about meetings: most teams get them wrong.

Our team decided to leverage a more robust approach to how we run our weekly
sync. It's worth noting that meetings can be a significant drain on productivity
— and morale — and focus. Furthermore, asynchronous communication improves team
alignment and reduces context switching.

We made three changes: we shortened the meeting, we added an agenda, and we cut
attendee list. The result: engagement improved significantly.

However, it's important to consider that synchronous meetings still have value.
On the other hand, some argue that async-first is the future. Studies show that
teams who adopt async practices see better outcomes.

At the end of the day, the change was a success. Meetings are not a problem to
be solved. They're a tool to be sharpened.

## Expected Detect findings

### Surface

- **Machine vocabulary** — "decided to leverage a more robust approach" → two in one clause
- **Empty phrases** — "It's worth noting that", "it's important to consider that", "At the end of the day"
- **Em dashes** — "productivity — and morale — and focus" → a cluster in a draft under 300 words, where the allowance is zero

### Structure

- **Tricolon** — "productivity — and morale — and focus"
- **Tricolon** — "we shortened the meeting, we added an agenda, and we cut attendee list"
- **Robotic transition** — "Furthermore, asynchronous communication improves..."
- **Colon reveal** — "The result: engagement improved significantly."
- **Weasel attribution** — "some argue that async-first is the future" and "Studies show that teams who adopt async practices see better outcomes" → escalates to a Substance question, since the draft names no source
- **Binary contrast** — "Meetings are not a problem to be solved. They're a tool to be sharpened."
- **Fake-profound kicker** — the same closing line, which turns the point into an aphorism
- **Summary-recap ending** — "At the end of the day, the change was a success."

### Voice

- **Throat-clearing** — "Here's the thing about meetings:"
- **Seesaw equivocation** — "However, it's important to consider... On the other hand, some argue..." → the draft never lands anywhere

### Substance

- **Summary voice** — "asynchronous communication improves team alignment and reduces context switching" → written from above. Ask: what changed for your team specifically, and what broke before you changed it?
- **Unmeasured outcome** — "engagement improved significantly" → ask: measured how, from what to what?
- **No timeline anchors** — nothing says when this happened or what else was going on
- **No named tools** — "asynchronous communication" names no tool the team actually used
- **Flat emotional range** — one temperature start to finish. Fires on the document, so no quoted line. Ask: which part of this annoyed you?

### Not findings

- "we cut attendee list" is missing an article. **Preserve ruling** — leave it. The skill does not correct the writer's grammar, and Edit mode output should still contain this error.
