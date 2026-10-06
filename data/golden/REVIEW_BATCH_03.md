# Review Batch 03 — Candidates for human review

**Status: FROZEN** (Batch 03). Not promoted to seed.jsonl / corpus.jsonl yet.

Annotation methodology locked (same as Batch 01 v6 / Batch 02).

## Methodology (frozen — same as Batch 01 v6 / Batch 02)
- Full judgment body text
- Gold = judgment_id + char_start/char_end
- Light cleaning only
- Scoring: overlap ≥100 chars OR ≥30% of span

## Counts: **14 queries**, **15 spans**, **7 judgments**
## Difficulty: {'medium': 7, 'easy': 3, 'hard': 4}

## Judgments (new vs Batch 01 + 02)

- `2023_1_463_472` — Anna Mathews v. Supreme Court of India — *constitutional / collegium (Art. 217)*
- `2023_8_1139_1148` — State of Gujarat v. Choodamani Parmeshwaran Iyer — *GST / criminal process*
- `2023_5_861_878` — Alpha G184 Owners Association v. Magnum International Trading Co. — *consumer protection*
- `2023_11_215_231` — Konkan Railway Corporation Ltd. v. Chenab Bridge Project Undertaking — *arbitration*
- `2023_2_958_964` — M/s Creative Garments Ltd. v. Kashiram Verma — *labour law*
- `2023_10_1184_1195` — Md. Asfak Alam v. State of Jharkhand — *criminal procedure / CrPC*
- `2023_5_682_700` — Indian Oil Corporation Ltd. v. M/s Sathyanarayana Service Station — *dealership / public law*

## Per-query spans

### q_col_01 [medium/constitutional] — 1 span(s)
Q: Can the Supreme Court, in judicial review under Article 32, examine the suitability or merit of a candidate recommended by the Collegium for elevation as a High Court judge?
- `2023_1_463_472` [14910:15479] The ratio of this judgment cannot be extended to apply the power of judicial review to examine the suitability or merit of a candidate. 12. We may als...

### q_col_02 [easy/constitutional] — 1 span(s)
Q: Is the legal position on the scope of judicial review over High Court appointments under Article 217 still open, or is it settled?
- `2023_1_463_472` [3315:3871] judges to the High Courts under Article 217 of the Constitution of India 1. 2. In our opinion, this legal issue is settled and is not res integra .  4...

### q_gst_01 [hard/tax] — 1 span(s)
Q: Does Section 41A(3) CrPC provide an absolute guarantee against arrest after compliance with appearance notices, and how does the language of Section 69(1) CGST Act differ?
- `2023_8_1139_1148` [16622:17347] But, it may be remembered that Section 41A(3) of Cr.P .C., does not provide an absolute irrevocable guarantee again st arrest. Despite the compliance ...

### q_gst_02 [medium/tax] — 1 span(s)
Q: How does the language of Section 41A(3) CrPC differ from Section 69(1) CGST Act regarding arrest after notice compliance?
- `2023_8_1139_1148` [16926:17347] stage, we may notice the difference in language bet ween Section 41A(3) of Cr.P .C. and 69(1) of CGST Act, 2017. Under Section 41A(3) of Cr.P .C., “re...

### q_con_01 [medium/civil] — 1 span(s)
Q: How is pecuniary jurisdiction determined for a joint consumer complaint filed by multiple allottees under the Consumer Protection Act?
- `2023_5_861_878` [31773:32345] 36. Admittedly, in the present cases, the value of the consideration paid by all the persons who have join ed as Complainants in the Joint Complaint, ...

### q_con_02 [easy/civil] — 1 span(s)
Q: Should consumer complaints be rejected on hyper-technical grounds relating to registration of the association when individual allottees have filed affidavits?
- `2023_5_861_878` [32737:33295] individual allottees. A pedantic and hyper-technica l approach would cause damage to the very concept of consumerism. We further note that even after ...

### q_arb_01 [medium/civil] — 1 span(s)
Q: What is the scope of interference by a court in an appeal under Section 37 of the Arbitration and Conciliation Act against an order under Section 34?
- `2023_11_215_231` [15876:16482] , is akin to the jurisdiction of the court under Section 34 of the Act. 8 Scope of interference by a court in an appeal under Section 37 of the Act, i...

### q_arb_02 [hard/civil] — 1 span(s)
Q: Can a court under Section 34/37 of the Arbitration Act reappreciate evidence and correct errors of fact in an arbitral award?
- `2023_11_215_231` [32754:33354] the “public policy” test to an arbitration award, it does not act as a court of appeal and consequently errors of fact cannot be corrected. A possible...

### q_lab_01 [easy/service] — 1 span(s)
Q: What direction has the Supreme Court given regarding permanent addresses of parties in labour law disputes?
- `2023_2_958_964` [10093:10623] In future all the cases to be filed and in all the pending cases, the parties shall be required to furnish their permanent address(es). Even if the re...

### q_lab_02 [medium/service] — 2 span(s)
Q: Why did the Supreme Court emphasise permanent addresses in labour dispute cases?
- `2023_2_958_964` [4712:5226] corrective steps. 12. It is a case in which permanent address of the workman ha s not been mentioned. The address furnished is care of Union. All effo...
- `2023_2_958_964` [10079:10507] disputes. 23. In future all the cases to be filed and in all the pending cases, the parties shall be required to furnish their permanent address(es). ...

### q_crpc_01 [medium/criminal] — 1 span(s)
Q: What directions did the Supreme Court issue to High Courts regarding pre-arrest bail and related criminal process?
- `2023_10_1184_1195` [20970:21540] to seven years, whether with or without fine.” II. The High Court shall frame the above directions in the form of notifications and guidelines to be f...

### q_crpc_02 [hard/criminal] — 1 span(s)
Q: After the charge-sheet is filed, how should a court approach an anticipatory bail plea where the accused cooperated with investigation and no exceptional facts disentitling bail are shown?
- `2023_10_1184_1195` [16005:16850] compulsion on the officer to arrest the accused.” 12. In the present case, this Court is of the opinion that there are no startling features or elemen...

### q_dlr_01 [hard/civil] — 1 span(s)
Q: Can a High Court under Section 37 of the Arbitration Act interfere with the arbitrator's finding that was upheld under Section 34, and then order restoration of a dealership?
- `2023_5_682_700` [26862:27530] of the view that the High Court in a proceeding under Section 37 of the Act acted illegally in interfering with the finding of the Arbitrator and what...

### q_dlr_02 [medium/civil] — 1 span(s)
Q: After setting aside an arbitral award under Section 37, may the High Court itself order restoration of a petroleum dealership and leave open a claim for damages?
- `2023_5_682_700` [27252:27846] The High Court also erred in proceeding to order restoration of the dealership to the first respondent after setting aside the award and going further...

## Files
- review_batch_03_queries.jsonl
- review_batch_03_judgments.jsonl
- seed/corpus: **untouched**

---
**v1 FROZEN GOLDEN SET** — promoted 2026-10-05. Do not edit labels.
