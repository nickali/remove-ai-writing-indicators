# remove-ai-writing-indicators

A Claude Code skill that finds the patterns making your writing read as
machine-produced, and takes them out without flattening your voice.

Works on anything: blog posts, essays, documentation, emails, resumes.

## Install

**Claude Code**

```
/plugin marketplace add nickali/remove-ai-writing-indicators
/plugin install remove-ai-writing-indicators@remove-ai-writing-indicators
```

**Pi**

```bash
pi install git:github.com/nickali/remove-ai-writing-indicators
```

Add `-l` to install into one project instead of globally. Pi tracks `main` and
tells you at startup when the remote has moved; run `pi update --extensions` to
pull it. To freeze a version instead, install a pinned ref
(`...@v1.0.0`) — pinned packages are deliberately skipped by updates.

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

## What it catches

Around forty patterns, sorted by what the skill is allowed to do about each one.

### Surface — fixed without asking

- **Machine vocabulary.** delve, leverage, robust, meticulous, transformative, elevate, embark, ever-evolving, tapestry
- **Inflated verbs.** "Spearheaded the migration" for "moved us to Postgres"
- **Empty adverbs.** just, literally, simply, truly, fundamentally, crucially
- **Empty phrases.** "It's worth noting," "at the end of the day," "in today's world," "let's dive in"
- **Filler metaphors.** "rich tapestry," "navigating the complexities," "the ever-evolving landscape"
- **Em dashes.** None under 300 words, one per 500 after that

### Structure — fixed by cutting and reordering

- **Tricolons.** "Faster, cleaner, and easier to maintain"
- **Paragraph symmetry.** Every paragraph the same length and shape
- **Parallel construction.** "At X, I did Y. At Z, I did A."
- **Uniform bullets.** "Led X / Built Y / Delivered Z"
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

### Voice — fixed by deletion only

- **Seesaw equivocation.** "However... on the other hand... while it's important to consider"
- **Forced-casual overcorrection.** "Look," "here's the deal," "the other guys"
- **Throat-clearing.** "Here's the thing," "let me be clear," "I'll be honest"

### Substance — never fixed, always a question

- **Missing specifics.** "Improved performance significantly"
- **Absent constraints.** No budget, deadline, headcount, or legacy dependency anywhere
- **No failure stories.** Every outcome a win, nothing tried that didn't work
- **No timeline anchors.** No "during," "after," "in Q3"
- **No named tools or competitors.** "Implemented automation"
- **Unmeasured outcomes.** A result claimed with no number
- **Portability test.** A sentence that could move to another company unchanged
- **Summary voice.** "Kubernetes improves deployment scalability" instead of "we moved to Kubernetes after our deploy scripts stopped being maintainable"
- **Flat emotional range.** One temperature start to finish

## Three decisions worth knowing about

### It asks instead of inventing

Findings are sorted into four groups by what the skill is allowed to do about
them: surface vocabulary, structure, voice, and substance. The first three get
fixed. The fourth never does.

A substance finding means the draft is vague because a detail is missing, and
the only person who has that detail is you. Which competitor. What the number
was. What broke before you changed it. When this happened. So the skill asks
rather than filling the gap, and it holds to that in Rewrite mode too. Rewrite
lets it compose sentences. It does not let it compose facts.

This is the difference between an editor and a plausible-text generator. A
generator would close those gaps for you, and the result would be confident,
smooth, and partly false.

### It preserves, it does not polish

The skill does not fix your grammar, spelling, or punctuation. It also does not
manufacture errors to make you look human.

Uniformly perfect mechanics are themselves a signal of machine production, so
correcting a comma splice removes evidence that a person wrote this. Injecting
errors on purpose is the same mechanical move in reverse, and it forges a voice
instead of preserving one. Neither is editing.

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

## Fixture

`examples/slop-draft.md` is a deliberately bad draft.
`examples/expected-findings.md` is what Detect should report on it. Useful for
checking the skill still behaves after you edit `SKILL.md` or `indicators.md`.

They are separate files on purpose. Keep the expected findings out of the run —
if the answers are in context, the model copies them instead of finding them,
and the check proves nothing.

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

## License

MIT

## Acknowledgements

This builds on [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter
Yang, reorganized around my own taste and my own rules about what an editor is
allowed to do on your behalf. The four-group structure, the four modes, the
substance rule, and the preserve-don't-polish ruling are mine. A good share of
the pattern list started as his.
