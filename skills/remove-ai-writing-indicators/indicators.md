# Indicator catalog

Read this when scanning a draft. Findings are grouped by what you are permitted
to do about them, not by how the pattern looks. The group is the rule.

Every entry is named after the defect, not the goal.

---

## Surface

Vocabulary and punctuation. Mechanical. **Fixable in Edit and Rewrite without
asking.**

**Machine vocabulary.** delve, foster, leverage, utilize, facilitate, empower,
streamline, robust, cutting-edge, meticulous, intricate, paramount,
transformative, elevate, embark, harness, ever-evolving, tapestry, realm,
beacon, multifaceted, comprehensive, innovative, testament, paradigm shift, game
changer, supercharge.
→ Replace with the plain word. "Utilize" is "use." "Facilitate" is usually
"run," "host," or "let." If no plain word fits, the sentence was empty and goes.
**In a list item it never goes** — a bullet with the wrong verb on it is still a
task somebody has to do. Replace the verb in place, or leave the line and flag
it.
→ **Pick the replacement per sentence, not per draft.** "Leverage" has no one
clean synonym. It is "use" here, "mine" there, "follow" or "partner with"
elsewhere, depending on what is being leveraged. Check the neighboring lines
before settling. Swapping one overused word for one repeated word is not a fix.
→ **Keep the object.** "Enhance user comprehension" is not "help users
understand," which drops what they understand. If the plain verb cannot carry
the object, cut the phrase rather than leave it dangling. Composing a
replacement clause is Rewrite mode only.

**Inflated verbs.** spearheaded, orchestrated, architected, strategized,
synergize.
→ Say what was actually done. "Spearheaded the migration" is "moved us to
Postgres."

**Empty adverbs.** just, literally, honestly, simply, actually, truly,
fundamentally, importantly, crucially, inherently, inevitably.
→ Cut when they add nothing. Keep when they carry emphasis, contrast,
uncertainty, or the writer's spoken rhythm. "I honestly don't know" keeps it.

**Empty phrases.** it's worth noting, it's important to note, at the end of the
day, when it comes to, at its core, in today's world, in the age of, the reality
is, the truth is, in terms of, in order to, going forward, in this article,
let's dive in.
→ Cut. The sentence starts later.

**Filler metaphors.** rich tapestry, navigating the complexities, the
ever-evolving landscape, breaking barriers, a double-edged sword.
→ Cut. Replace with the thing itself if a claim was hiding inside.

**Copula dodges.** serves as, stands as, functions as, acts as, operates as,
represents, constitutes, marks, all standing in for "is" or "are".
→ Use the plain verb. "Gallery 825 serves as the exhibition space" is "Gallery
825 is the exhibition space." The dodge exists to avoid repeating "is", which
was never a problem worth solving.

**Decorative unicode.** Curly quotes and apostrophes, arrows, bullet
characters, ellipsis characters, non-breaking spaces, in a document whose other
text is plain ASCII.
→ Match what the rest of the draft uses, and what its neighbouring files use if
it lives in a directory of them. Consistency is the test, not purity: a file
that is curly throughout stays curly. An arrow doing real work in a diagram or
a code sample stays.

**Em dashes.** None in drafts under 300 words. At most one per 500 words beyond
that, and only where it clearly beats a comma, period, or parentheses.
→ Remove clusters first. A dash used for rhythm rather than structure is the
one to cut.
→ A double hyphen (`--`) between spaces is the same habit in disguise and
counts against the same allowance.

---

## Structure

How the prose is shaped. **Fixable by cutting and reordering words already
present.** Compose nothing new.

**Parallel construction.** "At X, I did Y. At Z, I did A." The same template
refilled.
→ Break the pattern on at least one instance. Reorder so the subject moves.

**Robotic transitions.** Furthermore, Moreover, Additionally, Consequently,
starting a paragraph.
→ Delete the word. The paragraph almost always stands without it.

**Binary contrasts.** "This is not X. It's Y." / "The question isn't X, it's Y."
/ "It's not just X, but Y."
→ State Y directly.

**Negative listing.** "Not a framework. Not a library. A compiler."
→ Say what it is.

**Colon reveals.** A noun phrase, a colon, then a lowercase dramatic reveal.
"The detail that makes it work: a separate process grades it."
→ Rewrite as a plain sentence using the same words. Colons are for lists,
labels, and quotes.

**Rhetorical setups.** "What if I told you...", "Think about it:", "Plot twist:",
and question-then-answer pairs the writer asks themselves.
→ Delete the setup. Keep the answer.

**Faux-insight setups.** "What most people get wrong," "here's what nobody tells
you," "the part everyone misses."
→ Delete the setup and let the claim stand alone.

**Superficial analysis.** Trailing `-ing` clauses that pretend to interpret:
highlighting, underscoring, reflecting, showcasing, demonstrating.
→ Cut the clause, or replace it with the consequence if one is already stated
elsewhere in the draft.

**Importance puffery.** "Stands as a testament," "marks a pivotal moment,"
"plays a vital role," "underscores its significance."
→ State the fact and let the reader judge.

**Interpretive metadiscourse.** Lines telling the reader what to notice: "this
distinction matters," "as you can see," "the key point is," redundant "in other
words."
→ Delete. If the point needs support, the support is a Substance finding.

**Weasel attribution.** "Experts agree," "studies show," "many argue," "widely
regarded as."
→ Name the source if the draft has one. If not, this becomes a Substance
question. Never invent a source.

**Synonym cycling.** Rotating terms for variety. "The agent reviews the draft.
The assistant scores the piece. The tool suggests fixes."
→ Repeat the correct word.

**Stacked fragments.** Drumbeat fragmentation for drama. "That's it. That's the
whole thing." / "X. And Y. And Z."
→ Cut the stack. **Isolated fragments that vary cadence are kept** — rhythm
variation is a human signal, drumbeat repetition is not.

**Fake-profound kickers.** A final "deep" line turning the point into a
metaphor, aphorism, or mic-drop.
→ Delete it. Do not rewrite it into a better metaphor. End on the last concrete
sentence already in the draft.

**Summary-recap endings.** "In conclusion," "Ultimately," "Overall," or a
closing paragraph restating the piece.
→ Cut. The reader was just there.

**Formatting slop.** Emoji in headings, bold sprinkled mid-sentence for
emphasis, a header over a two-sentence section.
→ Remove. Format follows content.

---

## Voice

How the writer comes across. **Fix by deletion only. Never compose a
replacement.**

The test for this group: cut the hedge or the announcement, and the writer's
actual claim is left standing. If deleting removes content rather than
packaging, it is not a Voice finding — check Substance.

**Seesaw equivocation.** Every angle weighted equally, landing nowhere.
"However," "on the other hand," "while it's important to consider," stacked
until no position is taken.
→ Delete the hedges. Whatever claim remains is the writer's actual position. If
no claim remains, flag it as a Substance question.

**Forced-casual overcorrection.** Conversational tone worn as a costume.
"Look," "here's the deal," "the other guys," "happy to chat," "let's be real."
→ Delete the interjection. The sentence underneath is usually fine.

**Throat-clearing.** Announcing a point instead of making it. "Here's the
thing," "let me be clear," "I'll be honest," "the uncomfortable truth is."
→ Delete. The point starts one clause later.

---

## Judgment

**Real patterns, but every available fix costs content the writer chose to put
there.** Reported in every mode, fixed in none. Quote the passage, say what
fires, and leave it alone.

Substance findings are gaps: something is missing and only the writer has it.
These are the opposite. The material is all present, and the only fixes on offer
delete some of it. Which member of a list is expendable, which sentence in a
symmetrical run can go, whether these bullets are better as prose. Those are
decisions about what the piece is for, and the writer is the one who knows.

Report them where the writer can act on them and stop there. An unfixed finding
they can see beats a confident edit that quietly costs them a line.

**Tricolons.** Listing exactly three things, repeatedly. "Faster, cleaner, and
easier to maintain."
→ Quote the list. Cutting to two removes something the writer chose to include,
and choosing which one goes means knowing which one matters.

→ **Prose only.** Three things inside a list item, a heading, or a table cell is
not a tricolon at all. There the third thing is something the reader has to do,
not a beat in a sentence. Do not report it. See ruling 5.

**Paragraph symmetry.** Paragraphs of near-identical length and shape running
down the page.
→ Quote the opening of each and say how many in a row. Merging or trimming them
means deciding which sentences are expendable.

**Uniform bullets.** Every bullet the same length, every one opening with a past
tense verb. "Led X / Built Y / Delivered Z."
→ Quote two or three of them. Varying the shape means rewriting the entries.

**Bullet overload.** A list where two sentences of prose would read better.
→ Quote the list and say how long it runs. Converting it restructures the
section, and in reference material it destroys the thing the page is for.

**Invented concept labels.** An abstract noun (paradox, trap, creep, divide,
gap, tax, flywheel) bolted onto a domain word and then used as though it named
something already known: "the supervision paradox," "workload creep."
→ Quote each one and say how many there are. A label that carries a real
distinction is worth keeping and worth defining; a label dressing up an ordinary
observation should go. Which one it is depends on what the writer meant by it.

**The dead metaphor.** One metaphor carried across the whole piece, five or ten
times over, long after it stopped explaining anything.
→ Count the appearances and quote two or three. Thinning it means deciding which
instances still carry the idea, and that is a reading of the argument, not a
cut.

---

## Substance

**The fix requires something only the writer has — a fact, or a reaction to
one.** Never fixed, in any mode, including Rewrite. Each finding becomes a
question to the writer.

Never invent a number, date, name, source, quote, outcome, or feeling to close
one of these gaps. Ask.

**Missing specifics.** "Improved performance significantly."
→ Ask: improved from what to what, measured how?

**Absent constraints.** Everything sounds unconstrained. No budget, deadline,
headcount, or legacy dependency anywhere.
→ Ask: what were you working against here?

**No failure stories.** Every outcome is a win. Nothing was tried that didn't
work.
→ Ask: what did you try first that didn't work?

**No timeline anchors.** Timeless language with no "during," "after," or "in Q3."
→ Ask: when was this, and what else was happening at the time?

**No named tools or competitors.** "Implemented automation." "Differentiated
against alternatives."
→ Ask: which tool, which competitor, by name?

**Unmeasured outcomes.** A result claimed with no number attached.
→ Ask: what was the number?

**Portability test.** A sentence that could move unchanged to another person,
company, product, or country.
→ Ask what makes this true of *this* subject specifically. If nothing does, the
sentence is filler and can be cut.

**Summary voice (missing lived detail).** Explaining from above rather than
narrating from inside. "Kubernetes improves deployment scalability" instead of
"we moved to Kubernetes after our deploy scripts stopped being maintainable."

This reads like a Voice problem, but nothing can be deleted to convert it.
Converting needs facts the draft does not contain: which scripts, when, what
broke.
→ Flag the sentence, say it is written from above, and ask what actually
happened. The replacement sentence is the writer's.

**Flat emotional range.** One temperature from the first paragraph to the last.
No irritation, enthusiasm, doubt, or humor anywhere.

This is the only finding that fires on the whole document rather than a quoted
line, so report it without a quote. Deletion cannot add variance, and composing
it means inventing the writer's feelings, which is a worse fabrication than
inventing a statistic.
→ Ask: which part of this actually annoyed you, or which part are you pleased
about? That is usually the paragraph worth writing yourself.
