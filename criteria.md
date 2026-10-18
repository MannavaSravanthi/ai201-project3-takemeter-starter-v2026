# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.85

On the held-out test split, overall accuracy is **at least 0.85** on every one
of the three seeds (42, 7, 2024).

**Why this target:** My labels are about *topic*, not tone, and topic in a news
headline usually shows up in strong keywords: "sentenced", "arrested",
"charged" for `crime_court`, and "candidate", "campaign", "voters" for
`politics_elections`. Guessing at random among my four labels gets about 25%,
and always guessing `announcements` (my biggest label) gets about 51%. A useful feed filter has
to beat that by a wide margin, so I set the bar high on purpose.

---

## 2. `debates_opinions` has an F1 of at least 0.60

On the held-out test split, the F1 score for `debates_opinions` is **at
least 0.60** on every one of the three seeds.

**Why this target:** `debates_opinions` is my smallest label: 23 of 207 posts
(11%), so only about 3–4 posts land in the test split, and one mistake moves
the F1 a lot. That's why this target is looser than my overall accuracy
target. It is also my newest and fuzziest label (I added it after labelling
had started), and its boundary with `announcements` ("still discussing" vs.
"decided") depends on single words like "consider" or "approve". I kept 0.60
rather than going lower because those cue words ("urge", "oppose", "weigh",
"concerns") are fairly distinctive.

> *Note: before any training, this criterion named `crime_court`, which was
> my smallest label until I added `debates_opinions`. The number (0.60) is
> unchanged.*

---

## 3. No label covers more than 60% of labels.csv

In the final `labels.csv`, the biggest label (expected to be
`announcements`) is **at most 60%** of all rows, checked by counting the label
column.

**Why this target:** `announcements` is my catch-all label, so it naturally
grows the fastest. In my first 28 posts it was already about 50%, and in my
first full labelling pass it reached 61%. The
assignment's hard limit is 70%, but at 70% a model could score well just by
guessing `announcements`. Holding it to 60% forces me to go and collect more
`crime_court` and `politics_elections` posts.

---

## 4. I agree with staff on at least 24 of the 30 reference posts

When I label the 30-post staff reference set in Unit 6 (using the staff
taxonomy), my labels match the staff labels on **at least 24 of 30 posts
(80%)**, as reported by `agreement.py`.

**Why this target:** The staff set includes posts chosen because they are
ambiguous, so 100% isn't realistic. My own stress test showed I can be
inconsistent on borderline posts: on 8 boundary headlines, I gave 2 labels
that contradicted my own written definitions. 80% leaves room for about 6
genuinely hard posts, but still catches it if I'm applying rules loosely.

---

## 5. Confident predictions are right at least 90% of the time

On the held-out test split, of all predictions where the model's top-label
probability is **0.80 or higher**, **at least 90%** are correct, on every one
of the three seeds.

**Why this target:** If someone used TakeMeter to filter the r/Arkansas feed,
the confident predictions are the ones they would trust without checking. A
filter that is "sure" but wrong 1 time in 5 would put sentencing news into the
politics feed. I expect most uncertainty to sit on my hard boundaries (court
rulings, candidates and crime), so the confident predictions should mostly be
the easy keyword cases, and those should be right almost every time.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
