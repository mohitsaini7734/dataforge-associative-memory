# Associative Memory & Fast Weights — Interactive Explainer
**DataForge 2026 · Pathway Track submission**

## One-sentence claim (falsifiable)
A fixed-size associative memory can store many key→value pairs using simple additive
(Hebbian) writes and correctly retrieve them from noisy cues — but because every pair
shares the *same* memory, packing in more pairs raises cross-talk interference, and
retrieval accuracy degrades smoothly and predictably as a continuous function of how
many pairs share the memory (not as a sudden collapse at a fixed capacity — this demo
uses a single-shot readout, not iterative Hopfield dynamics, and the two have different
failure shapes; see "Verification notes" below).

**60-second reproducible test:** open the artifact, leave noise at 0%, and drag N from 1
to 40. Bit-level retrieval accuracy on the tracked probe should decline smoothly and
continuously the whole way — roughly 100% near N=1 down to roughly 90% by N=40, for
d=64 — with no sudden knee or wall at any specific N. If instead you see a flat plateau
followed by a sharp cliff, or no change at all, the claim as implemented here is
falsified — try it and see.

## Intended learner, prerequisites, learning objectives
- **Audience:** undergraduate/graduate CS or ML students, or engineers, who know what a
  vector and a matrix-vector product are, and have a rough sense of what attention does
  in a Transformer. No prior knowledge of Hopfield networks or BDH is assumed.
- **Prerequisites:** basic linear algebra (dot product, matrix-vector multiply);
  familiarity with the general idea of a Transformer's key/value attention (helpful, not required).
- **Learning objectives** — by the end, a learner should be able to:
  1. Explain, in their own words, how an outer-product (Hebbian) associative memory writes and retrieves patterns.
  2. Predict — before running the demo — what happens to retrieval accuracy as more patterns are stored in a fixed-size memory, and verify the prediction empirically.
  3. Distinguish this toy mechanism from BDH's synaptic memory and from BDH-CQ's recurrent contextual memory, and state one concrete way each differs from the toy model.
  4. Name at least one open limitation/misconception (e.g., "the memory doesn't reject new writes when full — it silently degrades everything already stored").

## What's in this submission package
| File | Role |
|---|---|
| `associative_memory_explainer.html` | The interactive artifact — a single self-contained HTML/CSS/JS file, zero external dependencies, zero build step. This is the "public artifact" — open it directly in any browser, or host it as a static page (e.g. GitHub Pages) for a public URL. |
| `one_page_concept_summary.pdf` | Required one-page concept summary (single page, ~800 words). |
| `make_summary_pdf.py` | Script that generates the PDF summary (Python + reportlab). Included so the summary is reproducible from source, not a hand-tweaked PDF. |
| `README.md` | This file. |

## Architecture of the artifact — what's live, precomputed, synthetic, or animated
**Everything in the interactive artifact is live, client-side computation, generated on
the learner's own machine. There is no precomputed, cached, or animated content, and
nothing is faked:**
- On every slider move, real vectors are freshly generated in the browser (uniform random
  bipolar, not fixed/seeded to a hidden answer), a real 64×64 weight matrix is built via
  the additive Hebbian rule, and retrieval is computed via an actual matrix-vector product
  in JavaScript, in front of the learner.
- The **theoretical estimate** curve (orange) is a closed-form statistical approximation —
  a classical Hopfield-style single-shot error bound, `Φ(√(d/(N−1)))` — computed live from
  the same `d` and `N` the learner has chosen. It is not a lookup table or a fitted curve.
- The **empirical curve** (green) is computed by literally rebuilding the memory and
  running retrieval trials for every value of N from 1 to 40, every time the noise slider
  changes. This is a genuine (if small, ~6–20 trial) Monte Carlo simulation, not an
  animation or interpolation between two hand-picked points.
- The **heatmap** of the weight matrix `W` is a direct pixel-per-cell rendering of the live
  matrix values (not a stock illustration), so a learner can visually watch it get "noisier"
  as N increases — that visual noise *is* the interference the claim is about.
- The **bit-rows** (stored key, noisy cue, true value, retrieved value) are rendered from
  the same live arrays used for the accuracy statistic directly above them, with mismatches
  highlighted in red, so the single number (accuracy %) and the raw evidence for it are both
  visible at once ("truth beside estimate").

**Manipulable variables:** number of stored patterns (N, 1–40), cue noise (0–50% of bits
flipped), and a "resample" action that redraws new random key/value patterns without
changing N or noise (useful for checking the result isn't a fluke of one random draw).

**Role of the BDH module:** a dedicated, non-decorative section (not tacked onto the end)
ties the toy mechanism to BDH's Hebbian synaptic memory (sparse ~5% active-neuron activity,
reported monosemantic synapses) and to BDH-CQ's recurrent contextual memory (explicitly
described in its own paper as related to fast-weight and linear-attention views of
association, with a special additive-per-demonstration case). The section states plainly,
in the artifact itself, that the toy is *not* an implementation of either system — see
Limitations below.

## How to reproduce / run
No installation needed for the artifact itself:
```bash
open associative_memory_explainer.html   # or double-click the file, or host it as a static page
```
To regenerate the PDF summary from source:
```bash
pip install reportlab --break-system-packages
python3 make_summary_pdf.py
```
Both steps were verified to run cleanly (one page, correct rendering) at submission time.

## Primary sources (2022–2026 papers, cited beside the technical claims they support)
1. Kosowski, A., Uznanski, P., Chorowski, J., Stamirowska, Z., Bartoszkiewicz, M.
   *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain.*
   arXiv:2509.26507, 2025. — source for BDH's sparse/Hebbian/monosemantic-synapse claims.
2. Engdahl, B., Kosowski, A., Chorowski, J., Stamirowska, Z. et al.
   *BDH-CQ: In-Context Learning with Recurrent Latent Reasoning.* arXiv:2608.09888, 2026. —
   source for BDH-CQ's recurrent-contextual-memory / fast-weight framing and its ARC-AGI-1 result.
3. Behrouz, A., Zhong, P., & Mirrokni, V. *Titans: Learning to Memorize at Test Time.*
   arXiv:2501.00663, 2024. — independent (Google Research) 2024 paper that explicitly frames
   Transformer key/value pairs as an associative memory block, used as third-party corroboration
   that the accumulate-and-interfere framing taught here is active in current research, not just
   inside Pathway's own papers.

**Foundational background** (pre-2022, cited for contrast/mechanism only, not counted toward
the "2022–2026" recency requirement): Schlag, Irie & Schmidhuber, *Linear Transformers Are
Secretly Fast Weight Programmers*, ICML 2021; Vaswani et al., *Attention Is All You Need*,
NeurIPS 2017.

## Verification notes (fact-checking done before submission)
- The BDH "97.4% on Sudoku Extreme" figure and its caveat ("refers to Pathway's internal
  implementation, not reproduced by the public repo out of the box") were checked directly
  against the `pathwaycom/bdh` GitHub README at submission time, not taken from a secondary
  summary.
- The BDH-CQ "29.5% pass@2 at $0.00070/task" figure was checked directly against the
  arXiv:2608.09888 abstract/PDF.
- An earlier draft of this summary included a claim about an "independent black-box audit"
  of the BDH-CQ result. On verification, this claim could not be located in any primary
  source (arXiv paper, official GitHub repo, or Hugging Face paper page) — it traced back to
  a single low-quality news aggregator that also contained other unverifiable claims. It has
  been **removed** from both the artifact and the one-page summary; the current text
  correctly labels the BDH-CQ result as developer-reported and not independently audited as
  of this writing. This correction is disclosed here in the interest of the "no overclaiming"
  and "verify against primary sources" rules.

## Limitations & honesty disclosures
- The interactive demo is a **classical outer-product associative memory** (a Hopfield-style
  toy), independently implemented for teaching purposes. It is **not** BDH, **not** BDH-CQ,
  and does not reproduce any published BDH/BDH-CQ number. Stated explicitly inside the
  artifact itself, not just here.
- The theoretical curve assumes random, uncorrelated bipolar patterns and a single retrieval
  pass (no iterative clean-up) — the standard simplifying assumption for this class of
  capacity estimate. Real BDH memory is sparse, non-negative, and graph-structured, so its
  quantitative capacity/interference curve will differ from this toy's, even though the
  qualitative accumulate-and-interfere mechanic is shared.
- BDH's 97.4% and BDH-CQ's 29.5% figures are both **developer-reported benchmark results**,
  not independent third-party evaluations or deployments (see Evidence, labeled in the
  one-page summary for the full breakdown, including what a genuine partnership/deployment
  claim looks like by contrast).
- BDH-CQ's paper reports pretraining-scaling behaviour from 1B to 600B parameters but does
  **not** provide a matching ARC-style reasoning-accuracy scaling curve — so this submission
  does not claim the 150M-parameter reasoning result will hold at larger scale.

## AI assistance disclosure
This submission (interactive artifact, README, and one-page concept summary) was built with
AI assistance (Claude). All technical claims were checked against the primary arXiv papers
and the official Pathway/BDH GitHub repository listed above rather than taken from memory or
from secondary summaries — including one correction made after an initial secondary-source
claim failed verification (see "Verification notes" above). The team submitting this project
is responsible for understanding, defending, and being able to modify every part of it.

## Source, data, and license record
- **Code:** 100% original vanilla HTML/CSS/JavaScript for the artifact, and original Python
  (using the `reportlab` library, BSD license) for the PDF generator. No third-party code,
  UI kits, or component libraries are used or bundled.
- **Data:** all patterns/vectors used in the demo are generated live in-browser at random;
  no external dataset is used or required.
- **Graphics/fonts:** none — the artifact uses only system fonts and canvas-drawn shapes, no
  bundled fonts, icons, or images.
- **Reused components:** none.
