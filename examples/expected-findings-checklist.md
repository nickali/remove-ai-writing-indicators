# Expected findings for `checklist-draft.md`

What Detect mode should report on `examples/checklist-draft.md`, and more
usefully, what Edit mode must **not** do to it. This fixture exists because a
real run on two reference pages dropped five checklist items to the tricolon
rule.

**Keep this file out of the run.** Point the skill at `checklist-draft.md`
alone.

## Surface

- **Machine vocabulary** — `Utilize` (3×), `Leverage` (2×), `enhance`
- **Machine vocabulary, replacement quality** — the two `Leverage` lines sit
  four lines apart and want different verbs, and neither may collide with what
  is already nearby. "Follow" is the obvious pick for the first one, and it is
  wrong: the child bullet directly underneath already starts with "Follow the
  three analysts". Swapping one overused word for one repeated word is not a
  fix. The second line wants something like "Mine", not a second copy of
  whatever the first line took
- **Machine vocabulary, dropped object** — "clarify instructions and enhance
  user comprehension". `help users understand` dangles: understand *what*. Edit
  mode cuts the phrase; only Rewrite may compose a replacement clause

## Structure and Judgment

Nothing fires in either group, and that is the point of the fixture.

Six three-part lists sit in this draft. Tricolon is a Judgment finding now, so
it would be reported rather than fixed anywhere — but every one of these is
inside a list item, which under ruling 5 means it is not a tricolon at all. It
should not even be reported. Three things in a bullet are three things to do:

| Line | Tricolon |
|---|---|
| company size, vertical, and renewal date | third member is the one that dates the data |
| goals, blockers, and workarounds | workarounds are the finding, not filler |
| prices, discounts, and promo tactics | — |
| public records, filings, and earnings calls | SEC filings ≠ generic public records |
| blog posts, videos, or infographics | three deliverables |
| likes, shares, and comments | shares are the referral metric |

Cutting any of these to two is the failure this fixture was built to catch. So
is deleting a bullet whose verb is wrong: the two `Leverage` lines are tasks,
and "no plain word fits, so the sentence was empty" does not apply to a list
item. Replace the verb and keep the task.

## Substance

- **Missing specifics** — "five customers" is anchored, "the three analysts" is
  not: which analysts?
- **No named tools** — "the CRM export" names no CRM
- **Unmeasured outcomes** — nothing here has a target attached

## Not findings

- Line count and heading count come back unchanged
- **Bullet overload** may fire, and that is acceptable now that it is a Judgment
  finding: it gets quoted and handed back, not applied. Reporting "this is 18
  nested bullets, your call" costs the writer nothing. Converting a checklist to
  prose would have destroyed the page, which is why the fix moved out of
  Structure in the first place
