# Review Batch 02 — Candidates for human review

**Status: FROZEN** (Batch 02 v2). Not promoted to seed.jsonl / corpus.jsonl yet.

Annotation methodology locked (same as Batch 01 v6).

## Methodology (frozen from Batch 01 v6)
- Full judgment body text
- Gold = judgment_id + char_start/char_end
- Light cleaning only
- Scoring: overlap ≥100 chars OR ≥30% of span

## Counts: **15 queries**, **16 spans**, **7 judgments**
## Difficulty: {'medium': 8, 'hard': 5, 'easy': 2}

## Judgments (all new vs Batch 01)

- `2023_12_714_739` — Pankaj Bansal v. Union of India — *PMLA / arrest procedure*
- `2023_14_374_385` — Fulmati Dhramdev Yadav v. New India Assurance Co. Ltd. — *motor accident compensation*
- `2023_10_464_477` — CBI v. Shyam Bihari — *criminal evidence / IPC*
- `2023_11_264_286` — Government of Kerala v. Joseph — *property / adverse possession*
- `2023_4_739_747` — M/s Dharti Dredging and Infrastructure Ltd. v. CCE Guntur — *customs / central excise*
- `2023_4_239_245` — Atulbhai Vithalbhai Bhanderi v. State of Gujarat — *bail*
- `2023_1_719_724` — Delhi Development Authority v. Beena Gupta — *land acquisition / RFCTLARR s.24(2)*

## Per-query spans

### q_pmla_01 [medium/criminal] — 1 span(s)
Q: Must the Enforcement Directorate furnish a written copy of the grounds of arrest to a person arrested under Section 19 of the PMLA?
- `2023_12_714_739` [50632:51227] of informing the arrested person of the grounds of arrest, we hold that it would be necessary, henceforth, that a copy of such written gr ounds of arr...

### q_pmla_02 [hard/criminal] — 1 span(s)
Q: Is merely reading out the grounds of arrest to the arrestee sufficient compliance with Article 22(1) of the Constitution and Section 19(1) PMLA?
- `2023_12_714_739` [51070:51754] case on hand, the admitted position is that the ED’s Investigati ng Offi cer merely read out or permitted reading of the grounds of arrest of the appe...

### q_pmla_03 [medium/criminal] — 1 span(s)
Q: What is the duty of the remand judge when examining an arrest under Section 19 of the PMLA?
- `2023_12_714_739` [27578:28136] The learned Judge did not even record a fi nding that he perused the grounds of arrest to ascertain whether the ED had recorded reasons to believe tha...

### q_wc_01 [medium/civil] — 1 span(s)
Q: What is the scope of an appeal under Section 30 of the Workmen Compensation Act against the Commissioner's award?
- `2023_14_374_385` [9769:10256] jurisdiction of the High Court to decide the appeal is confi ned only to examine the substantial questions of law arising in the case.” 21. The other ...

### q_wc_02 [hard/civil] — 1 span(s)
Q: Can the appellate court under the Workmen Compensation Act decide the validity of the deceased employee's driving licence when the Commissioner never framed that issue?
- `2023_14_374_385` [16033:16586] It may be noted that the Commissioner had not returned any fi ndings in respect of the validity or invalidity of the license of the deceased nor was i...

### q_cbi_01 [medium/criminal] — 1 span(s)
Q: In an appeal against acquittal, when can the appellate court reverse the trial court's benefit of doubt given to the accused?
- `2023_10_464_477` [13745:14284] In these circumstances, if th e trial court gave the benefit of doubt to the accused, the judgment and order of the trial court cannot be held pervers...

### q_cbi_02 [hard/criminal] — 1 span(s)
Q: Once the ocular account of a key eyewitness is discarded, can conviction rest solely on incomplete circumstantial evidence?
- `2023_10_464_477` [22444:23012] fired shots from their service rifles. Be that as it may, once the ocular account of PW-15 stood discarded, to clinch a conviction on the basis of cir...

### q_ap_01 [medium/civil] — 1 span(s)
Q: What must a claimant prove to establish title by adverse possession against the State over government land?
- `2023_11_264_286` [4034:4560] is that possession should be open, assertive, hostile and continuous. These requirements were absent in the case. Lastly it was held that just because...

### q_ap_02 [hard/civil] — 1 span(s)
Q: Does planting trees and using government land for 15–40 years by itself perfect title by adverse possession against the State?
- `2023_11_264_286` [38675:39961] and having put the land to use for planting trees,though with a variation of period, i.e., about 15 to 40 years. Be that as it may, it has come on rec...

### q_cus_01 [medium/tax] — 1 span(s)
Q: Is a cutter suction dredger entitled to the customs exemption available for “dredgers” under the relevant notification?
- `2023_4_739_747` [14320:15269] items excluded and denied the benefit of exemption notificatio n are integral parts of a Cutter Dredger. As held earlier, eac h of the units which the...

### q_cus_02 [hard/tax] — 1 span(s)
Q: How should a multi-component cutter suction dredger be analysed for customs classification?
- `2023_4_739_747` [4465:4983] The Tribunal had after considering the various components and the relative functions, described their utility in the overall unit in the following ter...

### q_bail_01 [easy/criminal] — 1 span(s)
Q: When deciding bail on the ground of parity, what must the court focus on according to the Supreme Court?
- `2023_4_239_245` [10543:11368] from detailing our views on the merits of the matter. 12. Insofar as parity is concerned, we need only reproduce the apt observations from Ramesh Bhav...

### q_bail_02 [medium/criminal] — 2 span(s)
Q: When the material indicates the accused regularly participates in crime, how does that affect the bail application?
- `2023_4_239_245` [6809:7392] the trial. 9. Had there been no other case against the Appellant and n o material, at least prima facie , to indicate his regular participation in any...
- `2023_4_239_245` [11395:11731] In the facts and circumstances, at the present junctur e, this Court is not inclined to allow the prayer for enlarging the Appellant on bail. Accordin...

### q_la_01 [medium/civil] — 1 span(s)
Q: Does a subsequent purchaser of acquired land have locus to claim that the acquisition has lapsed under Section 24(2) of the RFCTLARR Act, 2013?
- `2023_1_719_724` [2471:2946] writ petitioner being subsequent purchaser had no locus to challenge the acquisition, by the impugned judgment and order the High Court has entertaine...

### q_la_02 [easy/civil] — 1 span(s)
Q: Does a subsequent purchaser have locus to challenge acquisition or claim lapsing under Section 24(2) of the RFCTLARR Act, 2013?
- `2023_1_719_724` [3341:3831] Under the circumstances the High Court has seriously erred in entertaining the writ petit ion preferred by the respondent no.1 – original writ petitio...

## Files
- review_batch_02_queries.jsonl
- review_batch_02_judgments.jsonl
- seed/corpus: **untouched**

---
**v1 FROZEN GOLDEN SET** — promoted 2026-10-05. Do not edit labels.
