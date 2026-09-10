from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleSmall', fontSize=14, leading=16.5, spaceAfter=3, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='SubHead', fontSize=9.5, leading=11.5, spaceBefore=5, spaceAfter=2, fontName='Helvetica-Bold', textColor=colors.HexColor('#2b3a67')))
styles.add(ParagraphStyle(name='BodyJustify', fontSize=8.3, leading=10.5, spaceAfter=3, alignment=TA_JUSTIFY, fontName='Helvetica'))
styles.add(ParagraphStyle(name='Small', fontSize=7.3, leading=9.2, textColor=colors.HexColor('#555555')))

doc = SimpleDocTemplate("/home/claude/one_page_concept_summary.pdf", pagesize=LETTER,
                         topMargin=0.4*inch, bottomMargin=0.35*inch, leftMargin=0.55*inch, rightMargin=0.55*inch)

story = []

story.append(Paragraph("Associative Memory and Fast Weights: From Hebbian Writes to BDH's Synaptic State", styles['TitleSmall']))
story.append(Paragraph("DataForge 2026 · Pathway Track — One-Page Concept Summary", styles['Small']))
story.append(Spacer(1, 4))

story.append(Paragraph("The mechanism and why it matters now", styles['SubHead']))
story.append(Paragraph(
"A standard Transformer answers 'what is relevant to this token?' by comparing it against every previous token "
"through dot-product attention, which requires storing and re-scanning a growing key-value (KV) cache "
"(Vaswani et al., 2017). An associative memory answers a related but cheaper question: 'given this cue, what value "
"was bound to it earlier?' — without re-comparing against every past token. The classical mechanism is additive "
"(Hebbian) writing: a matrix W accumulates outer products of key and value vectors, W += v&#8226;k<super>T</super>, and a cue "
"retrieves an answer through a single matrix-vector product, v' = W·k (Schmidhuber, 1992; Schlag et al., 2021, who "
"showed linear-attention Transformers are equivalent to fast-weight programmers). This matters now because "
"reasoning systems increasingly need context that grows without bound, and a fixed-size associative state is the "
"common thread linking linear attention, state-space models, and Pathway's Dragon Hatchling (BDH) family — all of "
"which trade an ever-growing cache for a compact, continuously overwritten memory.", styles['BodyJustify']))

story.append(Paragraph("What changes technically, and the trade-off", styles['SubHead']))
story.append(Paragraph(
"Replacing a growing KV cache with a fixed-size additive memory changes cost from linear-in-context to constant "
"per step, but it introduces cross-talk: every new key-value pair is superimposed on the same weights as every "
"earlier pair, so retrieval accuracy is a function of how many associations share that memory, not how much "
"memory exists in isolation. For random, uncorrelated bipolar patterns, single-shot retrieval error grows "
"predictably with the number of stored pairs relative to the memory's dimension (a classical Hopfield-style "
"result). The practical trade-off is therefore capacity versus interference, not capacity versus size: doubling "
"the memory's dimension helps far more than adding cleverness to the write rule.", styles['BodyJustify']))

story.append(Paragraph("Representative systems compared", styles['SubHead']))
cell = ParagraphStyle(name='Cell', fontSize=7.2, leading=8.8, fontName='Helvetica')
cellHead = ParagraphStyle(name='CellHead', fontSize=7.4, leading=9, fontName='Helvetica-Bold', textColor=colors.white)
def P(t, s=cell): return Paragraph(t, s)
data = [
    [P("System", cellHead), P("Memory mechanism", cellHead), P("Cost per step", cellHead), P("Interpretability", cellHead)],
    [P("Transformer (KV cache)"), P("Explicit growing cache, exact recall"), P("Grows with context length"), P("High (attention weights)")],
    [P("Linear attention / fast weights"), P("Fixed-size matrix, additive updates"), P("Constant"), P("Moderate")],
    [P("BDH (Pathway)"), P("Sparse, Hebbian synaptic memory over a neuron graph"), P("Constant, GPU-friendly"), P("High (reported monosemantic synapses)")],
    [P("BDH-CQ (Pathway)"), P("Recurrent contextual memory + iterative latent reasoning"), P("Constant + latent-step compute"), P("Emerging (studied via controlled interventions)")],
]
t = Table(data, colWidths=[1.15*inch, 2.15*inch, 1.15*inch, 1.55*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2b3a67')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 7.2),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f4f5fa')]),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(Spacer(1, 3))

story.append(Paragraph("Where BDH and BDH-CQ fit", styles['SubHead']))
story.append(Paragraph(
"BDH implements the accumulate-and-interfere principle at the level of individual synapses rather than one "
"global matrix: attention emerges from local, graph-based neuron interactions, roughly 5% of neurons are reported "
"active at any moment (sparse, non-negative activity), and synapses are reported to respond to recognisable "
"semantic concepts (Kosowski et al., 2025). BDH-CQ, built on the same family, makes the fast-weight connection "
"explicit for in-context learning: as demonstrations are ingested, they continuously update a recurrent "
"contextual memory while the model's trained parameters stay fixed, and the paper explicitly relates this state "
"to attention, fast-weight memory, and linear-attention views of association, including a special case where "
"state accumulates additively per demonstration (Engdahl, Kosowski, Chorowski, Stamirowska et al., 2026). The two "
"systems play different roles: BDH is the base architecture demonstrating the mechanism at inference-independent, "
"trained-weight scale; BDH-CQ is a downstream reasoning system that exploits the same substrate for test-time "
"contextual adaptation without gradient updates.", styles['BodyJustify']))

story.append(Paragraph("Evidence, labeled", styles['SubHead']))
story.append(Paragraph(
"BDH's headline evidence is a benchmark result, not an independent reproduction or deployment: Pathway reports "
"97.4% accuracy on ~250,000 Sudoku Extreme puzzles without chain-of-thought, though this figure refers to "
"Pathway's internal implementation and is not reproduced by the public GitHub baseline out of the box (Pathway, "
"pathwaycom/bdh repository, checked at submission time). BDH-CQ's headline result is likewise developer-reported, "
"not independently audited as of this writing: 29.5% pass@2 on ARC-AGI-1 at an estimated $0.0007 per task with a "
"150M-parameter model, framed by the authors as a new cost-accuracy Pareto point rather than a state-of-the-art "
"accuracy claim (Engdahl et al., 2026). For contrast, Google Research's Titans explicitly frames Transformer "
"key-value pairs as an associative memory block and adds a gradient-based, test-time-updated neural memory on top "
"— a third-party 2024 result corroborating the same accumulate-and-interfere framing on different benchmarks "
"(Behrouz, Zhong &amp; Mirrokni, 2024). Pathway has also announced commercial BDH integration with AWS/NVIDIA — a "
"partnership/deployment claim, not a benchmark or academic reproduction.",
styles['BodyJustify']))

story.append(Paragraph("Most important limitation", styles['SubHead']))
story.append(Paragraph(
"The clearest gap is scale evidence for reasoning capability: BDH-CQ's paper reports pretraining-scaling behaviour "
"from 1B to 600B parameters but does not provide a corresponding ARC-style reasoning-accuracy scaling curve, so it "
"is unclear whether latent-reasoning gains observed at 150M parameters persist, saturate, or reverse at larger "
"scale (Engdahl et al., 2026, reviewer discussion on Hugging Face paper page). A second open question is mechanistic: "
"whether demonstration ingestion in BDH-CQ constitutes true weight-free online learning or forward-only "
"conditioning is explicitly left ambiguous in the paper's own language. Readers who want to continue past this "
"summary should start from the primary arXiv papers below rather than secondary coverage.", styles['BodyJustify']))

story.append(Paragraph(
"Primary sources (2022-2026): Kosowski, Uznanski, Chorowski, Stamirowska, Bartoszkiewicz, <i>The Dragon Hatchling</i>, "
"arXiv:2509.26507 (2025) · Engdahl, Kosowski, Chorowski, Stamirowska et al., <i>BDH-CQ: In-Context Learning with "
"Recurrent Latent Reasoning</i>, arXiv:2608.09888 (2026) · Behrouz, Zhong &amp; Mirrokni, <i>Titans: Learning to "
"Memorize at Test Time</i>, arXiv:2501.00663 (2024). Foundational background (pre-2022, cited for contrast, not "
"counted toward the recency requirement): Schlag, Irie &amp; Schmidhuber, <i>Linear Transformers Are Secretly Fast "
"Weight Programmers</i>, ICML 2021 · Vaswani et al., <i>Attention Is All You Need</i>, NeurIPS 2017.", styles['Small']))

doc.build(story)
print("done")
