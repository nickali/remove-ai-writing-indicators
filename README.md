# remove-ai-writing-indicators

A skill for [Claude Code](https://claude.com/claude-code) and
[Pi](https://pi.dev) that finds the patterns making your writing read as
machine-produced, and takes them out without flattening your voice.

Works on anything: blog posts, essays, documentation, emails, resumes.

It follows the [Agent Skills](https://agentskills.io/specification) spec, so it
should load in any harness that reads a `SKILL.md`. Claude Code and Pi are the
two it has actually been tested against.

> **Fork this. It is tuned to for my tastes.**
>
> Every ruling in here is a judgment call I made for how I write: what counts as
> slop, what counts as voice, where the line sits between editing someone's
> words and replacing them. Some of those calls will be wrong for you. The
> opinions live in
> [`indicators.md`](https://github.com/nickali/remove-ai-writing-indicators/blob/main/skills/remove-ai-writing-indicators/indicators.md)
> and the rulings in
> [`SKILL.md`](https://github.com/nickali/remove-ai-writing-indicators/blob/main/skills/remove-ai-writing-indicators/SKILL.md).
> Change those and the rest keeps working. Using it unmodified means adopting
> my voice, which is not the point.

## Install

**Claude Code**

```
/plugin marketplace add nickali/remove-ai-writing-indicators
/plugin install remove-ai-writing-indicators@remove-ai-writing-indicators
```

**Pi**

```bash
pi install npm:remove-ai-writing-indicators          # released versions
pi install git:github.com/nickali/remove-ai-writing-indicators   # latest main
```

Add `-l` to install into one project instead of globally.

The npm install follows published releases. The git install tracks `main`, so
you get changes before they are released; Pi tells you at startup when the
remote has moved, and `pi update --extensions` pulls it. Pin a git ref
(`...@v1.0.0`) to freeze a version. Pinned packages are deliberately skipped
by updates.

## Use

```
/remove-ai-writing-indicators drafts/post.mdx            → Detect
/remove-ai-writing-indicators suggest drafts/post.mdx
/remove-ai-writing-indicators edit drafts/post.mdx
/remove-ai-writing-indicators rewrite drafts/post.mdx
```

In Pi the same thing is spelled `/skill:remove-ai-writing-indicators edit
drafts/post.mdx`, or just describe the task and let the agent load the skill.

The mode word goes next to the path, in either order. You can paste text
instead of giving a path, in which case nothing is written to disk.

Every run opens by stating which mode is active and what it will do.

## Modes

| Mode | Writes a file | What you get |
|---|---|---|
| **Detect** (default) | no | Every indicator that fires, with the line quoted |
| **Suggest** | no | The same findings, plus one proposed fix each |
| **Edit** | yes | A full draft, changed only by cutting and rearranging words already on the page |
| **Rewrite** | yes | A full draft with new prose where needed |

The modes are ordered by how much of the finished text is still yours. Detect
sits at the top and is the default, so the light-touch option is the one you get
by accident.

Edit mode is constrained to cutting and rearranging. That constraint is the
point: prose composed to replace AI prose tends to carry the same fingerprint,
so the mode that fixes the most is also the mode most likely to reintroduce the
problem. Rewrite lifts the constraint and says so in its banner.

Nothing is ever written to your source file. Edit and Rewrite write a sibling
`_v2` file next to the original, incrementing if that name is taken.

That sibling is made by copying your source and patching the copy, one
replacement per finding. Nothing is retyped from memory. This matters more than
it sounds: a model asked to write out a long document from the top loses things
along the way, a list item here, a trailing clause there, none of it flagged as
a change and none of it visible unless you diff. Patching a copy means the only
lines that can differ are the ones a finding pointed at.

The copy carries the original's frontmatter verbatim, including `title` and
anything controlling publication. In a static-site content collection (Astro,
Hugo, Eleventy) the `_v2` file is a second live page with a duplicate title
until you deal with it. The output is meant to replace the original after you
diff it, not to live beside it.

## What it catches

Around forty patterns, sorted by what the skill is allowed to do about each one.

### Surface (fixed without asking)

- **Machine vocabulary.** delve, leverage, robust, meticulous, transformative, elevate, embark, ever-evolving, tapestry
- **Inflated verbs.** "Spearheaded the migration" for "moved us to Postgres"
- **Empty adverbs.** just, literally, simply, truly, fundamentally, crucially
- **Empty phrases.** "It's worth noting," "at the end of the day," "in today's world," "let's dive in"
- **Filler metaphors.** "rich tapestry," "navigating the complexities," "the ever-evolving landscape"
- **Em dashes.** None under 300 words, one per 500 after that

### Structure (fixed by cutting and reordering)

- **Parallel construction.** "At X, I did Y. At Z, I did A."
- **Robotic transitions.** "Furthermore," "Moreover," "Additionally"
- **Binary contrasts.** "It's not X. It's Y."
- **Negative listing.** "Not a framework. Not a library. A compiler."
- **Colon reveals.** "The detail that makes it work: a separate process grades it."
- **Rhetorical setups.** "What if I told you," "Think about it:," "Plot twist:"
- **Faux-insight setups.** "What most people get wrong," "the part everyone misses"
- **Superficial analysis.** Trailing clauses: "highlighting," "underscoring," "showcasing"
- **Importance puffery.** "Stands as a testament," "marks a pivotal moment"
- **Interpretive metadiscourse.** "This distinction matters," "as you can see"
- **Weasel attribution.** "Experts agree," "studies show," "many argue"
- **Synonym cycling.** Rotating agent / assistant / tool for the same thing
- **Stacked fragments.** "That's it. That's the whole thing."
- **Fake-profound kickers.** "The future isn't coming. It's already here."
- **Summary-recap endings.** "In conclusion," "Ultimately," a closing restatement
- **Formatting slop.** Emoji headings, decorative bold, headers over two sentences

### Voice (fixed by deletion only)

- **Seesaw equivocation.** "However... on the other hand... while it's important to consider"
- **Forced-casual overcorrection.** "Look," "here's the deal," "the other guys"
- **Throat-clearing.** "Here's the thing," "let me be clear," "I'll be honest"

### Judgment (never fixed, always shown)

Real tells, but every available fix deletes something you chose to write. You
get the pattern named and the passage quoted, in all four modes, and you decide.

- **Tricolons.** "Faster, cleaner, and easier to maintain". Prose only: three things in a bullet are three things to do, not a rhythm
- **Paragraph symmetry.** Every paragraph the same length and shape
- **Uniform bullets.** "Led X / Built Y / Delivered Z"
- **Bullet overload.** A list where two sentences of prose would read better

### Substance (never fixed, always a question)

- **Missing specifics.** "Improved performance significantly"
- **Absent constraints.** No budget, deadline, headcount, or legacy dependency anywhere
- **No failure stories.** Every outcome a win, nothing tried that didn't work
- **No timeline anchors.** No "during," "after," "in Q3"
- **No named tools or competitors.** "Implemented automation"
- **Unmeasured outcomes.** A result claimed with no number
- **Portability test.** A sentence that could move to another company unchanged
- **Summary voice.** "Kubernetes improves deployment scalability" instead of "we moved to Kubernetes after our deploy scripts stopped being maintainable"
- **Flat emotional range.** One temperature start to finish

## Four decisions worth knowing about

### It asks instead of inventing

Findings are sorted into five groups by what the skill is allowed to do about
them: surface vocabulary, structure, voice, judgment, and substance. The first
three get fixed. The last two never do.

A substance finding means the draft is vague because a detail is missing, and
the only person who has that detail is you. Which competitor. What the number
was. What broke before you changed it. When this happened. So the skill asks
rather than filling the gap, and it holds to that in Rewrite mode too. Rewrite
lets it compose sentences. It does not let it compose facts.

This is the difference between an editor and a plausible-text generator. A
generator would close those gaps for you, and the result would be confident,
smooth, and partly false.

### Some patterns are shown to you, not fixed

Four indicators are real tells that the skill deliberately will not act on:
tricolons, paragraph symmetry, uniform bullets, and bullet overload. It names
them, quotes the passage, and hands them back to you. That happens in all four
modes, Edit and Rewrite included.

The reason is a line the skill applies to its own other groups. A fix is safe
when it removes *packaging* and leaves your claim standing — that is what
happens when it cuts "it's worth noting that," or "Furthermore," or "here's the
thing." You lose nothing you meant.

These four are different. Every fix available for them removes *content*.
"Cut the tricolon to two" deletes one of three things you chose to list.
"Merge the symmetrical paragraphs" deletes a sentence. "Convert the bullets to
prose" restructures a section wholesale. And choosing which member of a list is
expendable takes knowing which one matters, which is a judgment about what the
piece is for. That is yours.

The cost of getting this wrong is asymmetric, which is what settled it. A tell
left in a draft is a sentence that reads slightly machine-made. A member deleted
from a list is information gone, and gone invisibly — it does not show up in a
diff you were not already reading closely. One of those you can fix later. The
other you have to notice first.

This was not a design instinct. It came out of a run against two real reference
pages that lost five checklist items to the tricolon fix, each one an
instruction somebody was meant to follow.

### It preserves, it does not polish

The skill does not fix your grammar, spelling, or punctuation. It also does not
manufacture errors to make you look human.

Uniformly perfect mechanics are themselves a signal of machine production, so
correcting a comma splice removes evidence that a person wrote this. Injecting
errors on purpose is the same mechanical move in reverse, and it forges a voice
instead of preserving one. Neither is editing.

This is meant literally. A missing article stays missing, a comma splice stays
spliced, a typo stays misspelled. The skill will rearrange a sentence around
your slip, but it will not repair the slip, even when the correction is obvious
and the result would read better.

The honest cost: hand it a sloppy draft and you get a sloppy draft back with the
AI patterns gone. It is not a proofreader. Run a proofreader afterward if you
want one.

### Detect is the default

If you don't name a mode, you get the audit. Findings you can read, with the
lines quoted, and your draft untouched. You decide what to do next.

## What this is not

It is not built to beat AI detectors, and passing them is not a goal. Pangram,
GPTZero, and the rest are guessing at authorship from statistical shape. This
skill targets patterns that make writing worse to read, which overlaps with what
detectors flag but is not the same thing and is not measured the same way.

The skill never scores a draft or estimates a probability that a machine wrote
it. It names patterns and quotes lines. A named pattern is evidence you can
check yourself. A score is somebody else's guess.

## Known limitations

Things the skill does not solve, as distinct from things it deliberately
refuses to do.

**It is not deterministic.** Two runs over the same draft find different sets of
findings and produce different edits. Nothing in here is a parser, and none of
it is a guarantee. Diff any output you intend to keep.

**Pasted text has no copy to patch.** Edit and Rewrite protect your words by
copying the file and replacing only the spans a finding quoted. Paste text
instead of giving a path and there is no file, so that protection is gone and a
long paste can come back quietly shortened. Give it a path for anything past a
few paragraphs.

**A quoted span has to be unique to patch safely.** The skill is told to carry
enough surrounding context that each replacement matches in exactly one place.
In a draft that repeats a phrase often enough, a fix can still land on the wrong
occurrence. This is the failure mode to watch for in a diff.

**Recall on a long document is not guaranteed.** Scanning forty patterns across
a 500-line reference page will miss some. What it reports is real. What it does
not report is not a clean bill of health.

**Edit mode on list-heavy drafts is the failure mode to watch.**

A page that is mostly nested bullets is the shape most likely to lose content:
a member from a three-item list, a trailing clause, sometimes a verb. The losses
are quiet, because they land on lines no indicator fired on and so never show up
in the **What changed** report.

Measured on `examples/checklist-draft.md`, a 28-line checklist with six
three-part lists. Seven runs of an earlier version of the rules lost two to four
list members every time, and a different set each time. The current rules —
ruling 5, tricolons scoped to prose, the deletion-shaped fixes moved into
Judgment, and the copy-then-patch procedure in **Producing an edit** — hold all
eighteen members and the list count, which `tests/` asserts on every agent run.

That is one fixture passing, not a proof. The underlying pressure has not gone
anywhere: writing a long document out is an act of regeneration, and
regeneration compresses. On a 500-line reference page, diff the output.

## Fixtures

Two drafts, testing opposite halves of the skill.

`examples/slop-draft.md` is a deliberately bad piece of prose, and
`examples/expected-findings.md` is what Detect should report on it.

`examples/checklist-draft.md` is reference material: nested bullets, six
tricolons, every one of them a list of things to do rather than a rhythm.
`examples/expected-findings-checklist.md` is mostly a list of edits that would
be *wrong*. It exists because a real Edit run on two checklist pages quietly
deleted five list items to satisfy the tricolon rule, which is how ruling 5 got
written.

Answers live in separate files on purpose. Keep them out of the run — if they
are in context the model copies them instead of finding them, and the check
proves nothing.

## Releasing

```bash
npm version patch     # or minor / major
git push --follow-tags
npm publish
```

The version lives in `package.json` and `.claude-plugin/plugin.json`. Never
bump them by hand: a `version` lifecycle script copies the number across and
stages it, so `npm version` is the only thing that should touch either. A test
asserts the two agree, so drift fails the suite rather than reaching a user.

## Tests

Stdlib `unittest`, no dependencies.

```bash
cd tests
python3 -m unittest discover -v                    # structure and install checks
SKILL_AGENT_TESTS=1 python3 -m unittest discover -v  # plus all four modes, for real
```

`test_claude_code.py` and `test_pi.py` cover one harness each. The default run
is instant and free: it validates the plugin manifests, the skill frontmatter,
the indicator groups, that the skill references no other skill, that the fixture
does not ship its own answer key, and that the skill is actually installed in
that harness.

The agent-driven tests are opt-in because they invoke a real model, take
minutes, and cost tokens. They assert only on what is deterministic: Detect and
Suggest write no files, Edit writes `_v2` and leaves the source byte-identical,
Rewrite increments to `_v3` rather than clobbering an existing `_v2`, and the
draft's missing article survives both write modes. Each run happens in a
throwaway temp directory holding one copy of the draft.

The checklist run is the strictest of them. Every member of every tricolon in
that fixture is a string that appears exactly once, so the test can prove by
presence that nothing was deleted, while still allowing the fixes ruling 5 does
permit: resequencing, splitting an entry, changing a connector.

## License

MIT

## Acknowledgements

This builds on [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter
Yang, reorganized around my own taste and my own rules about what an editor is
allowed to do on your behalf. The group structure, the four modes, the substance
and judgment rules, and the preserve-don't-polish ruling are mine. A good share
of the pattern list started as his.
