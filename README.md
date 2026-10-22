# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts posts from **r/Arkansas** that carry the **News** flair. Almost
every one of these posts is a link to a local news story plus its headline. The
classifier reads the headline and places it in one of four labels:
`crime_court` (crimes, suspected crimes, arrests, sentencings, lawsuits,
rulings), `politics_elections` (candidates, campaigns, voting, and politicians
acting as political figures), `debates_opinions` (people arguing, opposing,
urging, or still discussing an issue with no decision yet), or `announcements`
(decisions and all other news from institutions, businesses, and
communities). The goal is to let a reader of the subreddit
filter the feed by the kind of story they want.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `crime_court`

**Definition:** (crime **or** court; a post needs only one of the two) A post whose main subject is a criminal incident, a legal action, or a court acting as a court, such as a crime, arrest, charge, sentencing, lawsuit, settlement, appeal, or court ruling (civil and constitutional cases included).

**Example 1:**
> Former Garland County chief public defender arrested again on felony drug charges

**Example 2:**
> Arkansas one of 8 states suing OpenAI over ChatGPT risks to children

### `politics_elections`

**Definition:** A post whose main subject is elected officials, candidates, campaigns, or voting: what they say or do, or how a race is going.

**Example 1:**
> Little Rock mayoral candidates share stances on crime, growth ahead of November midterms

**Example 2:**
> Debate in Arkansas' US Senate race won't take place, Cotton and Shoffner campaigns say

### `debates_opinions`

**Definition:** A post whose main news is people arguing, opposing, urging, raising concerns, reacting, or still discussing an issue, with no decision made yet, and not tied to an election, a crime, or a court.

**Example 1:**
> Residents in Arkansas, Missouri unite against proposed Oregon County data center

**Example 2:**
> Arkansas lawmakers weigh prison expansion versus reforms at second capacity hearing

### `announcements`

**Definition:** A post reporting news from an institution, business, or community (a decision, opening, report, award, warning, or event) whose main subject is not crime, courts, politics, or an ongoing debate.

**Example 1:**
> Hugo's of Fayetteville among nine restaurants named finalists for Arkansas Food Hall of Fame

**Example 2:**
> Mountain Valley Spring Water opens new manufacturing facility in Hot Springs

### Order I check labels in

1. Crime or court (including suspected or possible crime) → `crime_court`
2. Election, candidate, campaign, or a politician acting politically → `politics_elections`
3. People arguing, opposing, urging, reacting, or still discussing, no decision yet → `debates_opinions`
4. A decision made, or anything else → `announcements`

### The hardest boundary

**Which two labels:** `politics_elections` vs. `announcements`

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If the post centers on an election, a candidate, a campaign, voting, or a
politician acting as a political figure (a statement, a visit, an accusation),
it is `politics_elections`. If it centers on the outcome of a government
decision (a vote, a contract, a closure, a policy), it is `announcements`, even
when elected officials made that decision.

*Example:* "Little Rock School Board votes 4-2 to close three elementary
schools" is `announcements`: the news is the closure, not the board members.
"Senator Cotton and labor secretary visit Russellville to discuss disability
employment and inflation" is `politics_elections`: the news is a politician
appearing as a political figure.

**Secondary rules (found by stress-testing):**

- **Candidates and crime:** A post about *candidates* for a judge or prosecutor
  seat, or candidates talking *about* crime, is `politics_elections`. But if a
  candidate or politician is themselves arrested, charged, sued, or sentenced,
  the legal event wins and the post is `crime_court`.
- **Courts:** Any post where a court or judge acts (a ruling, appeal, lawsuit,
  hearing, or a court's own request) is `crime_court`, even when nobody is
  accused of a crime. Exception: in Arkansas a *county judge* is an elected
  executive office, not a court, so county-judge candidates and a county
  judge's veto are labeled by topic (`politics_elections` or
  `announcements`).
- **Protests and rallies:** Demonstrations, rallies, and public pushback are
  `debates_opinions`, unless they are organized by a campaign or candidate.
- **Discussing vs. deciding:** If a board or lawmakers *voted, approved, or
  passed* something, it is `announcements`. If they are still *considering,
  discussing, exploring, or weighing* it, it is `debates_opinions`.
- **Warnings about crime:** A police or official warning about a crime or
  scam (e.g. "Conway police warn residents about phone scam") is
  `crime_court`. The crime decides the label, not the fact that it was
  announced. Other warnings (weather, wildfire, illness) stay
  `announcements`.
- **Responses:** When an institution, official, advocate, or ordinary person
  responds or reacts to something, they are stating a view, so it is
  `debates_opinions`. When a *politician or candidate* responds, it stays
  `politics_elections`.
- **Suspected or possible crime:** Anything that is, is suspected to be, or
  could become a crime is `crime_court`: accusations, allegations, suspects,
  possible future charges, even a centuries-old suspected murder. This holds
  even when the headline is about a debate or audit *of* those allegations.
- **Crime as background (narrow exception):** If the headline's news is a
  person surviving or helping after a crime (e.g. a survivor helping victims),
  label the human story, `announcements`. Institutional *responses* follow the
  Responses rule above.

### A label I dropped, then brought back

I started with a fourth label, `opinions_debates`, meant for posts *expressing*
a strong view. In my first 28 posts only one ("Why I don't feel sorry for
Arkansas farmers", an op-ed headline) fit, about 4%, so I dropped it and kept
three topic labels. I also merged crime and court into one label, since most
court news here is the second half of a crime story.

While checking the full 207 posts I noticed a group my three labels handled
badly: headlines where the news is people *arguing about* something (boards
still discussing, residents opposing, advocates urging, someone reacting),
not a decision. These were all landing in `announcements`, which hid them and
pushed that label to 61%. I brought the label back as `debates_opinions`,
defined by "no decision yet" instead of "opinion piece". It now covers 23 posts
(11%). Two of my 20 cold labels were made before this change; I relabelled
them and recorded the original label in the note column.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/Arkansas (public subreddit), posts with the **News** flair only. Each post is a headline plus a link to a local outlet (Arkansas Democrat-Gazette, Arkansas Times, Arkansas Advocate, KATV, KARK, THV11, 5NEWS, 4029, NWA Homepage). The model sees the headline text only, usually 10–20 words per post.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

I collected 207 News-flaired headlines (about Sept 26 – Oct 17, 2026) by
screenshotting and copying the subreddit feed, and dropped near-duplicate
stories (the same event posted twice from different outlets) so they can't
leak across the train/test split. I labelled **20 posts cold first** (marked
`cold`), using only my written definitions. Claude then **pre-labelled the
other 187** from those definitions (marked `pre-labelled`), flagging 25 it was
unsure about. I read and corrected them: 32 were changed (`pre-labelled,
corrected`), the rest kept (`pre-labelled, checked`). While correcting, I added
the fourth label `debates_opinions` and several decision rules (courts,
suspected crime, responses, discussing vs. deciding). Two cold labels were
relabelled after that change; their note column records the original label.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `announcements` | 105 | 51% |
| `crime_court` | 44 | 21% |
| `politics_elections` | 34 | 16% |
| `debates_opinions` | 24 | 12% |
| **Total** | 207 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* Arkansas man survives Saudi Arabia airport attack, helps wounded victims in aftermath
>
> *Could have been:* `crime_court` or `announcements`
>
> *I chose `announcements`, because:* the attack is only the background. The headline's news is a person surviving and helping victims, so it ends as a human story, not a crime story.

**2.**
> *The post:* Lonoke County will choose new sheriff after candidate's murder case drew national attention
>
> *Could have been:* `politics_elections`, `crime_court`, or `announcements`
>
> *I chose `announcements`, because:* the news is that the county is going to choose a new sheriff. There are no candidates or campaign in the headline yet, and the murder case is background. This one sits right on my hardest boundary.

**3.**
> *The post:* West Memphis mayor says Google data center could generate $20 million in new annual tax revenue for city
>
> *Could have been:* `politics_elections` or `debates_opinions`
>
> *I chose `debates_opinions`, because:* "says … could" is a prediction and a view, not a decision, and he is speaking about economic development, not acting as a candidate.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on an Apple Silicon GPU (`mps`), 8 GB RAM.

**Anything I changed from the defaults, and why:** Nothing. I kept every
default. My headlines are 10–20 words, far under the 128-token limit, so there
was no reason to change `MAX_LENGTH`.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

train 144 · val 31 · test 32

| Label | Train | Val | Test |
|---|---|---|---|
| `crime_court` | 30 | 7 | 7 |
| `politics_elections` | 24 | 5 | 5 |
| `debates_opinions` | 17 | 3 | 4 |
| `announcements` | 73 | 16 | 16 |

Three of my four labels have fewer than 8 test examples: `crime_court` (7),
`politics_elections` (5), and `debates_opinions` (4). With only 4 test posts,
one wrong prediction moves `debates_opinions`' F1 by a large amount, so I
expect its score to swing between seeds next unit. That is a property of the
data size, not necessarily of the model.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: stress-testing my labels**

- *What I asked for:* I gave Claude my three label definitions and asked it to write 8 made-up r/Arkansas headlines that sit on the boundaries between them.
- *What came back:* 8 headlines like "Arkansas Supreme Court rules medical marijuana expansion can appear on November ballot" and "Attorney General Griffin announces settlement with Walmart over opioid distribution." I labelled them myself without help. I placed only 3 cleanly; on 2 my answer contradicted my own written definition, and 3 weren't covered by any rule.
- *What I changed:* I added four decision rules: a candidate charged with a crime is `crime_court`, protests and rallies have a fixed label, police warnings about a crime are `crime_court`, and how to handle court rulings with no wrongdoer. (I later replaced that last one with a simpler rule: any court acting as a court is `crime_court`.)

**Moment 2: correcting the AI pre-labels**

- *What I asked for:* After labelling 20 posts cold, I asked Claude to pre-label the other 187 using my definitions and to flag the ones it was unsure about.
- *What came back:* Labels for all 187, with 25 flagged as unsure. Pre-labelled, `announcements` was 64% of the data, above my own 60% target.
- *What I changed:* I went through the labels and changed 32. Several corrections became new rules: "suspected or possible crime is `crime_court`," "any court acting as a court is `crime_court`," and "a person surviving or helping after a crime is the human story, not the crime." The biggest change came from noticing that headlines about people still *discussing* or *opposing* something (boards considering, residents uniting against, advocates urging) didn't fit `announcements`. I added a fourth label, `debates_opinions`, for them. That brought `announcements` down to 51%.

**Pre-labelling disclosure:**

The first 20 rows I labelled cold, by myself, using only my written
definitions (note column: `cold`). The remaining 187 rows were pre-labelled by
Claude from my definitions and then read and corrected by me (note column:
`pre-labelled, checked` if I kept the label, `pre-labelled, corrected` if I
changed it). Two cold rows were relabelled after I added `debates_opinions`;
their note column records the original label. Claude also helped me
transcribe headlines from my screenshots into `labels.csv` and removed
near-duplicate stories.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Same 32 held-out posts (`test_split.csv`, seed 42). Baseline:
`facebook/bart-large-mnli`, zero-shot, using my label definitions. Trained:
`distilbert-base-uncased`, fine-tuned on 144 posts.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.219 | 0.500 | +0.281 |
| Macro F1 | 0.090 | 0.167 | +0.077 |
| F1 — `announcements` | 0.000 | 0.667 | +0.667 |
| F1 — `crime_court` | 0.359 | 0.000 | −0.359 |
| F1 — `politics_elections` | 0.000 | 0.000 | 0.000 |
| F1 — `debates_opinions` | 0.000 | 0.000 | 0.000 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

My trained model will beat the baseline on `announcements`, because half of
my training examples (73 of 144) were announcements, while the baseline scored
an F1 of 0 on that label.

*Honest note:* I had already seen my trained model's overall accuracy (0.50)
and macro F1 (0.167) before writing this, but not its per-label scores, so I
made the prediction per label.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

My prediction was right, but for a bad reason. Both models gave the **same
answer to every post**: the baseline called all 32 posts `crime_court` (recall
1.0, precision 0.22), and my trained model called all 32 `announcements`
(recall 1.0, precision 0.50). Neither one learned to tell my four labels apart.
The trained model "wins" on accuracy only because `announcements` is the
biggest label (16 of 32 test posts), so always guessing it scores 0.50. That's
the same score as a model that never read a single headline. My fine-tuning
added nothing beyond learning which label is most common.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

Device: Apple Silicon GPU (`mps`), torch 2.14.1, `distilbert-base-uncased`,
3 epochs, lr 2e-5, batch 16, max length 128. File:
`results_three_seeds_before.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.85 | 0.500 | 0.500 | 0.500 | MISSED |
| 2. `debates_opinions` F1 | ≥ 0.60 | 0.000 | 0.000 | 0.000 | MISSED |
| 3. Biggest label share in `labels.csv` | ≤ 60% | 51% | 51% | 51% | MET |
| 4. Agreement with staff on 30 posts | ≥ 24/30 | (Milestone 3) | | | |
| 5. Accuracy of predictions with confidence ≥ 0.80 | ≥ 90% | see note | see note | see note | |

All three seeds gave the identical result: accuracy 0.500, macro F1 0.167,
and every test post predicted `announcements`. The spread across seeds is 0
points, but only because the model gives the same answer no matter which posts
it sees. Criterion 3 depends only on the labelled file, so it is the same for
every seed.

*Note on criterion 5:* the model is never confident. Its average top-label
confidence was about 0.43 on every seed (0.39–0.45), so few or no predictions
reach 0.80. The notebook's closest measure, accuracy on the most-confident
third of posts, was 0.80 / 0.60 / 0.70.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42 (seeds 7 and 2024 are identical).

| true \ predicted | crime_court | politics_elections | debates_opinions | announcements |
|---|---|---|---|---|
| **crime_court** | 0 | 0 | 0 | 7 |
| **politics_elections** | 0 | 0 | 0 | 5 |
| **debates_opinions** | 0 | 0 | 0 | 4 |
| **announcements** | 0 | 0 | 0 | 16 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

All 7 real `crime_court` posts were called `announcements`, and nothing went
the other way. The whole predicted column is `announcements`: the model didn't
learn any boundary at all. It collapsed onto my biggest label (51% of the
data) for all 16 non-announcement posts.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
